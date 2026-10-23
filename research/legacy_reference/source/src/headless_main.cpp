#include "particle_life/checkpoint.hpp"
#include "particle_life/experiment.hpp"
#include "particle_life/metrics.hpp"
#include "particle_life/runner.hpp"
#include "particle_life/simulation.hpp"

#include <array>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {

struct Options {
    std::uint32_t seed = 5489u;
    std::uint64_t steps = 10000;
    std::filesystem::path loadCheckpoint;
    std::filesystem::path saveCheckpoint;
    std::uint64_t checkpointEvery = 0;
    std::filesystem::path metricsPath;
    std::uint64_t metricsEvery = 100;
    double realtimeStepsPerSecond = 0.0;
    bool bruteForce = false;
    particle_life::BoundaryMode boundaryMode = particle_life::BoundaryMode::LegacyContainment;
    bool boundarySpecified = false;

    std::array<std::size_t, 6> initialCounts{};

    bool periodicSourceEnabled = false;
    particle_life::PeriodicSource periodicSource;
};

std::uint64_t parseUnsigned64(const char* text) {
    std::size_t consumed = 0;
    const std::string value(text);
    const unsigned long long result = std::stoull(value, &consumed);
    if (consumed != value.size()) {
        throw std::invalid_argument("Invalid unsigned integer: " + value);
    }
    return static_cast<std::uint64_t>(result);
}

std::uint32_t parseUnsigned32(const char* text) {
    const std::uint64_t value = parseUnsigned64(text);
    if (value > std::numeric_limits<std::uint32_t>::max()) {
        throw std::out_of_range("Seed is outside uint32 range");
    }
    return static_cast<std::uint32_t>(value);
}

double parseDouble(const char* text) {
    std::size_t consumed = 0;
    const std::string value(text);
    const double result = std::stod(value, &consumed);
    if (consumed != value.size()) {
        throw std::invalid_argument("Invalid floating point value: " + value);
    }
    return result;
}

const char* requireValue(int argc, char** argv, int& index) {
    if (index + 1 >= argc) {
        throw std::invalid_argument(std::string("Missing value after ") + argv[index]);
    }
    return argv[++index];
}

particle_life::BoundaryMode parseBoundaryMode(const std::string& value) {
    if (value == "contain" || value == "legacy") {
        return particle_life::BoundaryMode::LegacyContainment;
    }
    if (value == "destroy") {
        return particle_life::BoundaryMode::Destroy;
    }
    if (value == "reflect" || value == "closed") {
        return particle_life::BoundaryMode::Reflect;
    }
    if (value == "wrap" || value == "periodic") {
        return particle_life::BoundaryMode::Wrap;
    }
    throw std::invalid_argument(
        "--boundary expects contain, destroy, reflect or wrap");
}

