#include "particle_life/checkpoint.hpp"
#include "particle_life/experiment.hpp"
#include "particle_life/math.hpp"
#include "particle_life/metrics.hpp"
#include "particle_life/simulation.hpp"

#include "imgui.h"
#include "imgui-SFML.h"
#include <SFML/Graphics.hpp>

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>

namespace {

struct ViewerOptions {
    std::uint32_t seed = 5489u;
    std::filesystem::path loadCheckpoint;
    std::filesystem::path checkpointPath = "particle_life.checkpoint";
    std::filesystem::path metricsPath;
    std::uint64_t metricsEverySteps = 100;
};

struct ViewerState {
    int stepsPerFrame = 10;
    float persistenceSeconds = 0.5f;
    bool drawInteractionRadius = false;
    bool spawnAtMouseLocation = false;
    bool sourceEnabled = false;
    int sourceTypeIndex = 0;
    int patchBatchCount = 200;
    particle_life::Vec2 sourcePosition;
    bool paused = false;
    bool singleStepRequested = false;
};

constexpr std::array<particle_life::ParticleType, 6> kParticleTypes = {
    particle_life::ParticleType::F,
    particle_life::ParticleType::A,
    particle_life::ParticleType::B,
    particle_life::ParticleType::S,
    particle_life::ParticleType::L,
    particle_life::ParticleType::P
};

constexpr std::array<const char*, 6> kParticleTypeNames = {
    "F - food/precursor",
    "A - catalyst",
    "B - intermediary",
    "S - legacy surfactant",
    "L - limiter",
    "P - patch monomer"
};

ViewerOptions parseOptions(int argc, char** argv) {
    ViewerOptions options;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        auto requireValue = [&]() -> const char* {
            if (index + 1 >= argc) {
                throw std::invalid_argument("Missing value after " + argument);
            }
            return argv[++index];
        };

        if (argument == "--seed") {
            options.seed = static_cast<std::uint32_t>(std::stoul(requireValue()));
        } else if (argument == "--load") {
            options.loadCheckpoint = requireValue();
        } else if (argument == "--checkpoint") {
            options.checkpointPath = requireValue();
        } else if (argument == "--metrics") {
            options.metricsPath = requireValue();
        } else if (argument == "--metrics-every") {
            options.metricsEverySteps = std::stoull(requireValue());
        } else {
            throw std::invalid_argument("Unknown argument: " + argument);
        }
    }
    if (!options.metricsPath.empty() && options.metricsEverySteps == 0) {
        throw std::invalid_argument("--metrics-every must be non-zero");
    }
    return options;
}

sf::Vector2f toSf(const particle_life::Vec2& value) {
    return {value.x, value.y};
}

particle_life::Vec2 fromSf(const sf::Vector2f& value) {
    return {value.x, value.y};
}

particle_life::Vec2 displayDisplacement(
    const particle_life::SimulationConfig& config,
    const particle_life::Vec2& from,
    const particle_life::Vec2& to) {
    particle_life::Vec2 displacement = to - from;
    if (config.boundaryMode == particle_life::BoundaryMode::Wrap) {
        const float width = static_cast<float>(config.worldWidth);
        const float height = static_cast<float>(config.worldHeight);
        if (width > 0.0f) {
            displacement.x -= std::round(displacement.x / width) * width;
        }
        if (height > 0.0f) {
            displacement.y -= std::round(displacement.y / height) * height;
        }
    }
    return displacement;
}

sf::Color particleColor(particle_life::ParticleType type) {
    switch (type) {
    case particle_life::ParticleType::F:
        return sf::Color::Green;
    case particle_life::ParticleType::A:
        return sf::Color::Red;
    case particle_life::ParticleType::B:
        return sf::Color::Magenta;
    case particle_life::ParticleType::S:
        return sf::Color(255, 200, 0);
    case particle_life::ParticleType::L:
        return sf::Color(27, 227, 243);
    case particle_life::ParticleType::P:
        return sf::Color(80, 170, 255);
    }
    return sf::Color::White;
}

