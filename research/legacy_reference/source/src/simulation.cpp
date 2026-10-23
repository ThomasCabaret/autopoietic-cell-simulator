#include "particle_life/simulation.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <utility>

namespace particle_life {
namespace {

using ParticleIndex = std::unordered_map<ParticleId, std::size_t>;

ParticleIndex buildParticleIndex(const std::vector<Particle>& particles) {
    ParticleIndex result;
    result.reserve(particles.size());
    for (std::size_t index = 0; index < particles.size(); ++index) {
        result.emplace(particles[index].id, index);
    }
    return result;
}

Vec2 patchTangent(const Particle& particle) noexcept {
    return unitVectorFromAngle(
        particle.orientation + static_cast<float>(kPi) / 2.0f);
}

float safePositive(float value) noexcept {
    return std::max(value, std::numeric_limits<float>::epsilon());
}

} // namespace

Simulation::Simulation(SimulationConfig config, std::uint32_t seed)
    : config_(config),
      seed_(seed),
      randomEngine_(seed),
      spatialGrid_(std::max(config.interactionRadius, std::numeric_limits<float>::epsilon())) {}

SimulationConfig& Simulation::config() noexcept {
    return config_;
}

const SimulationConfig& Simulation::config() const noexcept {
    return config_;
}

std::uint32_t Simulation::seed() const noexcept {
    return seed_;
}

std::uint64_t Simulation::stepIndex() const noexcept {
    return step_;
}

const std::vector<Particle>& Simulation::particles() const noexcept {
    return particles_;
}

std::vector<Particle>& Simulation::particles() noexcept {
    return particles_;
}

void Simulation::clearParticles() noexcept {
    particles_.clear();
}

void Simulation::reset(std::uint32_t seed) {
    seed_ = seed;
    randomEngine_.seed(seed_);
    step_ = 0;
    nextParticleId_ = 1;
    particles_.clear();
}

std::size_t Simulation::spawn(ParticleType type, Vec2 origin) {
    std::uniform_real_distribution<double> positionX(
        -static_cast<double>(config_.worldWidth) / 2.0,
        static_cast<double>(config_.worldWidth) / 2.0);
    std::uniform_real_distribution<double> positionY(
        -static_cast<double>(config_.worldHeight) / 2.0,
        static_cast<double>(config_.worldHeight) / 2.0);
    std::uniform_real_distribution<double> velocity(-0.5, 0.5);
    std::uniform_real_distribution<double> orientation(0.0, 2.0 * kPi);

    Particle particle;
    particle.id = nextParticleId_++;
    particle.position = {
        static_cast<float>(positionX(randomEngine_)),
        static_cast<float>(positionY(randomEngine_))
    };
    particle.position += origin;
    particle.velocity = {
        static_cast<float>(velocity(randomEngine_)),
        static_cast<float>(velocity(randomEngine_))
    };
    particle.orientation = static_cast<float>(orientation(randomEngine_));
    particle.angularVelocity = 0.0f;
    particle.force = {};
    particle.torque = 0.0f;
    particle.type = type;
    particle.spawnStep = step_;
    particle.leftBond = kInvalidParticleId;
    particle.rightBond = kInvalidParticleId;

    particles_.push_back(particle);
    return particles_.size() - 1U;
}

void Simulation::spawnMany(ParticleType type, std::size_t count, Vec2 origin) {
    particles_.reserve(particles_.size() + count);
    for (std::size_t index = 0; index < count; ++index) {
        spawn(type, origin);
    }
}

std::size_t Simulation::patchBondCount() const noexcept {
    return static_cast<std::size_t>(std::count_if(
        particles_.begin(),
        particles_.end(),
        [](const Particle& particle) {
            return particle.type == ParticleType::P &&
                   particle.rightBond != kInvalidParticleId;
        }));
}

void Simulation::breakAllPatchBonds() noexcept {
    for (Particle& particle : particles_) {
        particle.leftBond = kInvalidParticleId;
        particle.rightBond = kInvalidParticleId;
    }
}

void Simulation::calculateSurfactantForceAndTorque(
    Particle& particle,
    Particle& other,
    const Vec2& displacement,
    float distance,
    Vec2& outputForce,
    float& outputTorque) {
    const float orientation1 = particle.orientation;
    const float orientation2 = other.orientation;

    const float theta = wrapAngle(orientation2 - orientation1);
    const float phi = wrapAngle(angleFromVector(displacement) - orientation1);
    const float antiPhi = wrapAngle(angleFromVector(-displacement) - orientation2);

    const float opposition = std::max(std::abs(phi), std::abs(antiPhi));

    float anisotropyFactor = 1.0f;
    constexpr float oppositionTransitionHalfWidth = 0.1f;
    if (opposition < config_.oppositionThreshold - oppositionTransitionHalfWidth) {
        anisotropyFactor = -1.0f;
    } else if (opposition < config_.oppositionThreshold + oppositionTransitionHalfWidth) {
        anisotropyFactor =
            ((opposition - (config_.oppositionThreshold - oppositionTransitionHalfWidth)) /
             (2.0f * oppositionTransitionHalfWidth)) *
                2.0f -
            1.0f;
    }

    const float rotatorFactor = std::sin(2.0f * phi - theta + static_cast<float>(kPi));
    const float distanceFactor = 1.0f / std::pow(distance, config_.surfactantForceExponent);

    outputForce =
        rotateVector(displacement, rotatorFactor) *
        (10.0f * rotatorFactor * rotatorFactor + 1.0f) *
        config_.surfactantForceStrength * anisotropyFactor * distanceFactor;

    const float middle = static_cast<float>(middleAngle(orientation1, orientation2));
    const bool isLeft =
        dot(displacement, rotateVector(unitVectorFromAngle(middle), -static_cast<float>(kPi) / 2.0f)) > 0.0f;

    float leftTargetOffset = wrapAngle((-theta - config_.divisionAngle) / 2.0f);
    float rightTargetOffset = wrapAngle((-theta + config_.divisionAngle) / 2.0f);

    const float directionFactor =
        ((isLeft && leftTargetOffset < 0.0f) || (!isLeft && rightTargetOffset < 0.0f)) ? 1.0f : -1.0f;
    outputTorque = directionFactor * config_.surfactantTorqueStrength;
    outputTorque /= distance;

    outputForce +=
        ((particle.velocity + other.velocity) / 2.0f - particle.velocity) *
        config_.surfactantForceViscosity;
    outputTorque +=
        ((particle.angularVelocity + other.angularVelocity) / 2.0f - particle.angularVelocity) *
        config_.surfactantTorqueViscosity;
}

Vec2 Simulation::displacementBetween(const Vec2& from, const Vec2& to) const noexcept {
    Vec2 displacement = to - from;
    if (config_.boundaryMode != BoundaryMode::Wrap) {
        return displacement;
    }

    const float width = static_cast<float>(config_.worldWidth);
    const float height = static_cast<float>(config_.worldHeight);
    if (width > 0.0f) {
        displacement.x -= std::round(displacement.x / width) * width;
    }
    if (height > 0.0f) {
        displacement.y -= std::round(displacement.y / height) * height;
    }
    return displacement;
}

void Simulation::collectCandidates(
    std::size_t particleIndex,
    float searchRadius,
    std::vector<std::size_t>& output) const {
    if (config_.neighborSearchMode == NeighborSearchMode::BruteForce) {
        output.resize(particles_.size());
        std::iota(output.begin(), output.end(), std::size_t{0});
        return;
    }

    const Vec2 position = particles_[particleIndex].position;
    spatialGrid_.queryCandidateIndices(position, output);

    if (config_.boundaryMode == BoundaryMode::Wrap) {
        const float width = static_cast<float>(config_.worldWidth);
        const float height = static_cast<float>(config_.worldHeight);
        const float halfWidth = width / 2.0f;
        const float halfHeight = height / 2.0f;

        std::vector<float> xShifts{0.0f};
        std::vector<float> yShifts{0.0f};
        if (position.x - (-halfWidth) < searchRadius) {
            xShifts.push_back(width);
        }
        if (halfWidth - position.x < searchRadius) {
            xShifts.push_back(-width);
        }
        if (position.y - (-halfHeight) < searchRadius) {
            yShifts.push_back(height);
        }
        if (halfHeight - position.y < searchRadius) {
            yShifts.push_back(-height);
        }

        std::vector<std::size_t> periodicCandidates;
        for (const float shiftX : xShifts) {
            for (const float shiftY : yShifts) {
                if (shiftX == 0.0f && shiftY == 0.0f) {
                    continue;
                }
                spatialGrid_.queryCandidateIndices(
                    {position.x + shiftX, position.y + shiftY},
                    periodicCandidates);
                output.insert(
                    output.end(),
                    periodicCandidates.begin(),
                    periodicCandidates.end());
            }
        }
        std::sort(output.begin(), output.end());
        output.erase(std::unique(output.begin(), output.end()), output.end());
    }
}

void Simulation::compactActiveParticles(const std::vector<std::uint8_t>& active) {
    std::size_t outputIndex = 0;
    for (std::size_t inputIndex = 0; inputIndex < particles_.size(); ++inputIndex) {
        if (active[inputIndex] == 0U) {
            continue;
        }
        if (outputIndex != inputIndex) {
            particles_[outputIndex] = std::move(particles_[inputIndex]);
        }
        ++outputIndex;
    }
    particles_.resize(outputIndex);
}

void Simulation::repairPatchBondConsistency() {
    std::unordered_set<ParticleId> usedIds;
    usedIds.reserve(particles_.size());
    for (Particle& particle : particles_) {
        if (particle.id == kInvalidParticleId || !usedIds.insert(particle.id).second) {
            particle.id = nextParticleId_++;
            particle.leftBond = kInvalidParticleId;
            particle.rightBond = kInvalidParticleId;
            usedIds.insert(particle.id);
        } else {
            nextParticleId_ = std::max(nextParticleId_, particle.id + 1U);
        }
        if (particle.type != ParticleType::P) {
            particle.leftBond = kInvalidParticleId;
            particle.rightBond = kInvalidParticleId;
        }
    }

    const ParticleIndex particleIndex = buildParticleIndex(particles_);
    for (Particle& particle : particles_) {
        if (particle.type != ParticleType::P) {
            continue;
        }

        if (particle.leftBond != kInvalidParticleId) {
            const auto partnerIterator = particleIndex.find(particle.leftBond);
            if (
                partnerIterator == particleIndex.end() ||
                particles_[partnerIterator->second].type != ParticleType::P ||
                particles_[partnerIterator->second].rightBond != particle.id) {
                particle.leftBond = kInvalidParticleId;
            }
        }
        if (particle.rightBond != kInvalidParticleId) {
            const auto partnerIterator = particleIndex.find(particle.rightBond);
            if (
                partnerIterator == particleIndex.end() ||
                particles_[partnerIterator->second].type != ParticleType::P ||
                particles_[partnerIterator->second].leftBond != particle.id) {
                particle.rightBond = kInvalidParticleId;
            }
        }
    }
}

void Simulation::updatePatchBonds() {
    repairPatchBondConsistency();
    ParticleIndex particleIndex = buildParticleIndex(particles_);
    const PatchParticleConfig& patch = config_.patch;
    const float halfBondLength = patch.bondLength / 2.0f;

    std::uniform_real_distribution<float> unitRandom(0.0f, 1.0f);
    const float thermalBreakProbability =
        patch.temperature > 0.0f && patch.thermalBreakRate > 0.0f && config_.dt > 0.0f
            ? 1.0f - std::exp(-patch.temperature * patch.thermalBreakRate * config_.dt)
            : 0.0f;

    // Existing bonds are checked directly by stable particle id. The spatial
    // grid is not involved in keeping a bond alive.
    for (Particle& particle : particles_) {
        if (particle.type != ParticleType::P || particle.rightBond == kInvalidParticleId) {
            continue;
        }
        const auto partnerIterator = particleIndex.find(particle.rightBond);
        if (partnerIterator == particleIndex.end()) {
            particle.rightBond = kInvalidParticleId;
            continue;
        }

        Particle& partner = particles_[partnerIterator->second];
        const Vec2 centerDisplacement = displacementBetween(particle.position, partner.position);
        const Vec2 siteError =
            centerDisplacement -
            halfBondLength * (patchTangent(particle) + patchTangent(partner));
        const float angularError = std::abs(wrapAngle(
            partner.orientation - particle.orientation - patch.preferredTurnAngle));

        const bool mechanicallyBroken =
            norm(siteError) > patch.breakDistance || angularError > patch.breakAngle;
        const bool thermallyBroken =
            thermalBreakProbability > 0.0f && unitRandom(randomEngine_) < thermalBreakProbability;
        if (mechanicallyBroken || thermallyBroken) {
            particle.rightBond = kInvalidParticleId;
            if (partner.leftBond == particle.id) {
                partner.leftBond = kInvalidParticleId;
            }
        }
    }

    // First-arrived/first-served local association. Each nearby unordered pair
    // is considered once, and either i.right-j.left or j.right-i.left may bind.
    const float formationSearchRadius = patch.bondLength + patch.captureRadius;
    std::vector<std::size_t> candidates;
    for (std::size_t particleIndexValue = 0; particleIndexValue < particles_.size(); ++particleIndexValue) {
        Particle& particle = particles_[particleIndexValue];
        if (
            particle.type != ParticleType::P ||
            (particle.leftBond != kInvalidParticleId && particle.rightBond != kInvalidParticleId)) {
            continue;
        }

        collectCandidates(particleIndexValue, formationSearchRadius, candidates);
        for (const std::size_t otherIndex : candidates) {
            if (otherIndex <= particleIndexValue) {
                continue;
            }
            Particle& other = particles_[otherIndex];
            if (other.type != ParticleType::P) {
                continue;
            }

            const Vec2 centerDisplacement = displacementBetween(particle.position, other.position);
            if (normSquared(centerDisplacement) > formationSearchRadius * formationSearchRadius) {
                continue;
            }

            const Vec2 tangent = patchTangent(particle);
            const Vec2 otherTangent = patchTangent(other);
            const float angleScale = safePositive(patch.captureAngle);
            const float distanceScale = safePositive(patch.captureRadius);

            bool rightLeftValid = false;
            float rightLeftScore = std::numeric_limits<float>::infinity();
            if (
                particle.rightBond == kInvalidParticleId &&
                other.leftBond == kInvalidParticleId &&
                dot(centerDisplacement, tangent) > 0.0f &&
                dot(centerDisplacement, otherTangent) > 0.0f) {
                const Vec2 siteError =
                    centerDisplacement - halfBondLength * (tangent + otherTangent);
                const float siteDistance = norm(siteError);
                const float angularError = std::abs(wrapAngle(
                    other.orientation - particle.orientation - patch.preferredTurnAngle));
                rightLeftValid =
                    siteDistance <= patch.captureRadius && angularError <= patch.captureAngle;
                if (rightLeftValid) {
                    rightLeftScore =
                        siteDistance / distanceScale + angularError / angleScale;
                }
            }

            bool leftRightValid = false;
            float leftRightScore = std::numeric_limits<float>::infinity();
            if (
                particle.leftBond == kInvalidParticleId &&
                other.rightBond == kInvalidParticleId &&
                dot(centerDisplacement, tangent) < 0.0f &&
                dot(centerDisplacement, otherTangent) < 0.0f) {
                const Vec2 siteError =
                    -centerDisplacement - halfBondLength * (tangent + otherTangent);
                const float siteDistance = norm(siteError);
                const float angularError = std::abs(wrapAngle(
                    particle.orientation - other.orientation - patch.preferredTurnAngle));
                leftRightValid =
                    siteDistance <= patch.captureRadius && angularError <= patch.captureAngle;
                if (leftRightValid) {
                    leftRightScore =
                        siteDistance / distanceScale + angularError / angleScale;
                }
            }

            if (rightLeftValid && rightLeftScore <= leftRightScore) {
                particle.rightBond = other.id;
                other.leftBond = particle.id;
            } else if (leftRightValid) {
                particle.leftBond = other.id;
                other.rightBond = particle.id;
            }

            if (
                particle.leftBond != kInvalidParticleId &&
                particle.rightBond != kInvalidParticleId) {
                break;
            }
        }
    }
}

void Simulation::applyPatchBondForces() {
    const ParticleIndex particleIndex = buildParticleIndex(particles_);
    const PatchParticleConfig& patch = config_.patch;
    const float halfBondLength = patch.bondLength / 2.0f;

    for (Particle& particle : particles_) {
        if (particle.type != ParticleType::P || particle.rightBond == kInvalidParticleId) {
            continue;
        }
        const auto partnerIterator = particleIndex.find(particle.rightBond);
        if (partnerIterator == particleIndex.end()) {
            continue;
        }
        Particle& partner = particles_[partnerIterator->second];

        const Vec2 tangent = patchTangent(particle);
        const Vec2 partnerTangent = patchTangent(partner);
        const Vec2 centerDisplacement = displacementBetween(particle.position, partner.position);
        const Vec2 siteError =
            centerDisplacement - halfBondLength * (tangent + partnerTangent);
        const Vec2 relativeVelocity = partner.velocity - particle.velocity;
        const Vec2 force =
            patch.bondStiffness * siteError + patch.bondDamping * relativeVelocity;

        particle.force += force;
        partner.force -= force;

        const Vec2 particleLever = halfBondLength * tangent;
        const Vec2 partnerLever = -halfBondLength * partnerTangent;
        particle.torque += cross(particleLever, force);
        partner.torque += cross(partnerLever, -force);

        const float angularError = wrapAngle(
            partner.orientation - particle.orientation - patch.preferredTurnAngle);
        const float angularTorque =
            patch.bendingStiffness * angularError +
            patch.bondDamping * (partner.angularVelocity - particle.angularVelocity);
        particle.torque += angularTorque;
        partner.torque -= angularTorque;
    }
}

void Simulation::applyPatchCoreRepulsion() {
    const PatchParticleConfig& patch = config_.patch;
    if (patch.coreRepulsionRadius <= 0.0f || patch.coreRepulsionStrength <= 0.0f) {
        return;
    }

    std::vector<std::size_t> candidates;
    for (std::size_t particleIndex = 0; particleIndex < particles_.size(); ++particleIndex) {
        Particle& particle = particles_[particleIndex];
        if (particle.type != ParticleType::P) {
            continue;
        }
        collectCandidates(particleIndex, patch.coreRepulsionRadius, candidates);
        for (const std::size_t otherIndex : candidates) {
            if (otherIndex <= particleIndex || particles_[otherIndex].type != ParticleType::P) {
                continue;
            }

            Particle& other = particles_[otherIndex];
            Vec2 displacement = displacementBetween(particle.position, other.position);
            float distance = norm(displacement);
            if (distance >= patch.coreRepulsionRadius) {
                continue;
            }
            if (distance == 0.0f) {
                displacement = {1.0f, 0.0f};
                distance = 1.0f;
            }

            const float magnitude =
                patch.coreRepulsionStrength *
                (1.0f - distance / patch.coreRepulsionRadius);
            const Vec2 force = displacement * (magnitude / distance);
            particle.force -= force;
            other.force += force;
        }
    }
}

void Simulation::applyPostIntegrationBoundary(Particle& particle) const noexcept {
    const float halfWidth = static_cast<float>(config_.worldWidth) / 2.0f;
    const float halfHeight = static_cast<float>(config_.worldHeight) / 2.0f;

    if (config_.boundaryMode == BoundaryMode::Wrap) {
        const float width = static_cast<float>(config_.worldWidth);
        const float height = static_cast<float>(config_.worldHeight);
        if (width > 0.0f) {
            while (particle.position.x >= halfWidth) {
                particle.position.x -= width;
            }
            while (particle.position.x < -halfWidth) {
                particle.position.x += width;
            }
        }
        if (height > 0.0f) {
            while (particle.position.y >= halfHeight) {
                particle.position.y -= height;
            }
            while (particle.position.y < -halfHeight) {
                particle.position.y += height;
            }
        }
    } else if (config_.boundaryMode == BoundaryMode::Reflect) {
        while (particle.position.x > halfWidth || particle.position.x < -halfWidth) {
            if (particle.position.x > halfWidth) {
                particle.position.x = halfWidth - (particle.position.x - halfWidth);
                particle.velocity.x = -std::abs(particle.velocity.x);
            } else if (particle.position.x < -halfWidth) {
                particle.position.x = -halfWidth + (-halfWidth - particle.position.x);
                particle.velocity.x = std::abs(particle.velocity.x);
            }
        }
        while (particle.position.y > halfHeight || particle.position.y < -halfHeight) {
            if (particle.position.y > halfHeight) {
                particle.position.y = halfHeight - (particle.position.y - halfHeight);
                particle.velocity.y = -std::abs(particle.velocity.y);
            } else if (particle.position.y < -halfHeight) {
                particle.position.y = -halfHeight + (-halfHeight - particle.position.y);
                particle.velocity.y = std::abs(particle.velocity.y);
            }
        }
    }
}

void Simulation::step() {
    ++step_;

    const float patchFormationRadius =
        config_.patch.bondLength + config_.patch.captureRadius;
    const float gridCellSize = std::max({
        config_.interactionRadius,
        patchFormationRadius,
        config_.patch.coreRepulsionRadius,
        std::numeric_limits<float>::epsilon()
    });
    spatialGrid_.setCellSize(gridCellSize);
    spatialGrid_.rebuild(particles_);

    updatePatchBonds();

    for (Particle& particle : particles_) {
        particle.force = {};
        particle.torque = 0.0f;
    }

    applyPatchBondForces();
    applyPatchCoreRepulsion();

    std::vector<std::uint8_t> active(particles_.size(), 1U);
    std::vector<std::size_t> candidates;

    for (std::size_t particleIndex = 0; particleIndex < particles_.size(); ++particleIndex) {
        if (active[particleIndex] == 0U) {
            continue;
        }

        Particle& particle = particles_[particleIndex];
        collectCandidates(particleIndex, config_.interactionRadius, candidates);
        for (const std::size_t otherIndex : candidates) {
            if (otherIndex == particleIndex || active[otherIndex] == 0U) {
                continue;
            }

            Particle& other = particles_[otherIndex];
            const Vec2 displacement = displacementBetween(particle.position, other.position);
            const float distance = norm(displacement);
            if (distance == 0.0f) {
                continue;
            }

            Vec2 force;
            float torque = 0.0f;

            if (particle.type == ParticleType::S && other.type == ParticleType::S) {
                if (distance < config_.interactionRadius) {
                    calculateSurfactantForceAndTorque(
                        particle,
                        other,
                        displacement,
                        distance,
                        force,
                        torque);
                    particle.force += force;
                    particle.torque += torque;

                    if (distance < 4.0f * config_.dotSize) {
                        const float factor = std::pow(2.0f * config_.dotSize / distance, 9.0f);
                        particle.force += -displacement * factor;
                    }
                }
            } else if (
                (particle.type == ParticleType::S &&
                 (other.type == ParticleType::A || other.type == ParticleType::B ||
                  other.type == ParticleType::L)) ||
                (other.type == ParticleType::S &&
                 (particle.type == ParticleType::A || particle.type == ParticleType::B ||
                  particle.type == ParticleType::L))) {
                if (distance < config_.interactionRadius) {
                    const float factor = std::pow(2.0f * config_.dotSize / distance, 6.0f);
                    particle.force +=
                        -displacement * factor *
                        (particle.type != ParticleType::S ? 10.0f : 0.001f);
                    particle.force += force;
                }
            } else if (
                (particle.type == ParticleType::A && other.type == ParticleType::F) ||
                (other.type == ParticleType::A && particle.type == ParticleType::F)) {
                if (distance < config_.interactionRadius / 2.0f) {
                    if (particle.type == ParticleType::F) {
                        particle.type = ParticleType::B;
                        particle.spawnStep = step_;
                    }
                    if (other.type == ParticleType::F) {
                        other.type = ParticleType::B;
                        other.spawnStep = step_;
                    }
                }
            } else if (
                (particle.type == ParticleType::B && other.type == ParticleType::F) ||
                (other.type == ParticleType::B && particle.type == ParticleType::F)) {
                if (distance < config_.interactionRadius / 2.0f) {
                    particle.type = ParticleType::A;
                    other.type = ParticleType::S;
                    particle.spawnStep = step_;
                    other.spawnStep = step_;
                }
            } else if (
                (particle.type == ParticleType::L && other.type == ParticleType::A) ||
                (other.type == ParticleType::A && particle.type == ParticleType::L)) {
                // Kept deliberately identical to the prototype, including its
                // first-arrived/first-served orientation dependence.
                if (distance < config_.interactionRadius / 2.0f) {
                    particle.type = ParticleType::F;
                    other.type = ParticleType::L;
                    particle.spawnStep = step_;
                    other.spawnStep = step_;
                }
            }
        }

        const float halfWidth = static_cast<float>(config_.worldWidth) / 2.0f;
        const float halfHeight = static_cast<float>(config_.worldHeight) / 2.0f;
        if (config_.boundaryMode == BoundaryMode::Destroy) {
            if (
                particle.position.x > halfWidth || particle.position.x < -halfWidth ||
                particle.position.y > halfHeight || particle.position.y < -halfHeight) {
                active[particleIndex] = 0U;
                continue;
            }
        } else if (config_.boundaryMode == BoundaryMode::LegacyContainment) {
            if (particle.position.x > halfWidth) {
                particle.force += {-config_.containingForce, 0.0f};
            }
            if (particle.position.x < -halfWidth) {
                particle.force += {config_.containingForce, 0.0f};
            }
            if (particle.position.y > halfHeight) {
                particle.force += {0.0f, -config_.containingForce};
            }
            if (particle.position.y < -halfHeight) {
                particle.force += {0.0f, config_.containingForce};
            }
        }

        if (particle.type == ParticleType::P) {
            if (config_.patch.temperature > 0.0f) {
                std::uniform_real_distribution<float> thermal(-1.0f, 1.0f);
                particle.force += config_.patch.temperature * Vec2{
                    thermal(randomEngine_), thermal(randomEngine_)};
                particle.torque += config_.patch.temperature * thermal(randomEngine_);
            }
        } else if (particle.type == ParticleType::S) {
            if (norm(particle.velocity) <= config_.brownianSpeed) {
                particle.force += 0.01f * particle.velocity / config_.dt;
            }
        } else {
            if (norm(particle.velocity) <= 1.0f) {
                particle.force += 0.01f * particle.velocity / config_.dt;
            }
            std::uniform_real_distribution<double> brownian(-0.01, 0.01);
            particle.force += {
                static_cast<float>(brownian(randomEngine_)),
                static_cast<float>(brownian(randomEngine_))
            };
        }
    }

    compactActiveParticles(active);
    repairPatchBondConsistency();

    for (Particle& particle : particles_) {
        const Vec2 acceleration = particle.force;
        const float angularAcceleration = particle.torque;

        particle.velocity += acceleration * config_.dt;
        particle.angularVelocity += angularAcceleration * config_.dt;

        constexpr float maximumVelocity = 2.0f;
        if (norm(particle.velocity) > maximumVelocity) {
            normalize(particle.velocity);
            particle.velocity *= maximumVelocity;
        }

        constexpr float maximumAngularVelocity = 10.0f;
        if (particle.angularVelocity > maximumAngularVelocity) {
            particle.angularVelocity = maximumAngularVelocity;
        }
        if (particle.angularVelocity < -maximumAngularVelocity) {
            particle.angularVelocity = -maximumAngularVelocity;
        }

        if (config_.centerize) {
            particle.velocity -= config_.centerForce * particle.position;
        }

        particle.velocity *= config_.voidViscosity;
        particle.angularVelocity *= config_.voidTorqueViscosity;

        particle.position += particle.velocity * config_.dt;
        particle.orientation += particle.angularVelocity * config_.dt;
        applyPostIntegrationBoundary(particle);
    }
}

void Simulation::runSteps(std::uint64_t count) {
    for (std::uint64_t index = 0; index < count; ++index) {
        step();
    }
}

SimulationSnapshot Simulation::snapshot() const {
    std::ostringstream randomState;
    randomState << randomEngine_;

    SimulationSnapshot result;
    result.config = config_;
    result.seed = seed_;
    result.step = step_;
    result.nextParticleId = nextParticleId_;
    result.randomEngineState = randomState.str();
    result.particles = particles_;
    return result;
}

void Simulation::restore(const SimulationSnapshot& snapshot) {
    config_ = snapshot.config;
    seed_ = snapshot.seed;
    step_ = snapshot.step;
    nextParticleId_ = std::max<ParticleId>(snapshot.nextParticleId, 1U);
    particles_ = snapshot.particles;

    if (snapshot.randomEngineState.empty()) {
        randomEngine_.seed(seed_);
    } else {
        std::istringstream randomState(snapshot.randomEngineState);
        randomState >> randomEngine_;
        if (!randomState) {
            throw std::runtime_error("Invalid random engine state in checkpoint");
        }
    }
    repairPatchBondConsistency();
}

} // namespace particle_life