Options parseOptions(int argc, char** argv) {
    Options options;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--seed") {
            options.seed = parseUnsigned32(requireValue(argc, argv, index));
        } else if (argument == "--steps") {
            options.steps = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--load") {
            options.loadCheckpoint = requireValue(argc, argv, index);
        } else if (argument == "--checkpoint") {
            options.saveCheckpoint = requireValue(argc, argv, index);
        } else if (argument == "--checkpoint-every") {
            options.checkpointEvery = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--metrics") {
            options.metricsPath = requireValue(argc, argv, index);
        } else if (argument == "--metrics-every") {
            options.metricsEvery = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--realtime-hz") {
            options.realtimeStepsPerSecond = parseDouble(requireValue(argc, argv, index));
        } else if (argument == "--brute-force") {
            options.bruteForce = true;
        } else if (argument == "--boundary") {
            options.boundaryMode = parseBoundaryMode(requireValue(argc, argv, index));
            options.boundarySpecified = true;
        } else if (argument == "--initial-f") {
            options.initialCounts[0] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--initial-a") {
            options.initialCounts[1] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--initial-b") {
            options.initialCounts[2] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--initial-s") {
            options.initialCounts[3] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--initial-l") {
            options.initialCounts[4] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--initial-p") {
            options.initialCounts[5] = parseUnsigned64(requireValue(argc, argv, index));
        } else if (argument == "--source-type") {
            const std::string value = requireValue(argc, argv, index);
            if (value.size() != 1U) {
                throw std::invalid_argument("--source-type expects one of F, A, B, S, L, P");
            }
            options.periodicSource.type = particle_life::particleTypeFromCode(value[0]);
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-count") {
            options.periodicSource.count = parseUnsigned64(requireValue(argc, argv, index));
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-period") {
            options.periodicSource.period = parseUnsigned64(requireValue(argc, argv, index));
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-start") {
            options.periodicSource.firstStep = parseUnsigned64(requireValue(argc, argv, index));
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-end") {
            options.periodicSource.lastStep = parseUnsigned64(requireValue(argc, argv, index));
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-x") {
            options.periodicSource.origin.x = static_cast<float>(parseDouble(requireValue(argc, argv, index)));
            options.periodicSourceEnabled = true;
        } else if (argument == "--source-y") {
            options.periodicSource.origin.y = static_cast<float>(parseDouble(requireValue(argc, argv, index)));
            options.periodicSourceEnabled = true;
        } else if (argument == "--help") {
            std::cout
                << "Particle Life headless runner\n"
                << "  --seed N --steps N --load FILE\n"
                << "  --checkpoint FILE [--checkpoint-every N]\n"
                << "  --metrics FILE [--metrics-every N]\n"
                << "  --realtime-hz HZ --brute-force\n"
                << "  --boundary contain|destroy|reflect|wrap\n"
                << "  --initial-f N --initial-a N --initial-b N --initial-s N\n"
                << "  --initial-l N --initial-p N\n"
                << "  --source-type F|A|B|S|L|P --source-count N --source-period N\n"
                << "  --source-start N --source-end N --source-x X --source-y Y\n";
            std::exit(0);
        } else {
            throw std::invalid_argument("Unknown argument: " + argument);
        }
    }
    return options;
}

} // namespace

int main(int argc, char** argv) {
    try {
        const Options options = parseOptions(argc, argv);

        particle_life::Simulation simulation({}, options.seed);
        if (!options.loadCheckpoint.empty()) {
            simulation.restore(particle_life::CheckpointIO::load(options.loadCheckpoint));
        }
        if (options.bruteForce) {
            simulation.config().neighborSearchMode = particle_life::NeighborSearchMode::BruteForce;
        }
        if (options.boundarySpecified) {
            simulation.config().boundaryMode = options.boundaryMode;
        }

        particle_life::ExperimentPlan experiment;
        const std::array<particle_life::ParticleType, 6> types = {
            particle_life::ParticleType::F,
            particle_life::ParticleType::A,
            particle_life::ParticleType::B,
            particle_life::ParticleType::S,
            particle_life::ParticleType::L,
            particle_life::ParticleType::P
        };
        for (std::size_t index = 0; index < types.size(); ++index) {
            if (options.initialCounts[index] != 0U) {
                experiment.addSpawn({0, types[index], options.initialCounts[index], {}});
            }
        }
        if (options.periodicSourceEnabled) {
            experiment.addPeriodicSource(options.periodicSource);
        }

        particle_life::RunOptions runOptions;
        runOptions.steps = options.steps;
        runOptions.realtimeStepsPerSecond = options.realtimeStepsPerSecond;
        runOptions.metricsPath = options.metricsPath;
        runOptions.metricsEverySteps = options.metricsEvery;
        runOptions.checkpointPath = options.saveCheckpoint;
        runOptions.checkpointEverySteps = options.checkpointEvery;
        runOptions.saveFinalCheckpoint = !options.saveCheckpoint.empty();

        particle_life::SimulationRunner::run(simulation, experiment, runOptions);

        const particle_life::MetricsSample metrics = particle_life::collectMetrics(simulation);
        std::cout << "seed=" << simulation.seed() << " step=" << metrics.step
                  << " total=" << metrics.total << " F=" << metrics.typeCounts[0]
                  << " A=" << metrics.typeCounts[1] << " B=" << metrics.typeCounts[2]
                  << " S=" << metrics.typeCounts[3] << " L=" << metrics.typeCounts[4]
                  << " P=" << metrics.typeCounts[5]
                  << " patch_bonds=" << metrics.patchBonds << '\n';
        return 0;
    } catch (const std::exception& exception) {
        std::cerr << "Error: " << exception.what() << '\n';
        return 1;
    }
}
