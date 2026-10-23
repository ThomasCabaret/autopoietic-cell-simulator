#include "particle_life/template_copy.hpp"

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>

namespace {

using namespace particle_life::template_copy;

struct Options {
    std::uint32_t seed = 5489u;
    std::string sequence = "011010";
    int randomSequenceLength = 0;
    int freeZeroCount = 48;
    int freeOneCount = 48;
    std::uint64_t maximumSteps = 5000;
    std::uint64_t reportEvery = 100;
    std::size_t targetDetachedExact = 4;
    bool stopAtTarget = true;
    std::string csvPath;

    float worldWidth = 100.0f;
    float worldHeight = 60.0f;
    float captureDuration = 12.0f;
    float releaseDuration = 4.0f;
};

void printUsage(const char* executable) {
    std::cout
        << "Usage: " << executable << " [options]\n"
        << "  --seed N                    Pseudo-random seed (default 5489)\n"
        << "  --sequence BITS             Initial binary template (default 011010)\n"
        << "  --random-sequence-length N  Generate a deterministic nontrivial sequence\n"
        << "  --free-zero N               Initial free 0 monomers (default 48)\n"
        << "  --free-one N                Initial free 1 monomers (default 48)\n"
        << "  --steps N                   Maximum simulated steps (default 5000)\n"
        << "  --report-every N            Report interval in steps (default 100)\n"
        << "  --target-exact N            Required detached exact chains (default 4)\n"
        << "  --continue-after-target     Do not stop when the target is reached\n"
        << "  --world-width X             Periodic world width (default 160)\n"
        << "  --world-height X            Periodic world height (default 90)\n"
        << "  --capture-duration X        Capture phase duration (default 12 s)\n"
        << "  --release-duration X        Release phase duration (default 4 s)\n"
        << "  --csv PATH                  Write the time series to a CSV file\n"
        << "  --help                      Show this help\n";
}

template <typename Value>
Value parseNumber(const char* text, const char* option) {
    std::istringstream stream(text);
    Value value{};
    stream >> value;
    if (!stream || !stream.eof()) {
        throw std::invalid_argument(std::string("Invalid value for ") + option + ": " + text);
    }
    return value;
}

const char* requireValue(int& index, int argc, char** argv, const char* option) {
    if (index + 1 >= argc) {
        throw std::invalid_argument(std::string("Missing value after ") + option);
    }
    return argv[++index];
}

Options parseOptions(int argc, char** argv) {
    Options options;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--help") {
            printUsage(argv[0]);
            std::exit(EXIT_SUCCESS);
        } else if (argument == "--seed") {
            options.seed = parseNumber<std::uint32_t>(requireValue(index, argc, argv, "--seed"), "--seed");
        } else if (argument == "--sequence") {
            options.sequence = requireValue(index, argc, argv, "--sequence");
        } else if (argument == "--random-sequence-length") {
            options.randomSequenceLength = parseNumber<int>(
                requireValue(index, argc, argv, "--random-sequence-length"),
                "--random-sequence-length");
        } else if (argument == "--free-zero") {
            options.freeZeroCount = parseNumber<int>(requireValue(index, argc, argv, "--free-zero"), "--free-zero");
        } else if (argument == "--free-one") {
            options.freeOneCount = parseNumber<int>(requireValue(index, argc, argv, "--free-one"), "--free-one");
        } else if (argument == "--steps") {
            options.maximumSteps = parseNumber<std::uint64_t>(requireValue(index, argc, argv, "--steps"), "--steps");
        } else if (argument == "--report-every") {
            options.reportEvery = parseNumber<std::uint64_t>(
                requireValue(index, argc, argv, "--report-every"),
                "--report-every");
        } else if (argument == "--target-exact") {
            options.targetDetachedExact = parseNumber<std::size_t>(
                requireValue(index, argc, argv, "--target-exact"),
                "--target-exact");
        } else if (argument == "--continue-after-target") {
            options.stopAtTarget = false;
        } else if (argument == "--world-width") {
            options.worldWidth = parseNumber<float>(requireValue(index, argc, argv, "--world-width"), "--world-width");
        } else if (argument == "--world-height") {
            options.worldHeight = parseNumber<float>(requireValue(index, argc, argv, "--world-height"), "--world-height");
        } else if (argument == "--capture-duration") {
            options.captureDuration = parseNumber<float>(
                requireValue(index, argc, argv, "--capture-duration"),
                "--capture-duration");
        } else if (argument == "--release-duration") {
            options.releaseDuration = parseNumber<float>(
                requireValue(index, argc, argv, "--release-duration"),
                "--release-duration");
        } else if (argument == "--csv") {
            options.csvPath = requireValue(index, argc, argv, "--csv");
        } else {
            throw std::invalid_argument("Unknown argument: " + argument);
        }
    }

    if (options.randomSequenceLength != 0
        && (options.randomSequenceLength < 2 || options.randomSequenceLength > 32)) {
        throw std::invalid_argument("--random-sequence-length must be between 2 and 32");
    }
    if (options.freeZeroCount < 0 || options.freeOneCount < 0) {
        throw std::invalid_argument("Free monomer counts cannot be negative");
    }
    if (options.maximumSteps == 0 || options.reportEvery == 0) {
        throw std::invalid_argument("--steps and --report-every must be positive");
    }
    if (options.targetDetachedExact == 0) {
        throw std::invalid_argument("--target-exact must be positive");
    }
    if (options.worldWidth <= 0.0f || options.worldHeight <= 0.0f) {
        throw std::invalid_argument("World dimensions must be positive");
    }
    return options;
}

