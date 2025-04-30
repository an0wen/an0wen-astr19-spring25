import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cm as cm
from scipy.stats import t


cmap_turbo = cm.get_cmap('turbo')

# Parameters
n_data = 20 # number of data points
y_noise = 1.0 # random noise on y
y_sigma = 3.0 # uncertainty on y
m_true = 2.5 # true slope
b_true = 1.0 # true intercept

# Generate some linear data with scatter
#np.random.seed(0)
x = np.linspace(0, 10, n_data)
y_true = m_true * x + b_true
noise = np.random.normal(0, y_noise, size=x.size)
y = y_true + noise

# Define slope and intercept ranges for the chi-square map
slope_range = np.linspace(-5, 5, 100)
intercept_range = np.linspace(-5, 5, 100)

# Precompute chi-square grid
chi2_grid = np.zeros((intercept_range.size, slope_range.size))
for i, b in enumerate(intercept_range):
    for j, m in enumerate(slope_range):
        model = m * x + b
        chi2_grid[i, j] = np.sum(((y - model) / y_sigma) ** 2)

# Avoid log(0) by setting a minimum value
chi2_grid = np.maximum(chi2_grid, 1e-5)

# Find best fit parameters
best_idx = np.unravel_index(np.argmin(chi2_grid), chi2_grid.shape)
best_intercept = intercept_range[best_idx[0]]
best_slope = slope_range[best_idx[1]]

# Fit linear regression to get standard error
X = np.vstack([x, np.ones_like(x)]).T
params, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
y_fit = params[0] * x + params[1]
s_err = np.sqrt(np.sum((y - y_fit)**2) / (len(x) - 2))

t_val = t.ppf(0.99, df=len(x)-2)
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
conf_int = t_val * s_err * np.sqrt(1/len(x) + (x - x_mean)**2 / Sxx)
upper = y_fit + conf_int
lower = y_fit - conf_int

# Create the figure
fig, (ax_data, ax_chi2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Left panel: data and initial fit
line, = ax_data.plot(x, 2.5 * x + 1.0, 'r-', label='Model')
best_fit_line, = ax_data.plot(x, best_slope * x + best_intercept, 'g--', label='Best Fit')
#ax_data.fill_between(x, lower, upper, color='green', alpha=0.2, label='95% Confidence Interval')
ax_data.errorbar(x, y, yerr=y_sigma, fmt='o', label='Data')
ax_data.set_xlabel('x')
ax_data.set_ylabel('y')
ax_data.legend()

# Right panel: chi-square colormap
cmap = ax_chi2.imshow(np.log10(chi2_grid)**0.1, extent=[slope_range[0], slope_range[-1], intercept_range[0], intercept_range[-1]], 
                      origin='lower', aspect='auto', cmap='turbo')
fig.colorbar(cmap, ax=ax_chi2, label='log10(Chi-square)')
marker, = ax_chi2.plot([], [], 'rx', markersize=12, markeredgewidth=2)
ax_chi2.scatter(best_slope, best_intercept,label='Best Fit',facecolors='none', edgecolors='green', s=100)

ax_chi2.set_xlabel('Slope')
ax_chi2.set_ylabel('Intercept')

# Sliders
ax_slope = plt.axes([0.15, 0.1, 0.65, 0.03])
ax_intercept = plt.axes([0.15, 0.05, 0.65, 0.03])

slope_slider = Slider(ax_slope, 'Slope', slope_range[0], slope_range[-1], valinit=0)
intercept_slider = Slider(ax_intercept, 'Intercept', intercept_range[0], intercept_range[-1], valinit=0.0)

# Update function
def update(val):
    m = slope_slider.val
    b = intercept_slider.val
    
    # Update line
    line.set_ydata(m * x + b)
    
    # Update marker on chi-square map
    marker.set_data((m,), (b,))
    
    fig.canvas.draw_idle()

slope_slider.on_changed(update)
intercept_slider.on_changed(update)

# Initial marker position
update(None)

plt.show()
