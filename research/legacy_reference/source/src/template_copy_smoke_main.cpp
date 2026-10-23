#include "particle_life/template_copy.hpp"

#include <algorithm>
#include <array>
#include <cstdlib>
#include <iomanip>
#include <iostream>

int main() {
    using namespace particle_life::template_copy;

    constexpr std::array<std::uint32_t, 16> seeds = {
        1u, 2u, 3u, 4u, 5u, 7u, 11u, 17u,
        23u, 42u, 101u, 777u, 2024u, 5489u, 12345u, 98765u
    };
    constexpr std::uint64_t maximumSteps = 2500;
    constexpr std::size_t targetDetachedExact = 4;
    constexpr const char* sequence = "011010";

    bool allSucceeded = true;
    double slowestSuccessTime = 0.0;

    for (const std::uint32_t seed : seeds) {
        Model model(seed);
        model.reset(sequence, 48, 48);

        bool succeeded = false;
        for (std::uint64_t step = 0; step < maximumSteps; ++step) {
            model.step();
            if ((step + 1) % 25 != 0) {
                continue;
            }

            const Statistics statistics = model.statistics();
            if (statistics.detachedExactSequenceCount >= targetDetachedExact) {
                succeeded = true;
                slowestSuccessTime = std::max(slowestSuccessTime, model.simulationTime());
                std::cout
                    << "seed=" << seed
                    << " success_time=" << std::fixed << std::setprecision(2)
                    << model.simulationTime()
                    << " detached_exact=" << statistics.detachedExactSequenceCount
                    << " chains=" << statistics.chainCount
                    << '\n';
                break;
            }
        }

        if (!succeeded) {
            allSucceeded = false;
            const Statistics statistics = model.statistics();
            std::cerr
                << "seed=" << seed
                << " failed after " << maximumSteps << " steps"
                << " exact=" << statistics.exactSequenceCount
                << " detached_exact=" << statistics.detachedExactSequenceCount
                << " chains=" << statistics.chainCount
                << " longest=" << statistics.longestChainLength
                << '\n';
        }
    }

    if (!allSucceeded) {
        return EXIT_FAILURE;
    }

    std::cout
        << "Template-copy replication test succeeded for " << seeds.size()
        << " deterministic seeds. Slowest success time="
        << std::fixed << std::setprecision(2) << slowestSuccessTime << " s.\n";
    return EXIT_SUCCESS;
}
