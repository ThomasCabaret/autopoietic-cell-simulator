#include "particle_life/experiment.hpp"

#include <stdexcept>

namespace particle_life {

void ExperimentPlan::addSpawn(SpawnEvent event) {
    spawnEvents_.push_back(event);
}

void ExperimentPlan::addPeriodicSource(PeriodicSource source) {
    if (source.period == 0) {
        throw std::invalid_argument("Periodic source period must be non-zero");
    }
    if (source.lastStep < source.firstStep) {
        throw std::invalid_argument("Periodic source last step precedes first step");
    }
    periodicSources_.push_back(source);
}

void ExperimentPlan::applyBeforeStep(Simulation& simulation) const {
    const std::uint64_t currentStep = simulation.stepIndex();

    for (const SpawnEvent& event : spawnEvents_) {
        if (event.step == currentStep) {
            simulation.spawnMany(event.type, event.count, event.origin);
        }
    }

    for (const PeriodicSource& source : periodicSources_) {
        if (currentStep < source.firstStep || currentStep > source.lastStep) {
            continue;
        }
        if ((currentStep - source.firstStep) % source.period == 0) {
            simulation.spawnMany(source.type, source.count, source.origin);
        }
    }
}

} // namespace particle_life
