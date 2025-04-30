import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initial values for amplitude, frequency, and phase
initial_mean = 0.1
initial_amplitude = 1.0
initial_frequency = 1.0
initial_start = 0.0

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)  # Adjust the bottom to make room for sliders

# Generate x values from 0 to 2*pi with a step of 0.01
x = np.arange(0, 2 * np.pi, 0.01)

# Initial sine wave with default parameters
y = initial_amplitude * np.sin(2*np.pi * (x-initial_start)/initial_frequency) + initial_mean
line, = ax.plot(x, y, label=f"A={initial_amplitude:0.5f}, \nP={initial_frequency:0.5f}, \nx0={initial_start:0.5f}, \ny0={initial_mean:0.5f}",color="blue")
marker, = ax.plot(initial_start, initial_mean, 'ro')  # red dot
label = ax.text(initial_start, initial_mean + 0.3, "Start x0", ha='center')


ax.legend()

# Set plot labels
ax.set_title("Sine wave: y = A sin(2 pi (x-x0)/P ) + y0")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc='upper right')
ax.set_ylim(-1.5,1.5)

# Define the positions and sizes for sliders
axcolor = 'lightgoldenrodyellow'
ax_mean = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_amplitude = plt.axes([0.25, 0.0666, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.25, 0.0333, 0.65, 0.03], facecolor=axcolor)
ax_start = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)

# Create sliders for amplitude, frequency, and phase
mean_slider = Slider(ax_mean, 'Mean y0', -1.0, 1.0, valinit=initial_mean)
amplitude_slider = Slider(ax_amplitude, 'Amplitude A', -2.0, 2.0, valinit=initial_amplitude)
frequency_slider = Slider(ax_frequency, 'Period P', -1.0, 5.0, valinit=initial_frequency)
start_slider = Slider(ax_start, 'Start x0', -2, 2, valinit=initial_start)

# Function to update the plot when sliders are changed
def update(val):
    mean = mean_slider.val
    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    start = start_slider.val

    # Update the sine wave with new parameters
    y = amplitude * np.sin(2*np.pi* (x-start)/frequency) + mean
    line.set_ydata(y)

    # Update the legend
    line.set_label(f"A={amplitude:0.5f}, \nP={frequency:0.5f}, \nx0={start:0.5f}, \ny0={mean:0.5f}")
    marker.set_data((start,), (mean,))
    label.set_position((start,mean + 0.3))

    ax.legend(loc='upper right')

    #ax.set_ylim([-amplitude*1.1,amplitude*1.1])
    ax.set_ylim(-1.5,1.5)

    # Redraw the plot
    fig.canvas.draw_idle()

# Attach the update function to the sliders
mean_slider.on_changed(update)
amplitude_slider.on_changed(update)
frequency_slider.on_changed(update)
start_slider.on_changed(update)

# Show the plot
plt.show()
