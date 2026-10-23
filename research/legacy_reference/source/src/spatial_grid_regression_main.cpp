#include "particle_life/simulation.hpp"

#include <cmath>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

bool sameFloat(float lhs, float rhs) {
    return lhs == rhs || (std::isnan(lhs) && std::isnan(rhs));
}

void requireSameParticle(
    const particle_life::Particle& bruteForce,
    const particle_life::Particle& spatial,
    std::size_t index,
    std::uint64_t step) {
    const bool same =
        bruteForce.id == spatial.id &&
        sameFloat(bruteForce.position.x, spatial.position.x) &&
        sameFloat(bruteForce.position.y, spatial.position.y) &&
        sameFloat(bruteForce.velocity.x, spatial.velocity.x) &&
        sameFloat(bruteForce.velocity.y, spatial.velocity.y) &&
        sameFloat(bruteForce.orientation, spatial.orientation) &&
        sameFloat(bruteForce.angularVelocity, spatial.angularVelocity) &&
        sameFloat(bruteForce.force.x, spatial.force.x) &&
        sameFloat(bruteForce.force.y, spatial.force.y) &&
        sameFloat(bruteForce.torque, spatial.torque) &&
        bruteForce.type == spatial.type &&
        bruteForce.spawnStep == spatial.spawnStep &&
        bruteForce.leftBond == spatial.leftBond &&
        bruteForce.rightBond == spatial.rightBond;

    if (!same) {
        throw std::runtime_error(
            "Spatial-grid regression at step " + std::to_string(step) +
            ", particle " + std::to_string(index));
    }
}

void setParticle(
    particle_life::Simulation& simulation,
    particle_life::ParticleType type,
    particle_life::Vec2 position,
    float orientation) {
    const std::size_t index = simulation.spawn(type);
    particle_life::Particle& particle = simulation.particles()[index];
    particle.position = position;
    particle.velocity = {};
    particle.orientation = orientation;
    particle.angularVelocity = 0.0f;
}


void verifyPeriodicSeamBond() {
    particle_life::SimulationConfig config;
    config.boundaryMode = particle_life::BoundaryMode::Wrap;
    config.patch.temperature = 0.0f;
    config.patch.thermalBreakRate = 0.0f;
    config.patch.preferredTurnAngle = 0.4f;

    particle_life::Simulation initializer(config, 17U);
    setParticle(initializer, particle_life::ParticleType::P, {238.0f, 0.0f}, -1.5707963f);
    setParticle(initializer, particle_life::ParticleType::P, {-237.0f, 1.0f}, -1.1707963f);

    particle_life::SimulationSnapshot bruteSnapshot = initializer.snapshot();
    particle_life::SimulationSnapshot spatialSnapshot = bruteSnapshot;
    bruteSnapshot.config.neighborSearchMode = particle_life::NeighborSearchMode::BruteForce;
    spatialSnapshot.config.neighborSearchMode = particle_life::NeighborSearchMode::SpatialGrid;

    particle_life::Simulation bruteForce;
    particle_life::Simulation spatial;
    bruteForce.restore(bruteSnapshot);
    spatial.restore(spatialSnapshot);
    bruteForce.step();
    spatial.step();

    if (bruteForce.patchBondCount() != 1U || spatial.patchBondCount() != 1U) {
        throw std::runtime_error("Periodic seam patch bond was not formed");
    }
    for (std::size_t index = 0; index < bruteForce.particles().size(); ++index) {
        requireSameParticle(bruteForce.particles()[index], spatial.particles()[index], index, 1U);
    }
}

