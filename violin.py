import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns

# Techy cyberpunk color palette
GRID_COLOR = '#0d1117'
TITLE_COLOR = '#00ffe7'
LABEL_COLOR = '#ffde57'
BAND_COLOR = '#1a1f2e'
VIOLIN_COLORS = ['#4c47e4', '#792ec7', '#be23c4', '#f174ea', '#ff24a5', '#1ef9d3']

# Set matplotlib style globally
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = GRID_COLOR
plt.rcParams['axes.facecolor'] = BAND_COLOR
plt.rcParams['text.color'] = LABEL_COLOR
plt.rcParams['axes.labelcolor'] = LABEL_COLOR
plt.rcParams['xtick.color'] = LABEL_COLOR
plt.rcParams['ytick.color'] = LABEL_COLOR
plt.rcParams['grid.color'] = '#2A3459'
plt.rcParams['font.family'] = 'DejaVu Sans'

def clt_violin_comparison_gif(population, max_sample_size=100, 
                               output_filename='clt_violin_techy.gif'):
    """
    Animated violin plots showing distribution shape evolution as sample size increases
    """
    fig, ax = plt.subplots(figsize=(14, 7), facecolor=GRID_COLOR)
    
    # Generate all sample sizes to animate through
    sample_size_progression = list(range(5, max_sample_size + 1, 5))
    
    def init():
        ax.clear()
        return fig,
    
    def update(frame):
        ax.clear()
        ax.set_facecolor(BAND_COLOR)
        
        # Get current sample sizes (progressively add more)
        current_sample_sizes = sample_size_progression[:frame+1]
        
        # Show at least 4 violin plots, max 8
        if len(current_sample_sizes) <= 4:
            display_sizes = current_sample_sizes
        else:
            # Select evenly distributed sample sizes
            indices = np.linspace(0, len(current_sample_sizes)-1, 
                                min(8, len(current_sample_sizes)), dtype=int)
            display_sizes = [current_sample_sizes[i] for i in indices]
        
        sample_means_list = []
        labels = []
        
        # Generate sample means for each sample size
        for size in display_sizes:
            means = [np.random.choice(population, size=size).mean() 
                    for _ in range(1000)]
            sample_means_list.append(means)
            labels.append(f'n={size}')
        
        # Create violin plot
        parts = ax.violinplot(sample_means_list, 
                             positions=range(len(display_sizes)), 
                             showmeans=True, 
                             showmedians=True,
                             widths=0.7)
        
        # Style the violin bodies with cyberpunk colors
        for i, pc in enumerate(parts['bodies']):
            color_idx = i % len(VIOLIN_COLORS)
            pc.set_facecolor(VIOLIN_COLORS[color_idx])
            pc.set_edgecolor('#ffffff')
            pc.set_linewidth(1.5)
            pc.set_alpha(0.8)
        
        # Style the mean/median/extrema lines
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
            if partname in parts:
                vp = parts[partname]
                vp.set_edgecolor(TITLE_COLOR)
                vp.set_linewidth(2)
                vp.set_alpha(0.9)
        
        # Set labels and title
        ax.set_xticks(range(len(display_sizes)))
        ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
        ax.set_xlabel('Sample Size', fontsize=13, fontweight='bold', color=LABEL_COLOR)
        ax.set_ylabel('Sample Mean', fontsize=13, fontweight='bold', color=LABEL_COLOR)
        ax.set_title('CLT: Distribution Shape Evolution\n(Violin Plots)', 
                    fontsize=16, fontweight='bold', color=TITLE_COLOR, pad=20)
        
        # Grid styling
        ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(LABEL_COLOR)
        ax.spines['bottom'].set_color(LABEL_COLOR)
        
        # Add progress indicator
        progress_text = f'Progress: {frame+1}/{len(sample_size_progression)} | Max n={current_sample_sizes[-1]}'
        fig.text(0.5, 0.02, progress_text, 
                ha='center', color=TITLE_COLOR, fontsize=11, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.04, 1, 1])
        return fig,
    
    # Create animation
    n_frames = len(sample_size_progression)
    print(f"Creating violin plot animation with {n_frames} frames...")
    
    anim = FuncAnimation(
        fig, 
        update, 
        frames=n_frames,
        init_func=init,
        interval=150,  # 150ms between frames
        blit=False,
        repeat=True
    )
    
    # Save as GIF
    print(f"Saving GIF (this may take a moment)...")
    writer = PillowWriter(fps=7, metadata=dict(artist='CLT Violin Demo'), bitrate=1800)
    anim.save(output_filename, writer=writer, dpi=100)
    print(f"✓ GIF saved as {output_filename}")
    
    plt.close()
    return anim


def clt_violin_comparison_static(population, sample_sizes=[5, 15, 30, 50, 100],
                                 output_filename='clt_violin_static_techy.png'):
    """
    Static version with techy styling (for comparison)
    """
    fig, ax = plt.subplots(figsize=(14, 7), facecolor=GRID_COLOR)
    ax.set_facecolor(BAND_COLOR)
    
    sample_means_list = []
    labels = []
    
    for size in sample_sizes:
        means = [np.random.choice(population, size=size).mean() 
                for _ in range(1000)]
        sample_means_list.append(means)
        labels.append(f'n={size}')
    
    # Create violin plot
    parts = ax.violinplot(sample_means_list, 
                         positions=range(len(sample_sizes)), 
                         showmeans=True, 
                         showmedians=True,
                         widths=0.7)
    
    # Color the violins with cyberpunk colors
    for i, pc in enumerate(parts['bodies']):
        color_idx = i % len(VIOLIN_COLORS)
        pc.set_facecolor(VIOLIN_COLORS[color_idx])
        pc.set_edgecolor('#ffffff')
        pc.set_linewidth(1.5)
        pc.set_alpha(0.8)
    
    # Style the mean/median/extrema lines
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
        if partname in parts:
            vp = parts[partname]
            vp.set_edgecolor(TITLE_COLOR)
            vp.set_linewidth(2)
            vp.set_alpha(0.9)
    
    ax.set_xticks(range(len(sample_sizes)))
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
    ax.set_xlabel('Sample Size', fontsize=13, fontweight='bold', color=LABEL_COLOR)
    ax.set_ylabel('Sample Mean', fontsize=13, fontweight='bold', color=LABEL_COLOR)
    ax.set_title('CLT: Distribution Shape Evolution\n(Violin Plots)', 
                fontsize=16, fontweight='bold', color=TITLE_COLOR, pad=20)
    ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(LABEL_COLOR)
    ax.spines['bottom'].set_color(LABEL_COLOR)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, facecolor=GRID_COLOR)
    print(f"✓ Static image saved as {output_filename}")
    plt.show()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Create population
    population = np.random.randint(1, 101, size=1000)
    
    print(" Creating Violin Plot CLT Visualization")
    print("This shows how distribution shape tightens with sample size\n")
    
    # Generate animated GIF
    anim = clt_violin_comparison_gif(
        population, 
        max_sample_size=100,
        output_filename='clt_violin_animated_techy.gif'
    )
    
    # Optional: Generate static high-quality image
    print("\nGenerating static comparison...")
    clt_violin_comparison_static(
        population, 
        sample_sizes=[5, 15, 30, 50, 100],
        output_filename='clt_violin_static_techy.png'
    )
    
    print("Violin plot visualizations created successfully!")
    print("For Medium blog:")
    print("   - Upload the animated GIF to show progressive evolution")
    print("   - Use the static PNG for a clean comparison view")
