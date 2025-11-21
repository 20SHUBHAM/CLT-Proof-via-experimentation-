import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import norm

# Techy cyberpunk color palette
SAMPLE_COLOR = '#1ef9d3'
MEAN_GRADIENT = ['#4c47e4', '#792ec7', '#be23c4', '#f174ea']
CURVE_COLOR = '#ff24a5'
GRID_COLOR = '#0d1117'
TITLE_COLOR = '#00ffe7'
LABEL_COLOR = '#ffde57'
BAND_COLOR = '#333d52'
POPULATION_COLOR = '#08F7FE'
NORMAL_CURVE_COLOR = '#FE53BB'

# Set matplotlib style globally
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = GRID_COLOR
plt.rcParams['axes.facecolor'] = BAND_COLOR
plt.rcParams['axes.edgecolor'] = LABEL_COLOR
plt.rcParams['text.color'] = LABEL_COLOR
plt.rcParams['axes.labelcolor'] = LABEL_COLOR
plt.rcParams['xtick.color'] = LABEL_COLOR
plt.rcParams['ytick.color'] = LABEL_COLOR
plt.rcParams['grid.color'] = '#2A3459'
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_clt_gif(population, output_filename='clt_interactive.gif'):
    """
    Create an animated GIF showing CLT with varying sample sizes
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor=GRID_COLOR)
    
    # Sample sizes to animate through
    sample_sizes = list(range(5, 105, 5))  # 5, 10, 15, ..., 100
    n_samples = 1000  # Fixed number of samples
    
    def init():
        ax1.clear()
        ax2.clear()
        return ax1, ax2
    
    def update(frame):
        sample_size = sample_sizes[frame]
        
        # Clear axes
        ax1.clear()
        ax2.clear()
        
        # LEFT PLOT: Population distribution (constant)
        ax1.patch.set_facecolor(BAND_COLOR)
        counts1, bins1, patches1 = ax1.hist(
            population, 
            bins=20, 
            alpha=0.85, 
            color=POPULATION_COLOR,
            edgecolor='#38006b', 
            density=True,
            linewidth=2
        )
        
        # Apply gradient to population histogram
        for i, patch in enumerate(patches1):
            color_idx = i % len(MEAN_GRADIENT)
            patch.set_facecolor(MEAN_GRADIENT[color_idx])
            patch.set_alpha(0.8)
        
        ax1.set_title('Population Distribution', 
                     fontweight='bold', color=TITLE_COLOR, fontsize=16)
        ax1.set_xlabel('Value', color=LABEL_COLOR, fontsize=13)
        ax1.set_ylabel('Density', color=LABEL_COLOR, fontsize=13)
        ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # RIGHT PLOT: Sampling distribution (changes with sample_size)
        ax2.patch.set_facecolor(BAND_COLOR)
        sample_means = [np.random.choice(population, size=sample_size).mean() 
                       for _ in range(n_samples)]
        
        counts2, bins2, patches2 = ax2.hist(
            sample_means, 
            bins=30, 
            alpha=0.85, 
            color=CURVE_COLOR,
            edgecolor='#17003b', 
            density=True,
            linewidth=2
        )
        
        # Apply gradient to sampling distribution histogram
        for i, patch in enumerate(patches2):
            color_idx = i % len(MEAN_GRADIENT)
            patch.set_facecolor(MEAN_GRADIENT[color_idx])
            patch.set_alpha(0.8)
        
        # Normal curve overlay with glow effect
        mu = np.mean(sample_means)
        sigma = np.std(sample_means)
        x = np.linspace(min(sample_means), max(sample_means), 200)
        y_normal = norm.pdf(x, mu, sigma)
        
        # Draw glowing normal curve (multiple layers for glow effect)
        ax2.plot(x, y_normal, '-', linewidth=4, color=NORMAL_CURVE_COLOR, 
                alpha=0.3, zorder=10)
        ax2.plot(x, y_normal, '-', linewidth=2.5, color=NORMAL_CURVE_COLOR, 
                alpha=0.7, zorder=11)
        ax2.plot(x, y_normal, '-', linewidth=1.5, color='white', 
                alpha=0.9, zorder=12)
        
        # Mean line with glow
        ax2.axvline(mu, color=TITLE_COLOR, linestyle='--', linewidth=3, 
                   alpha=0.4, zorder=8)
        ax2.axvline(mu, color=TITLE_COLOR, linestyle='--', linewidth=2, 
                   alpha=0.9, zorder=9,
                   label=f'μ={mu:.2f}, σ={sigma:.2f}')
        
        ax2.set_title(f'Sampling Distribution (n={sample_size}, samples={n_samples})', 
                     fontweight='bold', color=TITLE_COLOR, fontsize=16)
        ax2.set_xlabel('Sample Mean', color=LABEL_COLOR, fontsize=13)
        ax2.set_ylabel('Density', color=LABEL_COLOR, fontsize=13)
        ax2.legend(facecolor=BAND_COLOR, edgecolor=TITLE_COLOR, 
                  fontsize=11, labelcolor=LABEL_COLOR, framealpha=0.9)
        ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # Add frame counter
        fig.text(0.5, 0.02, f'Sample Size: {sample_size}', 
                ha='center', color=TITLE_COLOR, fontsize=14, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.03, 1, 1])
        return ax1, ax2
    
    # Create animation
    anim = FuncAnimation(
        fig, 
        update, 
        frames=len(sample_sizes), 
        init_func=init,
        interval=200,  # 200ms between frames
        blit=False, 
        repeat=True
    )
    
    # Save as GIF
    print(f"Creating GIF with {len(sample_sizes)} frames...")
    writer = PillowWriter(fps=5, metadata=dict(artist='CLT Demo'), bitrate=1800)
    anim.save(output_filename, writer=writer, dpi=100)
    print(f"✓ GIF saved as {output_filename}")
    
    plt.close()
    return anim


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Create population
    population = np.random.randint(1, 101, size=1000)
    
    # Generate and save as GIF
    print("Creating Interactive CLT Animation as GIF")
    print("This shows how sample size affects the sampling distribution")
    
    anim = create_clt_gif(population, output_filename='clt_interactive_techy.gif')
    
    print("Animation created successfully!")
    print("For Medium blog:")
    print(" - Drag and drop the GIF directly into Medium editor")
    print(" - Or use the image upload button")
