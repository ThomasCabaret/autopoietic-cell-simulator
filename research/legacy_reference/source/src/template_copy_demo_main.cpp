#include "particle_life/template_copy.hpp"

#include "imgui.h"
#include "imgui-SFML.h"
#include <SFML/Graphics.hpp>

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

using particle_life::Vec2;
using namespace particle_life::template_copy;

struct Options {
    std::uint32_t seed = 5489u;
};

struct ViewerState {
    int stepsPerFrame = 12;
    bool paused = false;
    bool singleStep = false;
    int freeZeroCount = 48;
    int freeOneCount = 48;
    int spawnBatchCount = 20;
    int spawnSymbol = 0;
    bool drawPairBonds = true;
    bool drawPorts = true;
    std::array<char, 33> sequenceBuffer{};
};

Options parseOptions(int argc, char** argv) {
    Options options;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--seed") {
            if (index + 1 >= argc) {
                throw std::invalid_argument("Missing value after --seed");
            }
            options.seed = static_cast<std::uint32_t>(std::stoul(argv[++index]));
        } else {
            throw std::invalid_argument("Unknown argument: " + argument);
        }
    }
    return options;
}

sf::Vector2f toSf(const Vec2& value) {
    return {value.x, value.y};
}

Vec2 fromSf(const sf::Vector2f& value) {
    return {value.x, value.y};
}

Vec2 displayDisplacement(const Config& config, const Vec2& from, const Vec2& to) {
    Vec2 result = to - from;
    if (config.boundaryMode == BoundaryMode::Wrap) {
        result.x -= std::round(result.x / config.worldWidth) * config.worldWidth;
        result.y -= std::round(result.y / config.worldHeight) * config.worldHeight;
    }
    return result;
}

sf::Color symbolColor(Symbol symbol) {
    return symbol == Symbol::Zero
        ? sf::Color(40, 210, 235)
        : sf::Color(240, 80, 205);
}

void drawLine(
    sf::RenderWindow& window,
    const Vec2& start,
    const Vec2& displacement,
    sf::Color color) {
    const sf::Vertex vertices[] = {
        sf::Vertex(toSf(start), color),
        sf::Vertex(toSf(start + displacement), color)
    };
    window.draw(vertices, 2, sf::Lines);
}

void drawModel(
    sf::RenderWindow& window,
    const Model& model,
    const ViewerState& viewer,
    const sf::RectangleShape& worldRectangle) {
    const Config& config = model.config();
    const auto& particles = model.particles();

    for (const Particle& particle : particles) {
        if (particle.right != kInvalidParticleId && particle.right < particles.size()) {
            drawLine(
                window,
                particle.position,
                displayDisplacement(config, particle.position, particles[particle.right].position),
                sf::Color(225, 225, 225));
        }
    }

    if (viewer.drawPairBonds) {
        for (const Particle& particle : particles) {
            if (particle.pairRole == PairRole::Template
                && particle.pair != kInvalidParticleId
                && particle.pair < particles.size()) {
                drawLine(
                    window,
                    particle.position,
                    displayDisplacement(config, particle.position, particles[particle.pair].position),
                    model.phase() == CyclePhase::Capture
                        ? sf::Color(120, 190, 120)
                        : sf::Color(230, 120, 80));
            }
        }
    }

    sf::CircleShape body(config.particleRadius);
    body.setOrigin(config.particleRadius, config.particleRadius);

    for (const Particle& particle : particles) {
        const sf::Color color = symbolColor(particle.symbol);
        body.setPosition(toSf(particle.position));
        body.setFillColor(color);
        if (particle.pairRole == PairRole::Copy) {
            body.setOutlineThickness(0.7f);
            body.setOutlineColor(sf::Color::White);
        } else {
            body.setOutlineThickness(0.0f);
        }
        window.draw(body);

        if (viewer.drawPorts) {
            const Vec2 tangent = particle_life::unitVectorFromAngle(particle.orientation);
            const Vec2 normal = particle_life::rotateVector(
                tangent,
                static_cast<float>(particle_life::kPi * 0.5));
            drawLine(window, particle.position, tangent * (config.particleRadius + 1.8f), sf::Color(200, 200, 200));
            drawLine(window, particle.position, normal * (config.particleRadius + 2.8f), sf::Color(100, 240, 120));
        }
    }

    window.draw(worldRectangle);
}

