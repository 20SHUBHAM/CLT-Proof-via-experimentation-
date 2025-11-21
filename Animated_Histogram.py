import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from scipy.stats import norm
import shutil

# Techy color palette
SAMPLE_COLOR = '#1ef9d3'
MEAN_GRADIENT = ['#00bcd4', '#2196f3', '#3f51b5', '#00acc1']
CURVE_COLOR = '#00c2ff'
GRID_COLOR = '#0d1117'
TITLE_COLOR = '#00ffe7'
LABEL_COLOR = '#ffde57'
BAND_COLOR = '#333d52'

# Set font globally
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['xtick.color'] = LABEL_COLOR
plt.rcParams['ytick.color'] = LABEL_COLOR


def animated_clt(population, sample_size=30, n_frames=200):
    """Animate the CLT as more samples are collected"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=GRID_COLOR)

    # Storage
    sample_means = []

    def init():
        ax1.clear()
        ax2.clear()
        return ax1, ax2

    def update(frame):
        # Take one sample
        sample = np.random.choice(population, size=sample_size, replace=True)
        sample_means.append(sample.mean())

        # Top plot: Current sample distribution
        ax1.clear()
        ax1.patch.set_facecolor(BAND_COLOR)
        counts, bins, patches = ax1.hist(
            sample,
            bins=np.linspace(1, 101, 15),
            alpha=0.8,
            color=SAMPLE_COLOR,
            edgecolor='#38006b',
            linewidth=2,
        )

        # Apply gradient to histogram bars
        for i, patch in enumerate(patches):
            color_idx = i % len(MEAN_GRADIENT)
            patch.set_facecolor(MEAN_GRADIENT[color_idx])

        ax1.set_title(f'Current Sample (n={sample_size})',
                      fontweight='bold', color=TITLE_COLOR, fontsize=16)
        ax1.set_xlim(0, 100)
        ax1.set_ylabel('Frequency', color=LABEL_COLOR, fontsize=12)
        ax1.grid(True, color='#222d3d', linestyle='-', alpha=0.3)
        ax1.tick_params(axis='x', colors=LABEL_COLOR)
        ax1.tick_params(axis='y', colors=LABEL_COLOR)

        # Bottom plot: Sampling distribution evolution
        ax2.clear()
        ax2.patch.set_facecolor(BAND_COLOR)

        if len(sample_means) > 5:
            counts2, bins2, patches2 = ax2.hist(
                sample_means,
                bins=min(30, len(sample_means) // 5),
                density=True,
                alpha=0.85,
                color=CURVE_COLOR,
                edgecolor='#17003b',
                linewidth=2,
            )

            # Apply gradient to histogram bars
            for i, patch in enumerate(patches2):
                color_idx = i % len(MEAN_GRADIENT)
                patch.set_facecolor(MEAN_GRADIENT[color_idx])

            # Fit normal curve if enough data
            if len(sample_means) > 30:
                mu = float(np.mean(sample_means))
                sigma = float(np.std(sample_means))
                x = np.linspace(min(sample_means), max(sample_means), 100)

                # Normal curve
                ax2.plot(x, norm.pdf(x, mu, sigma), '-',
                         linewidth=3, color=CURVE_COLOR, alpha=0.9)

                ax2.axvline(mu, color=TITLE_COLOR, linestyle='--',
                            linewidth=2.5, label=f'mu={mu:.2f}, sigma={sigma:.2f}')
                ax2.legend(facecolor=BAND_COLOR, edgecolor=GRID_COLOR,
                           fontsize=11, labelcolor=LABEL_COLOR)

        ax2.set_title(f'Sampling Distribution ({len(sample_means)} samples)',
                      fontweight='bold', color=TITLE_COLOR, fontsize=16)
        ax2.set_xlabel('Sample Mean', color=LABEL_COLOR, fontsize=13)
        ax2.set_ylabel('Density', color=LABEL_COLOR, fontsize=13)
        ax2.grid(True, color='#222d3d', linestyle='-', alpha=0.3)
        ax2.tick_params(axis='x', colors=LABEL_COLOR)
        ax2.tick_params(axis='y', colors=LABEL_COLOR)

        return ax1, ax2

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init,
                         interval=80, blit=False, repeat=False)
    plt.tight_layout()
    return anim


# =============================================================================
# MAIN EXECUTION: Generate and Save Animation
# =============================================================================

if __name__ == "__main__":
    # Create population
    population = np.random.randint(1, 101, size=1000)

    # Generate animation
    print("Generating CLT animation...")
    anim = animated_clt(population, sample_size=30, n_frames=200)

    # Save as MP4 (requires ffmpeg installed and on PATH)
    print("Saving as MP4...")
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path is None:
        print("Skipping MP4: ffmpeg not found on PATH. Install ffmpeg or add it to PATH to enable MP4 output.")
    else:
        try:
            writer_mp4 = FFMpegWriter(fps=20, metadata=dict(artist='CLT Demo'), bitrate=1800)
            anim.save('clt_animation.mp4', writer=writer_mp4, dpi=150)
            print("Saved as clt_animation.mp4")
        except (FileNotFoundError, OSError) as e:
            print(f"Skipping MP4 due to ffmpeg error: {e}")

    # Save as GIF (alternative)
    print("Saving as GIF...")
    writer_gif = PillowWriter(fps=12, metadata=dict(artist='CLT Demo'))
    anim.save('clt_animation1.gif', writer=writer_gif, dpi=100)
    print("Saved as clt_animation.gif")

    # Display the animation (optional)
    plt.show()

    print("\nAnimation saved successfully!")
    print("For Medium blog:")
    print("   - Upload MP4 to YouTube/Drive and embed link")
    print("   - Or drag-and-drop GIF directly into Medium editor")


