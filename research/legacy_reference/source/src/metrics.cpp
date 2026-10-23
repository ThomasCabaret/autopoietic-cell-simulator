#include "particle_life/metrics.hpp"

#include "particle_life/math.hpp"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <locale>
#include <stdexcept>

namespace particle_life {

MetricsSample collectMetrics(const Simulation& simulation) {
    MetricsSample sample;
    sample.step = simulation.stepIndex();
    sample.total = simulation.particles().size();
    sample.patchBonds = simulation.patchBondCount();

    double speedSum = 0.0;
    for (const Particle& particle : simulation.particles()) {
        const std::size_t typeIndex = static_cast<std::size_t>(particle.type);
        ++sample.typeCounts.at(typeIndex);

        const double speedSquared = static_cast<double>(normSquared(particle.velocity));
        const double speed = std::sqrt(speedSquared);
        speedSum += speed;
        sample.maximumSpeed = std::max(sample.maximumSpeed, speed);
        sample.kineticEnergy += 0.5 * speedSquared;
    }

    if (sample.total != 0U) {
        sample.meanSpeed = speedSum / static_cast<double>(sample.total);
    }
    return sample;
}

MetricsCsvWriter::MetricsCsvWriter(const std::filesystem::path& path)
    : output_(path, std::ios::trunc) {
    if (!output_) {
        throw std::runtime_error("Cannot open metrics file: " + path.string());
    }
    output_.imbue(std::locale::classic());
    output_ << std::setprecision(17);
    output_ << "step,total,F,A,B,S,L,P,patch_bonds,mean_speed,max_speed,kinetic_energy\n";
}

void MetricsCsvWriter::append(const Simulation& simulation) {
    append(collectMetrics(simulation));
}

void MetricsCsvWriter::append(const MetricsSample& sample) {
    output_ << sample.step << ',' << sample.total;
    for (const std::size_t count : sample.typeCounts) {
        output_ << ',' << count;
    }
    output_ << ',' << sample.patchBonds << ',' << sample.meanSpeed << ','
            << sample.maximumSpeed << ',' << sample.kineticEnergy << '\n';
    output_.flush();

    if (!output_) {
        throw std::runtime_error("Failed while writing metrics");
    }
}

} // namespace particle_life