std::string generateSequence(std::uint32_t seed, int length) {
    std::mt19937 random(seed ^ 0x9e3779b9u);
    std::uniform_int_distribution<int> symbol(0, 1);
    std::string sequence(static_cast<std::size_t>(length), '0');
    bool hasZero = false;
    bool hasOne = false;
    for (char& character : sequence) {
        character = symbol(random) == 0 ? '0' : '1';
        hasZero = hasZero || character == '0';
        hasOne = hasOne || character == '1';
    }
    if (!hasZero) {
        sequence.back() = '0';
    } else if (!hasOne) {
        sequence.back() = '1';
    }
    return sequence;
}

std::string formatCensus(const Model& model) {
    std::ostringstream output;
    bool first = true;
    for (const SequenceCensusEntry& entry : model.sequenceCensus()) {
        if (!first) {
            output << ';';
        }
        first = false;
        output << entry.sequence << '=' << entry.totalCount << '/' << entry.detachedCount;
    }
    return output.str();
}

void writeReport(
    std::ostream& output,
    const Model& model,
    const Statistics& statistics,
    bool csv) {
    const std::string census = formatCensus(model);
    if (csv) {
        output
            << model.stepCount() << ','
            << std::fixed << std::setprecision(4) << model.simulationTime() << ','
            << (model.phase() == CyclePhase::Capture ? "capture" : "release") << ','
            << statistics.exactSequenceCount << ','
            << statistics.detachedExactSequenceCount << ','
            << statistics.exactCopyCount << ','
            << statistics.detachedExactCopyCount << ','
            << statistics.chainCount << ','
            << statistics.fullLengthChainCount << ','
            << statistics.pairBondCount << ','
            << statistics.freeMonomerCount << ','
            << statistics.longestChainLength << ','
            << '"' << census << '"' << '\n';
        return;
    }

    output
        << "step=" << model.stepCount()
        << " time=" << std::fixed << std::setprecision(2) << model.simulationTime()
        << " phase=" << phaseName(model.phase())
        << " exact=" << statistics.exactSequenceCount
        << " detached_exact=" << statistics.detachedExactSequenceCount
        << " detached_copies=" << statistics.detachedExactCopyCount
        << " chains=" << statistics.chainCount
        << " full_length=" << statistics.fullLengthChainCount
        << " pairs=" << statistics.pairBondCount
        << " free=" << statistics.freeMonomerCount
        << " longest=" << statistics.longestChainLength
        << " census={" << census << "}\n";
}

} // namespace

int main(int argc, char** argv) {
    try {
        Options options = parseOptions(argc, argv);
        if (options.randomSequenceLength != 0) {
            options.sequence = generateSequence(options.seed, options.randomSequenceLength);
        }
        if (!isValidSequence(options.sequence)) {
            throw std::invalid_argument("Sequence must contain 2 to 32 binary symbols");
        }

        Model model(options.seed);
        Config& config = model.config();
        config.worldWidth = options.worldWidth;
        config.worldHeight = options.worldHeight;
        config.captureDuration = options.captureDuration;
        config.releaseDuration = options.releaseDuration;
        model.reset(options.sequence, options.freeZeroCount, options.freeOneCount);

        std::ofstream csv;
        if (!options.csvPath.empty()) {
            csv.open(options.csvPath, std::ios::out | std::ios::trunc);
            if (!csv) {
                throw std::runtime_error("Cannot open CSV output: " + options.csvPath);
            }
            csv
                << "step,time,phase,exact,detached_exact,copies,detached_copies,chains,"
                << "full_length,pair_bonds,free_monomers,longest_chain,census\n";
        }

        std::cout
            << "Template-copy headless run\n"
            << "seed=" << options.seed
            << " sequence=" << options.sequence
            << " free_zero=" << options.freeZeroCount
            << " free_one=" << options.freeOneCount
            << " target_detached_exact=" << options.targetDetachedExact
            << "\n";

        bool targetReached = false;
        double firstTargetTime = 0.0;
        for (std::uint64_t step = 0; step < options.maximumSteps; ++step) {
            model.step();
            const bool reportDue = model.stepCount() % options.reportEvery == 0;
            Statistics statistics;
            bool haveStatistics = false;

            if (reportDue || !targetReached) {
                statistics = model.statistics();
                haveStatistics = true;
                if (!targetReached
                    && statistics.detachedExactSequenceCount >= options.targetDetachedExact) {
                    targetReached = true;
                    firstTargetTime = model.simulationTime();
                }
            }

            if (reportDue || (targetReached && options.stopAtTarget)) {
                if (!haveStatistics) {
                    statistics = model.statistics();
                }
                writeReport(std::cout, model, statistics, false);
                if (csv) {
                    writeReport(csv, model, statistics, true);
                }
            }

            if (targetReached && options.stopAtTarget) {
                break;
            }
        }

        const Statistics finalStatistics = model.statistics();
        if (!targetReached
            && finalStatistics.detachedExactSequenceCount >= options.targetDetachedExact) {
            targetReached = true;
            firstTargetTime = model.simulationTime();
        }

        std::cout
            << "result=" << (targetReached ? "success" : "target_not_reached")
            << " first_target_time=" << std::fixed << std::setprecision(2) << firstTargetTime
            << " final_detached_exact=" << finalStatistics.detachedExactSequenceCount
            << " final_census={" << formatCensus(model) << "}\n";

        return targetReached ? EXIT_SUCCESS : EXIT_FAILURE;
    } catch (const std::exception& exception) {
        std::cerr << "Error: " << exception.what() << '\n';
        return EXIT_FAILURE;
    }
}