void drawSimulation(
    sf::RenderWindow& window,
    const sf::RectangleShape& worldRectangle,
    const particle_life::Simulation& simulation,
    const ViewerState& viewer,
    float framesPerSecond) {
    const auto& config = simulation.config();
    sf::CircleShape particleShape(config.dotSize);
    particleShape.setOrigin(config.dotSize, config.dotSize);

    sf::CircleShape reactionFlash(3.0f * config.dotSize);
    reactionFlash.setOrigin(3.0f * config.dotSize, 3.0f * config.dotSize);

    sf::CircleShape interactionCircle(config.interactionRadius);
    interactionCircle.setOrigin(config.interactionRadius, config.interactionRadius);
    interactionCircle.setFillColor(sf::Color::Transparent);
    interactionCircle.setOutlineThickness(0.1f);
    interactionCircle.setOutlineColor(sf::Color(180, 180, 180));

    const double persistenceSteps =
        static_cast<double>(viewer.persistenceSeconds) *
        static_cast<double>(framesPerSecond) *
        static_cast<double>(viewer.stepsPerFrame);

    std::unordered_map<particle_life::ParticleId, const particle_life::Particle*> particlesById;
    particlesById.reserve(simulation.particles().size());
    for (const particle_life::Particle& particle : simulation.particles()) {
        particlesById.emplace(particle.id, &particle);
    }

    // A right bond is drawn once. In periodic mode the minimum-image segment
    // is used, so a bond across the seam does not cross the whole box.
    for (const particle_life::Particle& particle : simulation.particles()) {
        if (
            particle.type != particle_life::ParticleType::P ||
            particle.rightBond == particle_life::kInvalidParticleId) {
            continue;
        }
        const auto partnerIterator = particlesById.find(particle.rightBond);
        if (partnerIterator == particlesById.end()) {
            continue;
        }
        const particle_life::Vec2 displacement = displayDisplacement(
            config, particle.position, partnerIterator->second->position);
        const sf::Vertex bond[] = {
            sf::Vertex(toSf(particle.position), sf::Color(160, 180, 200)),
            sf::Vertex(toSf(particle.position + displacement), sf::Color(160, 180, 200))
        };
        window.draw(bond, 2, sf::Lines);
    }

    for (const particle_life::Particle& particle : simulation.particles()) {
        const sf::Vector2f position = toSf(particle.position);
        const sf::Color color = particleColor(particle.type);

        if (particle.type == particle_life::ParticleType::S) {
            constexpr float tailLength = 10.0f;
            const particle_life::Vec2 tailEnd =
                particle.position +
                tailLength * particle_life::unitVectorFromAngle(
                                 particle.orientation + static_cast<float>(particle_life::kPi));
            const sf::Vertex tail[] = {
                sf::Vertex(position, sf::Color(210, 210, 210)),
                sf::Vertex(toSf(tailEnd), sf::Color(210, 210, 210))
            };
            window.draw(tail, 2, sf::Lines);
        } else if (particle.type == particle_life::ParticleType::P) {
            constexpr float normalLength = 6.0f;
            const particle_life::Vec2 normalEnd =
                particle.position +
                normalLength * particle_life::unitVectorFromAngle(particle.orientation);
            const sf::Vertex normal[] = {
                sf::Vertex(position, sf::Color(220, 230, 255)),
                sf::Vertex(toSf(normalEnd), sf::Color(220, 230, 255))
            };
            window.draw(normal, 2, sf::Lines);
        }

        if (
            persistenceSteps > 0.0 && simulation.stepIndex() > particle.spawnStep &&
            static_cast<double>(simulation.stepIndex() - particle.spawnStep) < persistenceSteps) {
            float alpha = static_cast<float>(
                static_cast<double>(simulation.stepIndex() - particle.spawnStep) / persistenceSteps);
            if (alpha < 0.25f) {
                alpha *= 4.0f;
            } else {
                alpha = 1.0f - (alpha - 0.25f) / 0.75f;
            }
            sf::Color flashColor = color;
            flashColor.a = static_cast<sf::Uint8>(std::clamp(alpha, 0.0f, 1.0f) * 255.0f);
            reactionFlash.setFillColor(flashColor);
            reactionFlash.setPosition(position);
            window.draw(reactionFlash);
        }

        particleShape.setFillColor(color);
        particleShape.setPosition(position);
        window.draw(particleShape);

        if (particle.type == particle_life::ParticleType::S && viewer.drawInteractionRadius) {
            interactionCircle.setPosition(position);
            window.draw(interactionCircle);
        }
    }

    window.draw(worldRectangle);
}

} // namespace

