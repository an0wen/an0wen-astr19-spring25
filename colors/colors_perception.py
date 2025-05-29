import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
from matplotlib.patches import Rectangle

# Create figure
fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')

# Create sliders
ax_slider_r = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor='red')
ax_slider_g = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='green')
ax_slider_b = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor='blue')
ax_slider_l = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor='white')

slider_r = Slider(ax_slider_r, 'R', 0, 1, valinit=0.5)
slider_g = Slider(ax_slider_g, 'G', 0, 1, valinit=0.5)
slider_b = Slider(ax_slider_b, 'B', 0, 1, valinit=0.5)
slider_l = Slider(ax_slider_l, 'L', 0, 1, valinit=1)

# Create textbox
#ax_textbox = plt.axes([0.1, 0.25, 0.8, 0.1])
#textbox = TextBox(ax_textbox, 'XYZ:', initial='(0.00, 0.00, 0.00)', color=(1, 1, 1, 1.0))

ax_textbox1 = plt.axes([0.1, 0.3, 0.2, 0.1])
ax_textbox2 = plt.axes([0.4, 0.3, 0.2, 0.1])
ax_textbox3 = plt.axes([0.7, 0.3, 0.2, 0.1])

textbox1 = TextBox(ax_textbox1, '', textalignment='center', initial=f'(X: {0:.2f})', color='white')
textbox2 = TextBox(ax_textbox2, '', textalignment='center', initial=f'(Y: {0:.2f})', color='white')
textbox3 = TextBox(ax_textbox3, '', textalignment='center', initial=f'(Z: {0:.2f})', color='white')



# Create initial rectangle
rect = Rectangle((0, 0), 1, 1, color=(0.5, 0.5, 0.5, 1.0))  # RGBA format with alpha=1.0
ax.add_patch(rect)

# Create initial rectangles
rect1 = Rectangle((0.1, 0.4), 0.2, 0.2, facecolor='red', edgecolor='black', alpha=1)
rect2 = Rectangle((0.4, 0.4), 0.2, 0.2, facecolor='green', edgecolor='black', alpha=1)
rect3 = Rectangle((0.7, 0.4), 0.2, 0.2, facecolor='blue', edgecolor='black', alpha=1)
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)

# Function to update the plot
def update(val):
    l = slider_l.val
    r = slider_r.val * l
    g = slider_g.val * l
    b = slider_b.val * l
    
    #ax.clear()
    #ax.add_patch(Rectangle((0, 0), 1, 1, color=(r, g, b, 1.0)))
    
    # Convert RGB to XYZ
    r_lin = r if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    g_lin = g if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    b_lin = b if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
    
    x = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
    y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
    z = r_lin * 0.0193339 + g_lin * 0.1191920 + b_lin * 0.9503041
    
    #textbox.set_val(f'({x:.2f}, {y:.2f}, {z:.2f})')

    textbox1.set_val(f'(X: {x:.2f})')
    textbox2.set_val(f'(Y: {y:.2f})')
    textbox3.set_val(f'(Z: {z:.2f})')
    
    # Update heights of rectangles based on XYZ values
    rect1.set_height(x*0.5)
    rect2.set_height(y*0.5)
    rect3.set_height(z*0.5)
    rect.set_color((r,g,b))

    ax.axis('off')
    plt.draw()

# Connect sliders to update function
slider_r.on_changed(update)
slider_g.on_changed(update)
slider_b.on_changed(update)
slider_l.on_changed(update)

plt.show()
