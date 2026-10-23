#include "particle_life/checkpoint.hpp"

#include <algorithm>
#include <fstream>
#include <iomanip>
#include <limits>
#include <locale>
#include <stdexcept>
#include <string>

namespace particle_life {
namespace {

constexpr int kCheckpointVersion = 2;

void requireKey(std::istream& input, const char* expected) {
    std::string actual;
    input >> actual;
    if (!input || actual != expected) {
        throw std::runtime_error(std::string("Expected checkpoint key: ") + expected);
    }
}

void writeConfig(std::ostream& output, const SimulationConfig& config) {
    output << "world_width " << config.worldWidth << '\n';
    output << "world_height " << config.worldHeight << '\n';
    output << "dot_size " << config.dotSize << '\n';
    output << "centerize " << config.centerize << '\n';
    output << "boundary_mode " << static_cast<int>(config.boundaryMode) << '\n';
    output << "interaction_radius " << config.interactionRadius << '\n';
    output << "brownian_speed " << config.brownianSpeed << '\n';
    output << "dt " << config.dt << '\n';
    output << "void_viscosity " << config.voidViscosity << '\n';
    output << "void_torque_viscosity " << config.voidTorqueViscosity << '\n';
    output << "containing_force " << config.containingForce << '\n';
    output << "division_angle " << config.divisionAngle << '\n';
    output << "surfactant_force_strength " << config.surfactantForceStrength << '\n';
    output << "surfactant_torque_strength " << config.surfactantTorqueStrength << '\n';
    output << "surfactant_force_exponent " << config.surfactantForceExponent << '\n';
    output << "surfactant_force_viscosity " << config.surfactantForceViscosity << '\n';
    output << "surfactant_torque_viscosity " << config.surfactantTorqueViscosity << '\n';
    output << "opposition_threshold " << config.oppositionThreshold << '\n';
    output << "center_force " << config.centerForce << '\n';

    output << "patch_bond_length " << config.patch.bondLength << '\n';
    output << "patch_capture_radius " << config.patch.captureRadius << '\n';
    output << "patch_capture_angle " << config.patch.captureAngle << '\n';
    output << "patch_preferred_turn_angle " << config.patch.preferredTurnAngle << '\n';
    output << "patch_bond_stiffness " << config.patch.bondStiffness << '\n';
    output << "patch_bending_stiffness " << config.patch.bendingStiffness << '\n';
    output << "patch_bond_damping " << config.patch.bondDamping << '\n';
    output << "patch_break_distance " << config.patch.breakDistance << '\n';
    output << "patch_break_angle " << config.patch.breakAngle << '\n';
    output << "patch_core_repulsion_radius " << config.patch.coreRepulsionRadius << '\n';
    output << "patch_core_repulsion_strength " << config.patch.coreRepulsionStrength << '\n';
    output << "patch_temperature " << config.patch.temperature << '\n';
    output << "patch_thermal_break_rate " << config.patch.thermalBreakRate << '\n';

    output << "neighbor_search_mode " << static_cast<int>(config.neighborSearchMode) << '\n';
}

SimulationConfig readConfigV1(std::istream& input) {
    SimulationConfig config;
    bool destroyAtBoundary = false;
    int neighborSearchMode = 0;

    requireKey(input, "world_width");
    input >> config.worldWidth;
    requireKey(input, "world_height");
    input >> config.worldHeight;
    requireKey(input, "dot_size");
    input >> config.dotSize;
    requireKey(input, "centerize");
    input >> config.centerize;
    requireKey(input, "destroy_at_boundary");
    input >> destroyAtBoundary;
    config.boundaryMode = destroyAtBoundary
        ? BoundaryMode::Destroy
        : BoundaryMode::LegacyContainment;
    requireKey(input, "interaction_radius");
    input >> config.interactionRadius;
    requireKey(input, "brownian_speed");
    input >> config.brownianSpeed;
    requireKey(input, "dt");
    input >> config.dt;
    requireKey(input, "void_viscosity");
    input >> config.voidViscosity;
    requireKey(input, "void_torque_viscosity");
    input >> config.voidTorqueViscosity;
    requireKey(input, "containing_force");
    input >> config.containingForce;
    requireKey(input, "division_angle");
    input >> config.divisionAngle;
    requireKey(input, "surfactant_force_strength");
    input >> config.surfactantForceStrength;
    requireKey(input, "surfactant_torque_strength");
    input >> config.surfactantTorqueStrength;
    requireKey(input, "surfactant_force_exponent");
    input >> config.surfactantForceExponent;
    requireKey(input, "surfactant_force_viscosity");
    input >> config.surfactantForceViscosity;
    requireKey(input, "surfactant_torque_viscosity");
    input >> config.surfactantTorqueViscosity;
    requireKey(input, "opposition_threshold");
    input >> config.oppositionThreshold;
    requireKey(input, "center_force");
    input >> config.centerForce;
    requireKey(input, "neighbor_search_mode");
    input >> neighborSearchMode;

    if (!input || neighborSearchMode < 0 || neighborSearchMode > 1) {
        throw std::runtime_error("Invalid simulation configuration in checkpoint");
    }
    config.neighborSearchMode = static_cast<NeighborSearchMode>(neighborSearchMode);
    return config;
}

SimulationConfig readConfigV2(std::istream& input) {
    SimulationConfig config;
    int boundaryMode = 0;
    int neighborSearchMode = 0;

    requireKey(input, "world_width");
    input >> config.worldWidth;
    requireKey(input, "world_height");
    input >> config.worldHeight;
    requireKey(input, "dot_size");
    input >> config.dotSize;
    requireKey(input, "centerize");
    input >> config.centerize;
    requireKey(input, "boundary_mode");
    input >> boundaryMode;
    requireKey(input, "interaction_radius");
    input >> config.interactionRadius;
    requireKey(input, "brownian_speed");
    input >> config.brownianSpeed;
    requireKey(input, "dt");
    input >> config.dt;
    requireKey(input, "void_viscosity");
    input >> config.voidViscosity;
    requireKey(input, "void_torque_viscosity");
    input >> config.voidTorqueViscosity;
    requireKey(input, "containing_force");
    input >> config.containingForce;
    requireKey(input, "division_angle");
    input >> config.divisionAngle;
    requireKey(input, "surfactant_force_strength");
    input >> config.surfactantForceStrength;
    requireKey(input, "surfactant_torque_strength");
    input >> config.surfactantTorqueStrength;
    requireKey(input, "surfactant_force_exponent");
    input >> config.surfactantForceExponent;
    requireKey(input, "surfactant_force_viscosity");
    input >> config.surfactantForceViscosity;
    requireKey(input, "surfactant_torque_viscosity");
    input >> config.surfactantTorqueViscosity;
    requireKey(input, "opposition_threshold");
    input >> config.oppositionThreshold;
    requireKey(input, "center_force");
    input >> config.centerForce;

    requireKey(input, "patch_bond_length");
    input >> config.patch.bondLength;
    requireKey(input, "patch_capture_radius");
    input >> config.patch.captureRadius;
    requireKey(input, "patch_capture_angle");
    input >> config.patch.captureAngle;
    requireKey(input, "patch_preferred_turn_angle");
    input >> config.patch.preferredTurnAngle;
    requireKey(input, "patch_bond_stiffness");
    input >> config.patch.bondStiffness;
    requireKey(input, "patch_bending_stiffness");
    input >> config.patch.bendingStiffness;
    requireKey(input, "patch_bond_damping");
    input >> config.patch.bondDamping;
    requireKey(input, "patch_break_distance");
    input >> config.patch.breakDistance;
    requireKey(input, "patch_break_angle");
    input >> config.patch.breakAngle;
    requireKey(input, "patch_core_repulsion_radius");
    input >> config.patch.coreRepulsionRadius;
    requireKey(input, "patch_core_repulsion_strength");
    input >> config.patch.coreRepulsionStrength;
    requireKey(input, "patch_temperature");
    input >> config.patch.temperature;
    requireKey(input, "patch_thermal_break_rate");
    input >> config.patch.thermalBreakRate;

    requireKey(input, "neighbor_search_mode");
    input >> neighborSearchMode;

    if (
        !input || boundaryMode < 0 || boundaryMode > 3 ||
        neighborSearchMode < 0 || neighborSearchMode > 1) {
        throw std::runtime_error("Invalid simulation configuration in checkpoint");
    }
    config.boundaryMode = static_cast<BoundaryMode>(boundaryMode);
    config.neighborSearchMode = static_cast<NeighborSearchMode>(neighborSearchMode);
    return config;
}

} // namespace

void CheckpointIO::save(const std::filesystem::path& path, const Simulation& simulation) {
    std::ofstream output(path, std::ios::trunc);
    if (!output) {
        throw std::runtime_error("Cannot open checkpoint for writing: " + path.string());
    }

    output.imbue(std::locale::classic());
    output << std::setprecision(std::numeric_limits<float>::max_digits10);

    const SimulationSnapshot snapshot = simulation.snapshot();
    output << "PARTICLE_LIFE_CHECKPOINT " << kCheckpointVersion << '\n';
    output << "seed " << snapshot.seed << '\n';
    output << "step " << snapshot.step << '\n';
    output << "next_particle_id " << snapshot.nextParticleId << '\n';
    writeConfig(output, snapshot.config);
    output << "rng_state " << std::quoted(snapshot.randomEngineState) << '\n';
    output << "particles " << snapshot.particles.size() << '\n';

    for (const Particle& particle : snapshot.particles) {
        output << particle.id << ' '
               << particle.position.x << ' ' << particle.position.y << ' '
               << particle.velocity.x << ' ' << particle.velocity.y << ' '
               << particle.orientation << ' ' << particle.angularVelocity << ' '
               << particle.force.x << ' ' << particle.force.y << ' '
               << particle.torque << ' ' << static_cast<int>(particle.type) << ' '
               << particle.spawnStep << ' '
               << particle.leftBond << ' ' << particle.rightBond << '\n';
    }

    if (!output) {
        throw std::runtime_error("Failed while writing checkpoint: " + path.string());
    }
}

SimulationSnapshot CheckpointIO::load(const std::filesystem::path& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("Cannot open checkpoint for reading: " + path.string());
    }
    input.imbue(std::locale::classic());

