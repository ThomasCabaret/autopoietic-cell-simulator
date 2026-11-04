"""Optional static figures, separate from mechanics and headless imports."""
import numpy as np

def plot_run(observer, config, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    indices = np.linspace(0, len(observer.frames) - 1, 4, dtype=int)
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.5), constrained_layout=True)
    all_pos = np.concatenate(observer.frames)
    lo, hi = all_pos.min(axis=0) - .5, all_pos.max(axis=0) + .5
    for ax, index in zip(axes, indices):
        p = observer.frames[index]
        n = len(p) // 2
        for i in range(n):
            ax.plot(p[[i, n + i], 0], p[[i, n + i], 1], color="#bbc4cc", lw=.7)
        mat = observer.edges_frames[index]
        if config["mode"] == "copy":
            for i, j in np.argwhere(np.triu(mat, 1)):
                ax.plot(p[[i, j], 0], p[[i, j], 1], color="#617889", lw=1.5)
            ax.scatter(p[:n, 0], p[:n, 1], c=np.array(["#718594", "#9a4aa0"])[observer.last_families], s=15)
            ax.scatter(p[n:, 0], p[n:, 1], c=np.array(["#148e9c", "#df7947", "#8d75bb"])[observer.last_bits], s=18)
        else:
            for row in (0, 1):
                for i, j in np.argwhere(np.triu(mat[row], 1)):
                    a, b = row * n + i, row * n + j
                    ax.plot(p[[a, b], 0], p[[a, b], 1], color=["#148e9c", "#df7947"][row], lw=1.8)
            ax.scatter(p[:n, 0], p[:n, 1], color="#148e9c", s=20)
            ax.scatter(p[n:, 0], p[n:, 1], color="#df7947", s=20)
        ax.set_title(f"t = {observer.times[index]:.1f}")
        ax.set_xlim(lo[0], hi[0])
        ax.set_ylim(lo[1], hi[1])
        ax.set_aspect("equal")
    fig.suptitle(f"{config['case']} | graine {config['seed']} | {config['mode']} | conditions initiales : {config.get('initial', 'polymere + monomeres libres')}")
    fig.savefig(out / "trajectory.png", dpi=140)
    plt.close(fig)


