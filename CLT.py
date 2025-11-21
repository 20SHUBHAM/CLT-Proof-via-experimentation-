import numpy as np

s = np.random.randint(1,101, size=1000)
sample_means = []  # use a list; append means, convert to array after loop
for i in range(10):

    sample_30_random = np.random.choice(s, size=30, replace=True)

    # minimal fix: append mean instead of using nonexistent NumPy insert
    sample_means.append(np.mean(sample_30_random))

# convert to ndarray for downstream NumPy ops
sample_means = np.array(sample_means)



import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_clt_results(sample_means, title="Central Limit Theorem Visualization"):
    """
    Plot histogram of sample means with normal distribution overlay
    """
    plt.figure(figsize=(12, 6))
    
    # Plot histogram with density=True for proper comparison
    plt.hist(sample_means, bins=30, density=True, alpha=0.7, 
             color='steelblue', edgecolor='black', label='Sample Means')
    
    # Calculate statistics for normal curve
    mu = sample_means.mean()
    sigma = sample_means.std()
    
    # Generate x values for normal curve
    x = np.linspace(sample_means.min(), sample_means.max(), 100)
    
    # Plot normal distribution overlay
    normal_curve = norm.pdf(x, mu, sigma)
    plt.plot(x, normal_curve, 'r-', linewidth=2, 
             label=f'Normal Curve\nmu={mu:.2f}, sigma={sigma:.2f}')
    
    # Add vertical lines for mean and +/- 1, +/- 2 standard deviations
    plt.axvline(mu, color='green', linestyle='--', linewidth=2, 
                label=f'Mean = {mu:.2f}')
    plt.axvline(mu + sigma, color='orange', linestyle=':', 
                label=f'mu +/- sigma = {mu+sigma:.2f}')
    plt.axvline(mu - sigma, color='orange', linestyle=':')
    plt.axvline(mu + 2*sigma, color='purple', linestyle=':', 
                label=f'mu +/- 2*sigma = {mu+2*sigma:.2f}')
    plt.axvline(mu - 2*sigma, color='purple', linestyle=':')
    
    # Formatting
    plt.xlabel('Sample Mean', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    return plt.show()



plot_clt_results(sample_means)