int main(int argc, char** argv) {
    try {
        const ViewerOptions options = parseOptions(argc, argv);

        particle_life::Simulation simulation({}, options.seed);
        if (!options.loadCheckpoint.empty()) {
            simulation.restore(particle_life::CheckpointIO::load(options.loadCheckpoint));
        }
        particle_life::ExperimentPlan experiment;
        ViewerState viewer;

        std::unique_ptr<particle_life::MetricsCsvWriter> metricsWriter;
        if (!options.metricsPath.empty()) {
            metricsWriter = std::make_unique<particle_life::MetricsCsvWriter>(options.metricsPath);
            metricsWriter->append(simulation);
        }

        sf::RenderWindow window(sf::VideoMode(1920, 1080), "Life Emergence");
        if (!ImGui::SFML::Init(window)) {
            std::cerr << "ImGui-SFML initialization failed\n";
            return 1;
        }
        ImGui::GetStyle().ScaleAllSizes(2.0f);
        ImGui::GetIO().FontGlobalScale = 2.0f;

        const auto& initialConfig = simulation.config();
        sf::View view(sf::FloatRect(
            -static_cast<float>(initialConfig.worldWidth) / 2.0f,
            -static_cast<float>(initialConfig.worldHeight) / 2.0f,
            static_cast<float>(initialConfig.worldWidth),
            static_cast<float>(initialConfig.worldHeight)));

        sf::RectangleShape worldRectangle(sf::Vector2f(
            static_cast<float>(initialConfig.worldWidth),
            static_cast<float>(initialConfig.worldHeight)));
        worldRectangle.setOutlineThickness(4.0f);
        worldRectangle.setOutlineColor(sf::Color::Red);
        worldRectangle.setFillColor(sf::Color::Transparent);
        worldRectangle.setOrigin(
            static_cast<float>(initialConfig.worldWidth) / 2.0f,
            static_cast<float>(initialConfig.worldHeight) / 2.0f);

        bool isDragging = false;
        sf::Vector2f lastMousePosition;
        sf::Vector2i mouseDownPixelPosition;
        sf::Clock deltaClock;
        std::uint64_t lastMetricStep = simulation.stepIndex();

        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                ImGui::SFML::ProcessEvent(event);
                switch (event.type) {
                case sf::Event::Closed:
                    window.close();
                    break;
                case sf::Event::MouseWheelScrolled:
                    if (!ImGui::GetIO().WantCaptureMouse) {
                        view.zoom(event.mouseWheelScroll.delta > 0.0f ? 0.9f : 1.1f);
                    }
                    break;
                case sf::Event::MouseButtonPressed:
                    if (!ImGui::GetIO().WantCaptureMouse && event.mouseButton.button == sf::Mouse::Left) {
                        isDragging = true;
                        mouseDownPixelPosition = sf::Mouse::getPosition(window);
                        lastMousePosition = window.mapPixelToCoords(mouseDownPixelPosition);
                    }
                    break;
                case sf::Event::MouseButtonReleased:
                    if (event.mouseButton.button == sf::Mouse::Left) {
                        if (!ImGui::GetIO().WantCaptureMouse) {
                            const sf::Vector2i mouseUpPixelPosition = sf::Mouse::getPosition(window);
                            constexpr int clickThreshold = 2;
                            if (
                                std::abs(mouseDownPixelPosition.x - mouseUpPixelPosition.x) < clickThreshold &&
                                std::abs(mouseDownPixelPosition.y - mouseUpPixelPosition.y) < clickThreshold) {
                                viewer.sourceEnabled = !viewer.sourceEnabled;
                                viewer.sourcePosition = fromSf(window.mapPixelToCoords(mouseUpPixelPosition));
                            }
                        }
                        isDragging = false;
                    }
                    break;
                case sf::Event::KeyPressed: {
                    const particle_life::Vec2 spawnOrigin = viewer.spawnAtMouseLocation
                        ? fromSf(window.mapPixelToCoords(sf::Mouse::getPosition(window)))
                        : particle_life::Vec2{};
                    if (event.key.code == sf::Keyboard::R) {
                        simulation.clearParticles();
                    } else if (event.key.code == sf::Keyboard::C) {
                        simulation.config().centerize = !simulation.config().centerize;
                    } else if (event.key.code == sf::Keyboard::S) {
                        simulation.spawn(particle_life::ParticleType::S, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::F) {
                        simulation.spawn(particle_life::ParticleType::F, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::A) {
                        simulation.spawn(particle_life::ParticleType::A, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::B) {
                        simulation.spawn(particle_life::ParticleType::B, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::L) {
                        simulation.spawn(particle_life::ParticleType::L, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::P) {
                        simulation.spawn(particle_life::ParticleType::P, spawnOrigin);
                    } else if (event.key.code == sf::Keyboard::Space) {
                        viewer.paused = !viewer.paused;
                    }
                    break;
                }
                default:
                    break;
                }
            }

            const sf::Time frameDelta = deltaClock.restart();
            ImGui::SFML::Update(window, frameDelta);
            const float framesPerSecond = frameDelta.asSeconds() > 0.0f
                ? 1.0f / frameDelta.asSeconds()
                : 0.0f;

            auto& config = simulation.config();
            ImGui::Begin("Simulation");
            ImGui::Text("FPS: %.1f", framesPerSecond);
            ImGui::Text("Step: %llu", static_cast<unsigned long long>(simulation.stepIndex()));
            ImGui::Text("Seed: %u", simulation.seed());
            ImGui::Text("Population: %zu", simulation.particles().size());
            ImGui::Text("P bonds: %zu", simulation.patchBondCount());
            ImGui::Checkbox("Paused", &viewer.paused);
            ImGui::SameLine();
            if (ImGui::Button("Single step")) {
                viewer.singleStepRequested = true;
            }
            if (ImGui::InputInt("Steps per frame", &viewer.stepsPerFrame)) {
                viewer.stepsPerFrame = std::max(viewer.stepsPerFrame, 1);
            }
            ImGui::SliderFloat("dt", &config.dt, 0.001f, 1.0f);
            ImGui::SliderFloat("Containing force", &config.containingForce, 0.0f, 2.0f);
            ImGui::SliderFloat("Centerize", &config.centerForce, 0.0f, 0.001f);
            ImGui::SliderFloat("Brownian speed", &config.brownianSpeed, 0.0f, 1.0f);
            ImGui::SliderFloat("Void viscosity", &config.voidViscosity, 0.90f, 1.0f);
            ImGui::SliderFloat("Void torque viscosity", &config.voidTorqueViscosity, 0.80f, 1.0f);

            const char* boundaryNames[] = {
                "Legacy soft containment",
                "Destroy outside",
                "Closed reflecting box",
                "Periodic wrap"
            };
            int boundaryMode = static_cast<int>(config.boundaryMode);
            if (ImGui::Combo("Boundary mode", &boundaryMode, boundaryNames, 4)) {
                config.boundaryMode = static_cast<particle_life::BoundaryMode>(boundaryMode);
            }

            ImGui::Separator();
            ImGui::Text("Legacy surfactant S");
            ImGui::SliderFloat("S interaction radius", &config.interactionRadius, 4.0f, 20.0f);
            ImGui::SliderFloat("S force strength", &config.surfactantForceStrength, 0.0f, 5.0f);
            ImGui::SliderFloat("S force exp power", &config.surfactantForceExponent, 1.0f, 5.0f);
            ImGui::SliderFloat("S torque strength", &config.surfactantTorqueStrength, 0.0f, 2.0f);
            ImGui::SliderFloat("S div angle", &config.divisionAngle, 0.0f, 0.4f);
            ImGui::SliderFloat("S force viscosity", &config.surfactantForceViscosity, 0.0f, 4.0f);
            ImGui::SliderFloat("S torque viscosity", &config.surfactantTorqueViscosity, 0.0f, 4.0f);
            ImGui::SliderFloat("S opposition threshold", &config.oppositionThreshold, 0.0f, 7.0f);

            if (ImGui::CollapsingHeader("Patch monomers P", ImGuiTreeNodeFlags_DefaultOpen)) {
                ImGui::TextWrapped(
                    "Each P monomer has one saturable left site and one saturable right site. "
                    "Raise temperature to dissociate, change the geometry, then cool to reassemble.");
                ImGui::SliderFloat("P preferred turn angle", &config.patch.preferredTurnAngle, -1.2f, 1.2f);
                ImGui::SliderFloat("P bond length", &config.patch.bondLength, 2.0f, 12.0f);
                ImGui::SliderFloat("P capture radius", &config.patch.captureRadius, 0.05f, 8.0f);
                ImGui::SliderFloat("P capture angle", &config.patch.captureAngle, 0.05f, 3.14159f);
                ImGui::SliderFloat("P bond stiffness", &config.patch.bondStiffness, 0.0f, 20.0f);
                ImGui::SliderFloat("P bending stiffness", &config.patch.bendingStiffness, 0.0f, 10.0f);
                ImGui::SliderFloat("P bond damping", &config.patch.bondDamping, 0.0f, 5.0f);
                ImGui::SliderFloat("P break distance", &config.patch.breakDistance, 0.05f, 15.0f);
                ImGui::SliderFloat("P break angle", &config.patch.breakAngle, 0.05f, 3.14159f);
                ImGui::SliderFloat("P core repulsion radius", &config.patch.coreRepulsionRadius, 0.5f, 12.0f);
                ImGui::SliderFloat("P core repulsion strength", &config.patch.coreRepulsionStrength, 0.0f, 50.0f);
                ImGui::SliderFloat("P temperature", &config.patch.temperature, 0.0f, 10.0f);
                ImGui::SliderFloat("P thermal break rate", &config.patch.thermalBreakRate, 0.0f, 5.0f);

                if (ImGui::InputInt("P batch count", &viewer.patchBatchCount)) {
                    viewer.patchBatchCount = std::max(viewer.patchBatchCount, 0);
                }
                if (ImGui::Button("Spawn P batch")) {
                    simulation.spawnMany(
                        particle_life::ParticleType::P,
                        static_cast<std::size_t>(viewer.patchBatchCount));
                }
                ImGui::SameLine();
                if (ImGui::Button("Break all P bonds")) {
                    simulation.breakAllPatchBonds();
                }
                ImGui::SameLine();
                if (ImGui::Button("Reset P defaults")) {
                    config.patch = particle_life::PatchParticleConfig{};
                }
            }

            ImGui::Separator();
            ImGui::Combo(
                "Click source particle",
                &viewer.sourceTypeIndex,
                kParticleTypeNames.data(),
                static_cast<int>(kParticleTypeNames.size()));
            ImGui::Text("Click source: %s", viewer.sourceEnabled ? "ON" : "OFF");
            ImGui::Checkbox("Draw S interaction radius", &viewer.drawInteractionRadius);
            ImGui::Checkbox("Spawn particles at mouse location", &viewer.spawnAtMouseLocation);
            bool useSpatialGrid = config.neighborSearchMode == particle_life::NeighborSearchMode::SpatialGrid;
            if (ImGui::Checkbox("Use spatial grid", &useSpatialGrid)) {
                config.neighborSearchMode = useSpatialGrid
                    ? particle_life::NeighborSearchMode::SpatialGrid
                    : particle_life::NeighborSearchMode::BruteForce;
            }
            if (ImGui::Button("Save checkpoint")) {
                particle_life::CheckpointIO::save(options.checkpointPath, simulation);
            }
            ImGui::Text("S/F/A/B/L/P: spawn, C: centerize, R: clear, Space: pause");
            ImGui::End();

            if (isDragging && sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
                const sf::Vector2f mousePosition =
                    window.mapPixelToCoords(sf::Mouse::getPosition(window));
                view.move(lastMousePosition - mousePosition);
            }
            lastMousePosition = window.mapPixelToCoords(sf::Mouse::getPosition(window));

            const bool shouldRun = !viewer.paused || viewer.singleStepRequested;
            if (shouldRun) {
                if (viewer.sourceEnabled && !viewer.singleStepRequested) {
                    simulation.spawn(
                        kParticleTypes.at(static_cast<std::size_t>(viewer.sourceTypeIndex)),
                        viewer.sourcePosition);
                }
                const int stepCount = viewer.singleStepRequested ? 1 : viewer.stepsPerFrame;
                for (int step = 0; step < stepCount; ++step) {
                    experiment.applyBeforeStep(simulation);
                    simulation.step();
                    if (
                        metricsWriter &&
                        simulation.stepIndex() / options.metricsEverySteps >
                            lastMetricStep / options.metricsEverySteps) {
                        metricsWriter->append(simulation);
                        lastMetricStep = simulation.stepIndex();
                    }
                }
            }
            viewer.singleStepRequested = false;

            window.setView(view);
            window.clear(sf::Color::Black);
            drawSimulation(window, worldRectangle, simulation, viewer, framesPerSecond);
            ImGui::SFML::Render(window);
            window.display();
        }

        if (!options.checkpointPath.empty()) {
            particle_life::CheckpointIO::save(options.checkpointPath, simulation);
        }
        ImGui::SFML::Shutdown();
        return 0;
    } catch (const std::exception& exception) {
        std::cerr << "Error: " << exception.what() << '\n';
        return 1;
    }
}