void runComparison(
    const particle_life::SimulationSnapshot& initialSnapshot,
    particle_life::BoundaryMode boundaryMode,
    std::uint64_t steps) {
    particle_life::SimulationSnapshot bruteSnapshot = initialSnapshot;
    particle_life::SimulationSnapshot spatialSnapshot = initialSnapshot;
    bruteSnapshot.config.boundaryMode = boundaryMode;
    spatialSnapshot.config.boundaryMode = boundaryMode;
    bruteSnapshot.config.neighborSearchMode = particle_life::NeighborSearchMode::BruteForce;
    spatialSnapshot.config.neighborSearchMode = particle_life::NeighborSearchMode::SpatialGrid;

    particle_life::Simulation bruteForce;
    particle_life::Simulation spatial;
    bruteForce.restore(bruteSnapshot);
    spatial.restore(spatialSnapshot);

    for (std::uint64_t step = 1; step <= steps; ++step) {
        bruteForce.step();
        spatial.step();

        if (bruteForce.particles().size() != spatial.particles().size()) {
            throw std::runtime_error("Particle count diverged at step " + std::to_string(step));
        }
        for (std::size_t index = 0; index < bruteForce.particles().size(); ++index) {
            requireSameParticle(
                bruteForce.particles()[index],
                spatial.particles()[index],
                index,
                step);
        }
        const particle_life::SimulationSnapshot bruteState = bruteForce.snapshot();
        const particle_life::SimulationSnapshot spatialState = spatial.snapshot();
        if (bruteState.randomEngineState != spatialState.randomEngineState) {
            throw std::runtime_error("Random engine state diverged at step " + std::to_string(step));
        }
        if (bruteState.nextParticleId != spatialState.nextParticleId) {
            throw std::runtime_error("Particle id state diverged at step " + std::to_string(step));
        }
    }
}

} // namespace

int main() {
    try {
        constexpr std::uint32_t seed = 0x5a17c9e3U;
        particle_life::SimulationConfig baseConfig;
        baseConfig.boundaryMode = particle_life::BoundaryMode::LegacyContainment;
        baseConfig.patch.temperature = 0.15f;
        baseConfig.patch.thermalBreakRate = 0.03f;

        particle_life::Simulation initializer(baseConfig, seed);
        initializer.spawnMany(particle_life::ParticleType::F, 120);
        initializer.spawnMany(particle_life::ParticleType::A, 15);
        initializer.spawnMany(particle_life::ParticleType::B, 15);
        initializer.spawnMany(particle_life::ParticleType::S, 60);
        initializer.spawnMany(particle_life::ParticleType::L, 8);
        initializer.spawnMany(particle_life::ParticleType::P, 80);

        // Positive, negative and exact cell-boundary coordinates.
        setParticle(initializer, particle_life::ParticleType::S, {13.0f, 0.0f}, 0.0f);
        setParticle(initializer, particle_life::ParticleType::S, {-13.0f, 0.0f}, 0.1f);
        setParticle(initializer, particle_life::ParticleType::A, {0.0f, 13.0f}, 0.2f);
        setParticle(initializer, particle_life::ParticleType::F, {0.0f, -13.0f}, 0.3f);

        // Patch candidates on ordinary and periodic seams.
        setParticle(initializer, particle_life::ParticleType::P, {-2.5f, 0.0f}, -1.5707963f);
        setParticle(initializer, particle_life::ParticleType::P, {2.5f, 0.0f}, -1.3507963f);
        setParticle(initializer, particle_life::ParticleType::P, {-239.0f, 40.0f}, -1.5707963f);
        setParticle(initializer, particle_life::ParticleType::P, {239.0f, 40.0f}, -1.3507963f);

        verifyPeriodicSeamBond();

        const particle_life::SimulationSnapshot initialSnapshot = initializer.snapshot();
        runComparison(
            initialSnapshot,
            particle_life::BoundaryMode::LegacyContainment,
            1000);
        runComparison(initialSnapshot, particle_life::BoundaryMode::Wrap, 1000);

        std::cout << "Spatial grid matches brute force for legacy and periodic boundaries.\n";
        return 0;
    } catch (const std::exception& exception) {
        std::cerr << "Regression failure: " << exception.what() << '\n';
        return 1;
    }
}
