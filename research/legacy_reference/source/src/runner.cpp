#include "particle_life/runner.hpp"

#include "particle_life/checkpoint.hpp"
#include "particle_life/metrics.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>
#include <thread>

namespace particle_life {

void SimulationRunner::run(
    Simulation& simulation,
    const ExperimentPlan& experiment,
    const RunOptions& options) {
    if (!options.metricsPath.empty() && options.metricsEverySteps == 0) {
        throw std::invalid_argument("metricsEverySteps must be non-zero");
    }
    if (options.realtimeStepsPerSecond < 0.0) {
        throw std::invalid_argument("realtimeStepsPerSecond cannot be negative");
    }

    std::unique_ptr<MetricsCsvWriter> metricsWriter;
    if (!options.metricsPath.empty()) {
        metricsWriter = std::make_unique<MetricsCsvWriter>(options.metricsPath);
        metricsWriter->append(simulation);
    }

    using Clock = std::chrono::steady_clock;
    Clock::time_point nextStepTime = Clock::now();
    const std::chrono::duration<double> stepDuration =
        options.realtimeStepsPerSecond > 0.0
            ? std::chrono::duration<double>(1.0 / options.realtimeStepsPerSecond)
            : std::chrono::duration<double>::zero();

    for (std::uint64_t index = 0; index < options.steps; ++index) {
        experiment.applyBeforeStep(simulation);
        simulation.step();

        if (metricsWriter && simulation.stepIndex() % options.metricsEverySteps == 0) {
            metricsWriter->append(simulation);
        }

        if (
            !options.checkpointPath.empty() && options.checkpointEverySteps != 0 &&
            simulation.stepIndex() % options.checkpointEverySteps == 0) {
            CheckpointIO::save(options.checkpointPath, simulation);
        }

        if (options.realtimeStepsPerSecond > 0.0) {
            nextStepTime += std::chrono::duration_cast<Clock::duration>(stepDuration);
            std::this_thread::sleep_until(nextStepTime);
        }
    }

    if (options.saveFinalCheckpoint && !options.checkpointPath.empty()) {
        CheckpointIO::save(options.checkpointPath, simulation);
    }
}

} // namespace particle_life
