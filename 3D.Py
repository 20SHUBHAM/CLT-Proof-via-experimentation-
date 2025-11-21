import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

# Techy cyberpunk color palette
GRID_COLOR = '#0d1117'
TITLE_COLOR = '#00ffe7'
LABEL_COLOR = '#ffde57'
BAND_COLOR = '#1a1f2e'

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

def clt_3d_surface_gif(population, max_sample_size=50, n_samples=500, 
                       output_filename='clt_3d_surface.gif'):
    """
    3D visualization with rotation animation showing how distribution 
    changes with sample size
    """
    fig = plt.figure(figsize=(12, 8), facecolor=GRID_COLOR)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(BAND_COLOR)
    
    # Calculate data once (don't recalculate for each frame)
    sample_sizes = np.arange(5, max_sample_size + 1, 5)
    x_range = np.linspace(20, 80, 100)
    
    # Create meshgrid
    X, Y = np.meshgrid(sample_sizes, x_range)
    Z = np.zeros_like(X, dtype=float)
    
    print("Calculating surface data...")
    # Calculate density for each sample size and x value
    for i, sample_size in enumerate(sample_sizes):
        sample_means = [np.random.choice(population, size=sample_size).mean() 
                       for _ in range(n_samples)]
        mu = np.mean(sample_means)
        sigma = np.std(sample_means)
        
        # Calculate normal PDF for each x point
        for j, x_val in enumerate(x_range):
            Z[j, i] = norm.pdf(x_val, mu, sigma)
    
    # Initial plot
    def init():
        ax.clear()
        return fig,
    
    def update(frame):
        ax.clear()
        ax.set_facecolor(BAND_COLOR)
        
        # Calculate rotation angle
        angle = frame * 2  # Rotate 2 degrees per frame
        
        # Plot surface with cyberpunk colormap
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.85, 
                              edgecolor='none', antialiased=True,
                              linewidth=0, rcount=50, ccount=50)
        
        # Add contour lines at the bottom
        ax.contour(X, Y, Z, zdir='z', offset=0, cmap='cool', 
                  levels=10, linewidths=1.5, alpha=0.6)
        
        # Set labels with techy colors
        ax.set_xlabel('Sample Size', fontsize=12, fontweight='bold', 
                     color=LABEL_COLOR, labelpad=10)
        ax.set_ylabel('Sample Mean', fontsize=12, fontweight='bold', 
                     color=LABEL_COLOR, labelpad=10)
        ax.set_zlabel('Density', fontsize=12, fontweight='bold', 
                     color=LABEL_COLOR, labelpad=10)
        
        # Set title
        ax.set_title('CLT: Distribution Evolution with Sample Size\n(3D Surface Plot)', 
                    fontsize=14, fontweight='bold', color=TITLE_COLOR, pad=20)
        
        # Set viewing angle (rotating)
        ax.view_init(elev=25, azim=angle)
        
        # Grid styling
        ax.grid(True, alpha=0.3, color='#2A3459')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('#2A3459')
        ax.yaxis.pane.set_edgecolor('#2A3459')
        ax.zaxis.pane.set_edgecolor('#2A3459')
        
        # Tick colors
        ax.tick_params(colors=LABEL_COLOR, labelsize=9)
        
        # Add rotation info
        fig.text(0.5, 0.02, f'Rotation: {angle}°', 
                ha='center', color=TITLE_COLOR, fontsize=11, fontweight='bold')
        
        return fig,
    
    # Create animation (full 360° rotation)
    n_frames = 180  # 180 frames * 2 degrees = 360° rotation
    print(f"Creating rotating 3D animation with {n_frames} frames...")
    
    anim = FuncAnimation(
        fig, 
        update, 
        frames=n_frames,
        init_func=init,
        interval=50,  # 50ms between frames
        blit=False,
        repeat=True
    )
    
    # Save as GIF
    print(f"Saving GIF (this may take a minute)...")
    writer = PillowWriter(fps=20, metadata=dict(artist='CLT 3D Demo'), bitrate=1800)
    anim.save(output_filename, writer=writer, dpi=100)
    print(f"✓ GIF saved as {output_filename}")
    
    plt.close()
    return anim


def clt_3d_surface_static(population, max_sample_size=50, n_samples=500, 
                          output_filename='clt_3d_static.png'):
    """
    Static 3D visualization with techy styling (for comparison)
    """
    fig = plt.figure(figsize=(12, 8), facecolor=GRID_COLOR)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(BAND_COLOR)
    
    sample_sizes = np.arange(5, max_sample_size + 1, 5)
    x_range = np.linspace(20, 80, 100)
    
    # Create meshgrid
    X, Y = np.meshgrid(sample_sizes, x_range)
    Z = np.zeros_like(X, dtype=float)
    
    # Calculate density for each sample size and x value
    for i, sample_size in enumerate(sample_sizes):
        sample_means = [np.random.choice(population, size=sample_size).mean() 
                       for _ in range(n_samples)]
        mu = np.mean(sample_means)
        sigma = np.std(sample_means)
        
        # Calculate normal PDF for each x point
        for j, x_val in enumerate(x_range):
            Z[j, i] = norm.pdf(x_val, mu, sigma)
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.85, 
                          edgecolor='none', antialiased=True)
    
    # Add contour lines
    ax.contour(X, Y, Z, zdir='z', offset=0, cmap='cool', 
              levels=10, linewidths=1.5, alpha=0.6)
    
    ax.set_xlabel('Sample Size', fontsize=12, fontweight='bold', 
                 color=LABEL_COLOR, labelpad=10)
    ax.set_ylabel('Sample Mean', fontsize=12, fontweight='bold', 
                 color=LABEL_COLOR, labelpad=10)
    ax.set_zlabel('Density', fontsize=12, fontweight='bold', 
                 color=LABEL_COLOR, labelpad=10)
    ax.set_title('CLT: Distribution Evolution with Sample Size', 
                fontsize=14, fontweight='bold', color=TITLE_COLOR, pad=20)
    
    # Grid and pane styling
    ax.grid(True, alpha=0.3, color='#2A3459')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#2A3459')
    ax.yaxis.pane.set_edgecolor('#2A3459')
    ax.zaxis.pane.set_edgecolor('#2A3459')
    ax.tick_params(colors=LABEL_COLOR, labelsize=9)
    
    # Colorbar
    cbar = fig.colorbar(surf, shrink=0.5, aspect=5, pad=0.1)
    cbar.ax.tick_params(colors=LABEL_COLOR, labelsize=9)
    cbar.set_label('Density', color=LABEL_COLOR, fontweight='bold')
    
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
    
    print("Creating 3D CLT Surface Visualization")
    print("This shows how the distribution shape changes with sample size\n")
    
    # Generate rotating GIF
    anim = clt_3d_surface_gif(
        population, 
        max_sample_size=50, 
        n_samples=500,
        output_filename='clt_3d_rotating_techy.gif'
    )
    
    # Optional: Generate static high-quality image
    # clt_3d_surface_static(population, max_sample_size=50, 
    #                       output_filename='clt_3d_techy.png')
    
    print("3D Animation created successfully!")
    print("For Medium blog:")
    print("   - Upload the rotating GIF directly to Medium")
    print("   - The 360° rotation shows CLT from all angles")