void resetModel(Model& model, ViewerState& viewer) {
    const std::string sequence(viewer.sequenceBuffer.data());
    if (!isValidSequence(sequence)) {
        return;
    }
    model.reset(sequence, viewer.freeZeroCount, viewer.freeOneCount);
}

} // namespace

int main(int argc, char** argv) {
    try {
        const Options options = parseOptions(argc, argv);
        Model model(options.seed);
        ViewerState viewer;
        const std::string defaultSequence = "011010";
        std::copy(defaultSequence.begin(), defaultSequence.end(), viewer.sequenceBuffer.begin());
        viewer.sequenceBuffer[defaultSequence.size()] = '\0';
        resetModel(model, viewer);

        sf::RenderWindow window(sf::VideoMode(1600, 900), "Template Copy Demonstrator");
        window.setVerticalSyncEnabled(true);
        if (!ImGui::SFML::Init(window)) {
            std::cerr << "ImGui-SFML initialization failed\n";
            return 1;
        }
        ImGui::GetStyle().ScaleAllSizes(1.6f);
        ImGui::GetIO().FontGlobalScale = 1.6f;

        sf::View view(sf::FloatRect(
            -model.config().worldWidth * 0.5f,
            -model.config().worldHeight * 0.5f,
            model.config().worldWidth,
            model.config().worldHeight));

        sf::RectangleShape worldRectangle({model.config().worldWidth, model.config().worldHeight});
        worldRectangle.setOrigin(model.config().worldWidth * 0.5f, model.config().worldHeight * 0.5f);
        worldRectangle.setFillColor(sf::Color::Transparent);
        worldRectangle.setOutlineColor(sf::Color(180, 180, 180));
        worldRectangle.setOutlineThickness(1.0f);

        bool dragging = false;
        sf::Vector2f lastMouseWorld;
        sf::Clock frameClock;

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
                    if (!ImGui::GetIO().WantCaptureMouse) {
                        if (event.mouseButton.button == sf::Mouse::Middle) {
                            dragging = true;
                            lastMouseWorld = window.mapPixelToCoords(sf::Mouse::getPosition(window), view);
                        } else if (event.mouseButton.button == sf::Mouse::Left) {
                            const Vec2 position = fromSf(window.mapPixelToCoords(
                                sf::Mouse::getPosition(window), view));
                            model.spawnFreeMonomer(
                                viewer.spawnSymbol == 0 ? Symbol::Zero : Symbol::One,
                                position);
                        }
                    }
                    break;
                case sf::Event::MouseButtonReleased:
                    if (event.mouseButton.button == sf::Mouse::Middle) {
                        dragging = false;
                    }
                    break;
                case sf::Event::KeyPressed:
                    if (!ImGui::GetIO().WantCaptureKeyboard) {
                        if (event.key.code == sf::Keyboard::Space) {
                            viewer.paused = !viewer.paused;
                        } else if (event.key.code == sf::Keyboard::R) {
                            resetModel(model, viewer);
                        } else if (event.key.code == sf::Keyboard::Num0) {
                            viewer.spawnSymbol = 0;
                        } else if (event.key.code == sf::Keyboard::Num1) {
                            viewer.spawnSymbol = 1;
                        }
                    }
                    break;
                default:
                    break;
                }
            }

            if (dragging && sf::Mouse::isButtonPressed(sf::Mouse::Middle)) {
                const sf::Vector2f mouseWorld = window.mapPixelToCoords(sf::Mouse::getPosition(window), view);
                view.move(lastMouseWorld - mouseWorld);
                lastMouseWorld = window.mapPixelToCoords(sf::Mouse::getPosition(window), view);
            }

            const sf::Time frameDelta = frameClock.restart();
            ImGui::SFML::Update(window, frameDelta);
            const float fps = frameDelta.asSeconds() > 0.0f ? 1.0f / frameDelta.asSeconds() : 0.0f;

            Config& config = model.config();
            const Statistics statistics = model.statistics();

            ImGui::Begin("Template Copy Demo");
            ImGui::Text("FPS %.1f | simulated time %.2f | step %llu",
                fps,
                model.simulationTime(),
                static_cast<unsigned long long>(model.stepCount()));
            ImGui::Text("Phase: %s (%.2f s remaining)", phaseName(model.phase()), model.phaseTimeRemaining());
            ImGui::Text("Particles: %zu | free: %zu | chains: %zu",
                statistics.particleCount,
                statistics.freeMonomerCount,
                statistics.chainCount);
            ImGui::Text("Pair bonds: %zu | backbone bonds: %zu",
                statistics.pairBondCount,
                statistics.backboneBondCount);
            ImGui::Text("Exact chains: %zu total | %zu detached",
                statistics.exactSequenceCount,
                statistics.detachedExactSequenceCount);
            ImGui::Text("Completed copies: %zu total | %zu detached",
                statistics.exactCopyCount,
                statistics.detachedExactCopyCount);
            if (statistics.detachedExactSequenceCount >= 4) {
                ImGui::TextColored(
                    ImVec4(0.35f, 1.0f, 0.45f, 1.0f),
                    "Replication milestone reached: four detached exact chains.");
            }
            ImGui::Text("Longest chain: %zu", statistics.longestChainLength);

            ImGui::Checkbox("Paused", &viewer.paused);
            ImGui::SameLine();
            if (ImGui::Button("Single step")) {
                viewer.singleStep = true;
            }
            ImGui::SameLine();
            if (ImGui::Button("Reset experiment")) {
                resetModel(model, viewer);
            }
            ImGui::SameLine();
            if (ImGui::Button("Clear")) {
                model.clear();
            }

            ImGui::Separator();
            ImGui::Text("Initial condition");
            ImGui::InputText("Template sequence", viewer.sequenceBuffer.data(), viewer.sequenceBuffer.size());
            if (!isValidSequence(std::string(viewer.sequenceBuffer.data()))) {
                ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.3f, 1.0f), "Use 2-32 symbols containing only 0 and 1.");
            }
            ImGui::SliderInt("Initial free 0", &viewer.freeZeroCount, 0, 250);
            ImGui::SliderInt("Initial free 1", &viewer.freeOneCount, 0, 250);
            ImGui::SliderInt("Spawn batch", &viewer.spawnBatchCount, 1, 200);
            const char* symbolNames[] = {"0", "1"};
            ImGui::Combo("Click / batch symbol", &viewer.spawnSymbol, symbolNames, 2);
            if (ImGui::Button("Spawn free batch")) {
                model.spawnFreeMonomers(
                    viewer.spawnSymbol == 0 ? Symbol::Zero : Symbol::One,
                    viewer.spawnBatchCount);
            }
            ImGui::SameLine();
            if (ImGui::Button("Spawn another template")) {
                const std::string sequence(viewer.sequenceBuffer.data());
                if (isValidSequence(sequence)) {
                    model.spawnTemplate(sequence);
                }
            }

            ImGui::Separator();
            ImGui::Text("Macroscopic cycle");
            ImGui::Checkbox("Automatic capture/release cycle", &config.automaticCycle);
            if (ImGui::Button("Force capture phase")) {
                model.forcePhase(CyclePhase::Capture);
            }
            ImGui::SameLine();
            if (ImGui::Button("Force release phase")) {
                model.forcePhase(CyclePhase::Release);
            }
            ImGui::SliderFloat("Capture duration", &config.captureDuration, 0.1f, 30.0f, "%.2f s");
            ImGui::SliderFloat("Release duration", &config.releaseDuration, 0.1f, 15.0f, "%.2f s");
            ImGui::SliderFloat("Capture noise", &config.captureNoise, 0.0f, 8.0f);
            ImGui::SliderFloat("Release noise", &config.releaseNoise, 0.0f, 15.0f);
            ImGui::SliderFloat("Release pair break rate", &config.releasePairBreakRate, 0.0f, 60.0f);
            ImGui::SliderFloat("Release repulsion", &config.releaseRepulsionStrength, 0.0f, 80.0f);

            if (ImGui::CollapsingHeader("Template pairing", ImGuiTreeNodeFlags_DefaultOpen)) {
                ImGui::TextWrapped(
                    "Exact copy: a free 0 binds only to a template 0, and a free 1 only to a template 1. "
                    "Only backbone-free monomers can be captured as copy substrates.");
                ImGui::SliderFloat("Pair distance", &config.pairDistance, 3.0f, 20.0f);
                ImGui::SliderFloat("Pair capture radius", &config.pairCaptureRadius, 0.5f, 25.0f);
                ImGui::SliderFloat("Pair capture rate", &config.pairCaptureRate, 0.0f, 80.0f);
                ImGui::SliderFloat("Pair spring", &config.pairStrength, 0.0f, 120.0f);
                ImGui::SliderFloat("Pair damping", &config.pairDamping, 0.0f, 12.0f);
                ImGui::SliderFloat("Pair alignment", &config.pairAlignmentStrength, 0.0f, 60.0f);
                ImGui::SliderFloat("Pair break distance", &config.pairBreakDistance, 4.0f, 50.0f);
            }

            if (ImGui::CollapsingHeader("Backbone and ligation", ImGuiTreeNodeFlags_DefaultOpen)) {
                ImGui::SliderFloat("Backbone rest length", &config.backboneRestLength, 3.0f, 18.0f);
                ImGui::SliderFloat("Backbone spring", &config.backboneStrength, 0.0f, 150.0f);
                ImGui::SliderFloat("Backbone damping", &config.backboneDamping, 0.0f, 15.0f);
                ImGui::SliderFloat("Backbone alignment", &config.backboneAlignmentStrength, 0.0f, 80.0f);
                ImGui::SliderFloat("Backbone break distance", &config.backboneBreakDistance, 5.0f, 50.0f);
                ImGui::SliderFloat("Ligation distance", &config.ligationDistance, 3.0f, 25.0f);
                ImGui::SliderFloat("Ligation angle tolerance", &config.ligationAngleTolerance, 0.05f, 3.14159f);
                ImGui::SliderFloat("Ligation rate", &config.ligationRate, 0.0f, 100.0f);
            }

            if (ImGui::CollapsingHeader("General mechanics")) {
                ImGui::SliderFloat("dt", &config.dt, 0.001f, 0.08f, "%.4f");
                ImGui::SliderInt("Steps per frame", &viewer.stepsPerFrame, 1, 100);
                ImGui::SliderFloat("Particle radius", &config.particleRadius, 0.5f, 6.0f);
                ImGui::SliderFloat("Repulsion radius", &config.repulsionRadius, 1.0f, 15.0f);
                ImGui::SliderFloat("Repulsion strength", &config.repulsionStrength, 0.0f, 200.0f);
                ImGui::SliderFloat("Linear damping", &config.linearDamping, 0.80f, 1.0f, "%.4f");
                ImGui::SliderFloat("Angular damping", &config.angularDamping, 0.80f, 1.0f, "%.4f");
                const char* boundaryNames[] = {"Reflecting box", "Periodic wrap"};
                int boundaryMode = static_cast<int>(config.boundaryMode);
                if (ImGui::Combo("Boundary mode", &boundaryMode, boundaryNames, 2)) {
                    config.boundaryMode = static_cast<BoundaryMode>(boundaryMode);
                }
            }

            if (ImGui::CollapsingHeader("Display and controls")) {
                ImGui::Checkbox("Draw pair bonds", &viewer.drawPairBonds);
                ImGui::Checkbox("Draw orientation / template ports", &viewer.drawPorts);
                ImGui::TextWrapped(
                    "Left click: add selected free monomer. Middle drag: pan. Wheel: zoom. "
                    "0/1: select symbol. Space: pause. R: reset.");
            }


            if (ImGui::CollapsingHeader("Sequence census", ImGuiTreeNodeFlags_DefaultOpen)) {
                const std::vector<SequenceCensusEntry> census = model.sequenceCensus();
                if (census.empty()) {
                    ImGui::TextUnformatted("No polymer chain yet.");
                } else {
                    for (const SequenceCensusEntry& entry : census) {
                        ImGui::Text("%s: %zu total, %zu detached",
                            entry.sequence.c_str(),
                            entry.totalCount,
                            entry.detachedCount);
                    }
                }
            }

            if (ImGui::CollapsingHeader("Chain length histogram")) {
                for (std::size_t length = 1; length < statistics.chainLengthHistogram.size(); ++length) {
                    const std::size_t count = statistics.chainLengthHistogram[length];
                    if (count == 0) {
                        continue;
                    }
                    if (length + 1 == statistics.chainLengthHistogram.size()) {
                        ImGui::Text("length >= %zu: %zu", length, count);
                    } else {
                        ImGui::Text("length %zu: %zu", length, count);
                    }
                }
            }
            ImGui::End();

            if (!viewer.paused || viewer.singleStep) {
                const int stepCount = viewer.singleStep ? 1 : viewer.stepsPerFrame;
                for (int step = 0; step < stepCount; ++step) {
                    model.step();
                }
            }
            viewer.singleStep = false;

            window.setView(view);
            window.clear(sf::Color(12, 14, 18));
            drawModel(window, model, viewer, worldRectangle);
            ImGui::SFML::Render(window);
            window.display();
        }

        ImGui::SFML::Shutdown();
        return 0;
    } catch (const std::exception& exception) {
        std::cerr << "Error: " << exception.what() << '\n';
        return 1;
    }
}
