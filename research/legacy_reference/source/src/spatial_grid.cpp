#include "particle_life/spatial_grid.hpp"

#include <algorithm>
#include <cmath>
#include <functional>
#include <stdexcept>

namespace particle_life {

SpatialGrid::SpatialGrid(float cellSize) {
    setCellSize(cellSize);
}

void SpatialGrid::setCellSize(float cellSize) {
    if (!(cellSize > 0.0f)) {
        throw std::invalid_argument("SpatialGrid cell size must be positive");
    }
    cellSize_ = cellSize;
}

std::size_t SpatialGrid::CellHash::operator()(const Cell& cell) const noexcept {
    const std::size_t xHash = std::hash<int>{}(cell.x);
    const std::size_t yHash = std::hash<int>{}(cell.y);
    return xHash ^ (yHash + 0x9e3779b97f4a7c15ULL + (xHash << 6U) + (xHash >> 2U));
}

SpatialGrid::Cell SpatialGrid::cellForPosition(const Vec2& position) const noexcept {
    return {
        static_cast<int>(std::floor(position.x / cellSize_)),
        static_cast<int>(std::floor(position.y / cellSize_))
    };
}

void SpatialGrid::rebuild(const std::vector<Particle>& particles) {
    cells_.clear();
    cells_.reserve(particles.size());

    for (std::size_t index = 0; index < particles.size(); ++index) {
        cells_[cellForPosition(particles[index].position)].push_back(index);
    }
}

void SpatialGrid::queryCandidateIndices(
    const Vec2& position,
    std::vector<std::size_t>& output) const {
    output.clear();
    const Cell center = cellForPosition(position);

    for (int deltaY = -1; deltaY <= 1; ++deltaY) {
        for (int deltaX = -1; deltaX <= 1; ++deltaX) {
            const Cell cell{center.x + deltaX, center.y + deltaY};
            const auto iterator = cells_.find(cell);
            if (iterator == cells_.end()) {
                continue;
            }
            output.insert(output.end(), iterator->second.begin(), iterator->second.end());
        }
    }

    // The unordered grid is only an acceleration structure. Sorting restores
    // the same first-arrived/first-served order as a vector-wide scan.
    std::sort(output.begin(), output.end());
}

} // namespace particle_life