    std::string magic;
    int version = 0;
    input >> magic >> version;
    if (magic != "PARTICLE_LIFE_CHECKPOINT" || (version != 1 && version != 2)) {
        throw std::runtime_error("Unsupported checkpoint format: " + path.string());
    }

    SimulationSnapshot snapshot;
    requireKey(input, "seed");
    input >> snapshot.seed;
    requireKey(input, "step");
    input >> snapshot.step;
    if (version == 2) {
        requireKey(input, "next_particle_id");
        input >> snapshot.nextParticleId;
        snapshot.config = readConfigV2(input);
    } else {
        snapshot.config = readConfigV1(input);
    }
    requireKey(input, "rng_state");
    input >> std::quoted(snapshot.randomEngineState);

    std::size_t particleCount = 0;
    requireKey(input, "particles");
    input >> particleCount;
    snapshot.particles.resize(particleCount);

    ParticleId assignedId = 1;
    for (Particle& particle : snapshot.particles) {
        int particleType = 0;
        if (version == 2) {
            input >> particle.id
                  >> particle.position.x >> particle.position.y
                  >> particle.velocity.x >> particle.velocity.y
                  >> particle.orientation >> particle.angularVelocity
                  >> particle.force.x >> particle.force.y
                  >> particle.torque >> particleType >> particle.spawnStep
                  >> particle.leftBond >> particle.rightBond;
        } else {
            particle.id = assignedId++;
            input >> particle.position.x >> particle.position.y
                  >> particle.velocity.x >> particle.velocity.y
                  >> particle.orientation >> particle.angularVelocity
                  >> particle.force.x >> particle.force.y
                  >> particle.torque >> particleType >> particle.spawnStep;
            particle.leftBond = kInvalidParticleId;
            particle.rightBond = kInvalidParticleId;
        }

        const int maximumParticleType = version == 2 ? 5 : 4;
        if (!input || particleType < 0 || particleType > maximumParticleType) {
            throw std::runtime_error("Invalid particle record in checkpoint");
        }
        particle.type = static_cast<ParticleType>(particleType);
        snapshot.nextParticleId = std::max(snapshot.nextParticleId, particle.id + 1U);
    }

    snapshot.nextParticleId = std::max<ParticleId>(snapshot.nextParticleId, 1U);
    return snapshot;
}

} // namespace particle_life
