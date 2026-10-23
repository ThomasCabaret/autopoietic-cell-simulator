#include "particle_life/template_copy.hpp"

#include <algorithm>
#include <cmath>
#include <deque>
#include <map>
#include <stdexcept>
#include <utility>

namespace particle_life::template_copy {
namespace {

constexpr float kEpsilon = 1.0e-6f;

float clampMagnitude(float value, float maximum) noexcept {
    return std::clamp(value, -maximum, maximum);
}

Symbol symbolFromCharacter(char character) {
    if (character == '0') {
        return Symbol::Zero;
    }
    if (character == '1') {
        return Symbol::One;
    }
    throw std::invalid_argument("Template sequence must contain only 0 and 1");
}

char characterFromSymbol(Symbol symbol) noexcept {
    return symbol == Symbol::Zero ? '0' : '1';
}

} // namespace

bool isValidSequence(const std::string& sequence) noexcept {
    if (sequence.size() < 2 || sequence.size() > 32) {
        return false;
    }
    return std::all_of(sequence.begin(), sequence.end(), [](char character) {
        return character == '0' || character == '1';
    });
}

const char* phaseName(CyclePhase phase) noexcept {
    return phase == CyclePhase::Capture ? "Capture / ligation" : "Release";
}

Model::Model(std::uint32_t seed)
    : random_(seed) {
}

void Model::setSeed(std::uint32_t seed) {
    random_.seed(seed);
}

void Model::reset(const std::string& sequence, int freeZeroCount, int freeOneCount) {
    if (!isValidSequence(sequence)) {
        throw std::invalid_argument("Template sequence must contain 2 to 32 binary symbols");
    }

    clear();
    targetSequence_ = sequence;
    spawnTemplate(sequence);
    spawnFreeMonomers(Symbol::Zero, std::max(0, freeZeroCount));
    spawnFreeMonomers(Symbol::One, std::max(0, freeOneCount));
}

void Model::clear() {
    particles_.clear();
    stepCount_ = 0;
    simulationTime_ = 0.0;
    phase_ = CyclePhase::Capture;
    phaseElapsed_ = 0.0f;
}

void Model::spawnTemplate(const std::string& sequence, Vec2 center) {
    if (!isValidSequence(sequence)) {
        throw std::invalid_argument("Template sequence must contain 2 to 32 binary symbols");
    }

    const float totalLength = static_cast<float>(sequence.size() - 1) * config_.backboneRestLength;
    const float startX = center.x - totalLength * 0.5f;
    ParticleId previous = kInvalidParticleId;

    for (std::size_t index = 0; index < sequence.size(); ++index) {
        const Vec2 position = {
            startX + static_cast<float>(index) * config_.backboneRestLength,
            center.y
        };
        const ParticleId current = addParticle(symbolFromCharacter(sequence[index]), position, 0.0f);
        if (previous != kInvalidParticleId) {
            createBackboneBond(previous, current);
        }
        previous = current;
    }
}

void Model::spawnFreeMonomers(Symbol symbol, int count) {
    const float halfWidth = config_.worldWidth * 0.5f;
    const float halfHeight = config_.worldHeight * 0.5f;
    std::uniform_real_distribution<float> xDistribution(-halfWidth, halfWidth);
    std::uniform_real_distribution<float> yDistribution(-halfHeight, halfHeight);
    std::uniform_real_distribution<float> angleDistribution(-static_cast<float>(kPi), static_cast<float>(kPi));

    for (int index = 0; index < count; ++index) {
        addParticle(symbol, {xDistribution(random_), yDistribution(random_)}, angleDistribution(random_));
    }
}

void Model::spawnFreeMonomer(Symbol symbol, Vec2 position) {
    std::uniform_real_distribution<float> angleDistribution(-static_cast<float>(kPi), static_cast<float>(kPi));
    addParticle(symbol, wrappedPosition(position), angleDistribution(random_));
}

void Model::setAutomaticCycle(bool enabled) noexcept {
    config_.automaticCycle = enabled;
}

void Model::forcePhase(CyclePhase phase) noexcept {
    phase_ = phase;
    phaseElapsed_ = 0.0f;
}

float Model::phaseTimeRemaining() const noexcept {
    const float duration = phase_ == CyclePhase::Capture
        ? std::max(config_.captureDuration, config_.dt)
        : std::max(config_.releaseDuration, config_.dt);
    return std::max(0.0f, duration - phaseElapsed_);
}

bool Model::isValidId(ParticleId id) const noexcept {
    return id != kInvalidParticleId && id < particles_.size();
}

int Model::backboneDegree(const Particle& particle) const noexcept {
    return (particle.left != kInvalidParticleId ? 1 : 0)
        + (particle.right != kInvalidParticleId ? 1 : 0);
}

Vec2 Model::displacement(const Vec2& from, const Vec2& to) const noexcept {
    Vec2 result = to - from;
    if (config_.boundaryMode == BoundaryMode::Wrap) {
        if (config_.worldWidth > 0.0f) {
            result.x -= std::round(result.x / config_.worldWidth) * config_.worldWidth;
        }
        if (config_.worldHeight > 0.0f) {
            result.y -= std::round(result.y / config_.worldHeight) * config_.worldHeight;
        }
    }
    return result;
}

Vec2 Model::wrappedPosition(Vec2 position) const noexcept {
    if (config_.boundaryMode != BoundaryMode::Wrap) {
        return position;
    }

    const float halfWidth = config_.worldWidth * 0.5f;
    const float halfHeight = config_.worldHeight * 0.5f;
    while (position.x >= halfWidth) {
        position.x -= config_.worldWidth;
    }
    while (position.x < -halfWidth) {
        position.x += config_.worldWidth;
    }
    while (position.y >= halfHeight) {
        position.y -= config_.worldHeight;
    }
    while (position.y < -halfHeight) {
        position.y += config_.worldHeight;
    }
    return position;
}

float Model::randomUnit() {
    return unitDistribution_(random_);
}

float Model::eventProbability(float ratePerSecond) const noexcept {
    if (ratePerSecond <= 0.0f || config_.dt <= 0.0f) {
        return 0.0f;
    }
    return 1.0f - std::exp(-ratePerSecond * config_.dt);
}

ParticleId Model::addParticle(Symbol symbol, Vec2 position, float orientation) {
    const ParticleId id = static_cast<ParticleId>(particles_.size());
    Particle particle;
    particle.id = id;
    particle.symbol = symbol;
    particle.position = wrappedPosition(position);
    particle.orientation = wrapAngle(orientation);
    particles_.push_back(particle);
    return id;
}

void Model::createBackboneBond(ParticleId left, ParticleId right) {
    if (!isValidId(left) || !isValidId(right) || left == right) {
        return;
    }
    Particle& leftParticle = particles_[left];
    Particle& rightParticle = particles_[right];
    if (leftParticle.right != kInvalidParticleId || rightParticle.left != kInvalidParticleId) {
        return;
    }
    leftParticle.right = right;
    rightParticle.left = left;
}

void Model::breakBackboneBond(ParticleId left, ParticleId right) {
    if (!isValidId(left) || !isValidId(right)) {
        return;
    }
    if (particles_[left].right == right) {
        particles_[left].right = kInvalidParticleId;
    }
    if (particles_[right].left == left) {
        particles_[right].left = kInvalidParticleId;
    }
}

void Model::createPairBond(ParticleId templateId, ParticleId copyId) {
    if (!isValidId(templateId) || !isValidId(copyId) || templateId == copyId) {
        return;
    }
    Particle& templateParticle = particles_[templateId];
    Particle& copyParticle = particles_[copyId];
    if (templateParticle.pair != kInvalidParticleId || copyParticle.pair != kInvalidParticleId) {
        return;
    }
    templateParticle.pair = copyId;
    templateParticle.pairRole = PairRole::Template;
    copyParticle.pair = templateId;
    copyParticle.pairRole = PairRole::Copy;
}

void Model::breakPairBond(ParticleId first, ParticleId second) {
    if (!isValidId(first) || !isValidId(second)) {
        return;
    }
    if (particles_[first].pair == second) {
        particles_[first].pair = kInvalidParticleId;
        particles_[first].pairRole = PairRole::None;
    }
    if (particles_[second].pair == first) {
        particles_[second].pair = kInvalidParticleId;
        particles_[second].pairRole = PairRole::None;
    }
}

void Model::updateCycle() {
    if (!config_.automaticCycle) {
        return;
    }

    phaseElapsed_ += config_.dt;
    const float duration = phase_ == CyclePhase::Capture
        ? std::max(config_.captureDuration, config_.dt)
        : std::max(config_.releaseDuration, config_.dt);

    if (phaseElapsed_ >= duration) {
        phaseElapsed_ = std::fmod(phaseElapsed_, duration);
        phase_ = phase_ == CyclePhase::Capture ? CyclePhase::Release : CyclePhase::Capture;
    }
}

void Model::resetForces() {
    for (Particle& particle : particles_) {
        particle.force = {};
        particle.torque = 0.0f;
    }
}

void Model::applyNonBondedRepulsion() {
    const float radius = std::max(config_.repulsionRadius, kEpsilon);
    const float radiusSquared = radius * radius;

    for (std::size_t firstIndex = 0; firstIndex < particles_.size(); ++firstIndex) {
        for (std::size_t secondIndex = firstIndex + 1; secondIndex < particles_.size(); ++secondIndex) {
            Particle& first = particles_[firstIndex];
            Particle& second = particles_[secondIndex];
            const Vec2 delta = displacement(first.position, second.position);
            const float distanceSquared = normSquared(delta);
            if (distanceSquared >= radiusSquared) {
                continue;
            }

            const float distance = std::sqrt(std::max(distanceSquared, kEpsilon));
            const Vec2 direction = delta / distance;
            const float overlapFraction = 1.0f - distance / radius;
            const Vec2 force = direction * (config_.repulsionStrength * overlapFraction);
            first.force -= force;
            second.force += force;
        }
    }
}

void Model::applyBackboneForces() {
    std::vector<std::pair<ParticleId, ParticleId>> brokenBonds;

    for (Particle& leftParticle : particles_) {
        if (!isValidId(leftParticle.right)) {
            continue;
        }

        Particle& rightParticle = particles_[leftParticle.right];
        const Vec2 delta = displacement(leftParticle.position, rightParticle.position);
        const float distance = std::max(norm(delta), kEpsilon);
        if (distance > config_.backboneBreakDistance) {
            brokenBonds.emplace_back(leftParticle.id, rightParticle.id);
            continue;
        }

        const Vec2 direction = delta / distance;
        const float stretch = distance - config_.backboneRestLength;
        const float relativeSpeed = dot(rightParticle.velocity - leftParticle.velocity, direction);
        const float magnitude = config_.backboneStrength * stretch
            + config_.backboneDamping * relativeSpeed;
        const Vec2 force = direction * magnitude;
        leftParticle.force += force;
        rightParticle.force -= force;

        const float targetAngle = angleFromVector(delta);
        const float leftError = wrapAngle(targetAngle - leftParticle.orientation);
        const float rightError = wrapAngle(targetAngle - rightParticle.orientation);
        leftParticle.torque += config_.backboneAlignmentStrength * leftError;
        rightParticle.torque += config_.backboneAlignmentStrength * rightError;
    }

    for (const auto& [left, right] : brokenBonds) {
        breakBackboneBond(left, right);
    }
}

void Model::applyPairForcesAndRelease() {
    std::vector<std::pair<ParticleId, ParticleId>> brokenPairs;
    const float releaseProbability = eventProbability(config_.releasePairBreakRate);

    for (Particle& templateParticle : particles_) {
        if (templateParticle.pairRole != PairRole::Template || !isValidId(templateParticle.pair)) {
            continue;
        }

        Particle& copyParticle = particles_[templateParticle.pair];
        const Vec2 directDelta = displacement(templateParticle.position, copyParticle.position);
        const float directDistance = norm(directDelta);
        if (directDistance > config_.pairBreakDistance) {
            brokenPairs.emplace_back(templateParticle.id, copyParticle.id);
            continue;
        }

        if (phase_ == CyclePhase::Release) {
            if (directDistance > kEpsilon) {
                const Vec2 direction = directDelta / directDistance;
                const Vec2 force = direction * config_.releaseRepulsionStrength;
                templateParticle.force -= force;
                copyParticle.force += force;
            }
            if (randomUnit() < releaseProbability) {
                brokenPairs.emplace_back(templateParticle.id, copyParticle.id);
            }
            continue;
        }

        const Vec2 normal = rotateVector(unitVectorFromAngle(templateParticle.orientation), static_cast<float>(kPi * 0.5));
        const Vec2 targetPosition = templateParticle.position + normal * config_.pairDistance;
        const Vec2 targetDelta = displacement(copyParticle.position, targetPosition);
        const float relativeNormalSpeed = dot(copyParticle.velocity - templateParticle.velocity, normal);
        const Vec2 force = targetDelta * config_.pairStrength
            - normal * (config_.pairDamping * relativeNormalSpeed);
        copyParticle.force += force;
        templateParticle.force -= force;

        const float orientationError = wrapAngle(templateParticle.orientation - copyParticle.orientation);
        copyParticle.torque += config_.pairAlignmentStrength * orientationError;
        templateParticle.torque -= config_.pairAlignmentStrength * orientationError;
    }

    for (const auto& [first, second] : brokenPairs) {
        breakPairBond(first, second);
    }
}

void Model::formPairBonds() {
    if (phase_ != CyclePhase::Capture) {
        return;
    }

    const float probability = eventProbability(config_.pairCaptureRate);
    const float radiusSquared = config_.pairCaptureRadius * config_.pairCaptureRadius;

    for (Particle& templateParticle : particles_) {
        if (templateParticle.pair != kInvalidParticleId || backboneDegree(templateParticle) == 0) {
            continue;
        }

        const Vec2 normal = rotateVector(unitVectorFromAngle(templateParticle.orientation), static_cast<float>(kPi * 0.5));
        const Vec2 targetPosition = templateParticle.position + normal * config_.pairDistance;

        ParticleId bestCandidate = kInvalidParticleId;
        float bestDistanceSquared = radiusSquared;
        for (Particle& candidate : particles_) {
            if (candidate.id == templateParticle.id
                || candidate.symbol != templateParticle.symbol
                || candidate.pair != kInvalidParticleId
                || backboneDegree(candidate) != 0) {
                continue;
            }

            const float distanceSquared = normSquared(displacement(targetPosition, candidate.position));
            if (distanceSquared < bestDistanceSquared) {
                bestDistanceSquared = distanceSquared;
                bestCandidate = candidate.id;
            }
        }

        if (bestCandidate != kInvalidParticleId && randomUnit() < probability) {
            createPairBond(templateParticle.id, bestCandidate);
        }
    }
}

void Model::formTemplatedBackboneBonds() {
    if (phase_ != CyclePhase::Capture) {
        return;
    }

    const float probability = eventProbability(config_.ligationRate);
    const float distanceSquaredLimit = config_.ligationDistance * config_.ligationDistance;

    for (Particle& templateLeft : particles_) {
        if (!isValidId(templateLeft.right)
            || templateLeft.pairRole != PairRole::Template
            || !isValidId(templateLeft.pair)) {
            continue;
        }

        Particle& templateRight = particles_[templateLeft.right];
        if (templateRight.pairRole != PairRole::Template || !isValidId(templateRight.pair)) {
            continue;
        }

        Particle& copyLeft = particles_[templateLeft.pair];
        Particle& copyRight = particles_[templateRight.pair];
        if (copyLeft.right != kInvalidParticleId || copyRight.left != kInvalidParticleId) {
            continue;
        }

        const Vec2 delta = displacement(copyLeft.position, copyRight.position);
        if (normSquared(delta) > distanceSquaredLimit) {
            continue;
        }

        const float targetAngle = angleFromVector(delta);
        const float leftError = std::abs(wrapAngle(targetAngle - copyLeft.orientation));
        const float rightError = std::abs(wrapAngle(targetAngle - copyRight.orientation));
        if (leftError > config_.ligationAngleTolerance || rightError > config_.ligationAngleTolerance) {
            continue;
        }

        if (randomUnit() < probability) {
            createBackboneBond(copyLeft.id, copyRight.id);
        }
    }
}

void Model::applyNoise() {
    const float noise = phase_ == CyclePhase::Capture ? config_.captureNoise : config_.releaseNoise;
    if (noise <= 0.0f || config_.dt <= 0.0f) {
        return;
    }

    const float linearScale = noise * std::sqrt(config_.dt);
    const float angularScale = 0.3f * noise * std::sqrt(config_.dt);
    for (Particle& particle : particles_) {
        particle.velocity.x += normalDistribution_(random_) * linearScale;
        particle.velocity.y += normalDistribution_(random_) * linearScale;
        particle.angularVelocity += normalDistribution_(random_) * angularScale;
    }
}

void Model::integrate() {
    for (Particle& particle : particles_) {
        particle.velocity += particle.force * config_.dt;
        particle.angularVelocity += particle.torque * config_.dt;

        const float speed = norm(particle.velocity);
        if (speed > config_.maxSpeed && speed > kEpsilon) {
            particle.velocity *= config_.maxSpeed / speed;
        }
        particle.angularVelocity = clampMagnitude(particle.angularVelocity, config_.maxAngularSpeed);

        particle.velocity *= config_.linearDamping;
        particle.angularVelocity *= config_.angularDamping;
        particle.position += particle.velocity * config_.dt;
        particle.orientation = wrapAngle(particle.orientation + particle.angularVelocity * config_.dt);
        enforceBoundaries(particle);
    }
}

void Model::enforceBoundaries(Particle& particle) {
    if (config_.boundaryMode == BoundaryMode::Wrap) {
        particle.position = wrappedPosition(particle.position);
        return;
    }

    const float halfWidth = config_.worldWidth * 0.5f;
    const float halfHeight = config_.worldHeight * 0.5f;
    if (particle.position.x > halfWidth) {
        particle.position.x = halfWidth;
        particle.velocity.x = -std::abs(particle.velocity.x);
    } else if (particle.position.x < -halfWidth) {
        particle.position.x = -halfWidth;
        particle.velocity.x = std::abs(particle.velocity.x);
    }
    if (particle.position.y > halfHeight) {
        particle.position.y = halfHeight;
        particle.velocity.y = -std::abs(particle.velocity.y);
    } else if (particle.position.y < -halfHeight) {
        particle.position.y = -halfHeight;
        particle.velocity.y = std::abs(particle.velocity.y);
    }
}

void Model::step() {
    updateCycle();
    resetForces();
    applyNonBondedRepulsion();
    applyBackboneForces();
    applyPairForcesAndRelease();
    formPairBonds();
    formTemplatedBackboneBonds();
    applyNoise();
    integrate();
    ++stepCount_;
    simulationTime_ += config_.dt;
}

std::vector<ParticleId> Model::chainComponent(ParticleId start, std::vector<bool>& visited) const {
    std::vector<ParticleId> component;
    std::deque<ParticleId> queue;
    queue.push_back(start);
    visited[start] = true;

    while (!queue.empty()) {
        const ParticleId current = queue.front();
        queue.pop_front();
        component.push_back(current);
        const Particle& particle = particles_[current];
        for (const ParticleId neighbor : {particle.left, particle.right}) {
            if (isValidId(neighbor) && !visited[neighbor]) {
                visited[neighbor] = true;
                queue.push_back(neighbor);
            }
        }
    }
    return component;
}

std::string Model::sequenceForChain(const std::vector<ParticleId>& chain) const {
    if (chain.empty()) {
        return {};
    }

    ParticleId start = kInvalidParticleId;
    for (const ParticleId id : chain) {
        if (particles_[id].left == kInvalidParticleId) {
            start = id;
            break;
        }
    }
    if (start == kInvalidParticleId) {
        return {};
    }

    std::string sequence;
    ParticleId current = start;
    std::size_t guard = 0;
    while (isValidId(current) && guard <= chain.size()) {
        sequence.push_back(characterFromSymbol(particles_[current].symbol));
        current = particles_[current].right;
        ++guard;
    }
    return sequence;
}

std::vector<Model::ChainDescription> Model::describeChains() const {
    std::vector<ChainDescription> descriptions;
    std::vector<bool> visited(particles_.size(), false);
    for (const Particle& particle : particles_) {
        if (visited[particle.id] || backboneDegree(particle) == 0) {
            continue;
        }

        const std::vector<ParticleId> component = chainComponent(particle.id, visited);
        const std::string sequence = sequenceForChain(component);
        if (sequence.empty()) {
            continue;
        }

        const bool detached = std::all_of(
            component.begin(),
            component.end(),
            [this](ParticleId id) {
                return particles_[id].pair == kInvalidParticleId;
            });
        descriptions.push_back({sequence, detached});
    }
    return descriptions;
}

std::vector<std::string> Model::chainSequences() const {
    std::vector<std::string> sequences;
    for (const ChainDescription& description : describeChains()) {
        sequences.push_back(description.sequence);
    }
    return sequences;
}

std::vector<SequenceCensusEntry> Model::sequenceCensus() const {
    std::map<std::string, SequenceCensusEntry> counts;
    for (const ChainDescription& description : describeChains()) {
        SequenceCensusEntry& entry = counts[description.sequence];
        entry.sequence = description.sequence;
        ++entry.totalCount;
        if (description.detached) {
            ++entry.detachedCount;
        }
    }

    std::vector<SequenceCensusEntry> result;
    result.reserve(counts.size());
    for (auto& [sequence, entry] : counts) {
        (void)sequence;
        result.push_back(std::move(entry));
    }

    std::sort(
        result.begin(),
        result.end(),
        [](const SequenceCensusEntry& first, const SequenceCensusEntry& second) {
            if (first.sequence.size() != second.sequence.size()) {
                return first.sequence.size() > second.sequence.size();
            }
            if (first.totalCount != second.totalCount) {
                return first.totalCount > second.totalCount;
            }
            return first.sequence < second.sequence;
        });
    return result;
}

Statistics Model::statistics() const {
    Statistics result;
    result.particleCount = particles_.size();
    result.chainLengthHistogram.resize(targetSequence_.size() + 2, 0);

    for (const Particle& particle : particles_) {
        if (backboneDegree(particle) == 0) {
            ++result.freeMonomerCount;
        }
        if (particle.right != kInvalidParticleId) {
            ++result.backboneBondCount;
        }
        if (particle.pairRole == PairRole::Template) {
            ++result.pairBondCount;
        }
    }

    const std::vector<ChainDescription> chains = describeChains();
    result.chainCount = chains.size();
    for (const ChainDescription& chain : chains) {
        const std::string& sequence = chain.sequence;
        result.longestChainLength = std::max(result.longestChainLength, sequence.size());
        const std::size_t histogramIndex = std::min(sequence.size(), result.chainLengthHistogram.size() - 1);
        ++result.chainLengthHistogram[histogramIndex];
        if (sequence.size() == targetSequence_.size()) {
            ++result.fullLengthChainCount;
        }
        if (sequence == targetSequence_) {
            ++result.exactSequenceCount;
            if (chain.detached) {
                ++result.detachedExactSequenceCount;
            }
        }
    }
    result.exactCopyCount = result.exactSequenceCount > 0 ? result.exactSequenceCount - 1 : 0;
    result.detachedExactCopyCount = result.detachedExactSequenceCount > 0
        ? result.detachedExactSequenceCount - 1
        : 0;
    return result;
}

} // namespace particle_life::template_copy
