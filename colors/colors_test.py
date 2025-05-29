import colors_class as cc
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider

#illuminant_D65 = cc.xyz_from_xy(1., 0.0)
#cs_hdtv = cc.ColourSystem(red=cc.xyz_from_xy(0.67, 0.33),
#                       green=cc.xyz_from_xy(0.21, 0.71),
#                       blue=cc.xyz_from_xy(0.15, 0.06),
#                       white=illuminant_D65)


#print(cs_hdtv.xyz_to_rgb(cc.xyz_from_xy(0.3127, 0.3291), out_fmt='html'))

#define a color as RGBL (L is brightness)
#my_xyz = ColourSystem(0.5,0.5,0.5,0.5)
#my_rgb = my_xyz.xyz_to_rgb(xyz, out_fmt='html')
#print(my_rgb)

# Example usage:
#xyz_color = [0.1, 0.0, 0.9]  # Example XYZ color values
#desired_luminance = 0.1  # Example desired luminance level
#html_color = cc.xyz_to_html_color(xyz_color, desired_luminance)
#print("XYZ:", xyz_color)
#print("Desired Luminance:", desired_luminance)
#print("HTML RGB:", html_color)

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def html_color_function(param1, param2, param3, param4):
    # Function to generate HTML color code based on parameters
    x = param1/(param1+param2+param3)
    y = param2/(param1+param2+param3)
    z = param3/(param1+param2+param3)
    html_color = cc.xyz_to_html_color([x, y, z], param4)
    return html_color

def update(val):
    # Update the figure with new background color
    fig.patch.set_facecolor(html_color_function(slider_r.val, slider_g.val, slider_b.val, slider_a.val))
    fig.canvas.draw_idle()

# Initial parameter values
initial_params = [0.5, 0.5, 0.5, 1.0]

# Create the figure
fig = plt.figure(figsize=(5, 5))
fig.patch.set_facecolor(html_color_function(*initial_params))

# Create sliders
ax_r = plt.axes([0.1, 0.05, 0.65, 0.03])
slider_r = Slider(ax_r, 'Red', 0, 1, valinit=initial_params[0])
ax_g = plt.axes([0.1, 0.1, 0.65, 0.03])
slider_g = Slider(ax_g, 'Green', 0, 1, valinit=initial_params[1])
ax_b = plt.axes([0.1, 0.15, 0.65, 0.03])
slider_b = Slider(ax_b, 'Blue', 0, 1, valinit=initial_params[2])
ax_a = plt.axes([0.1, 0.2, 0.65, 0.03])
slider_a = Slider(ax_a, 'Alpha', 0, 2, valinit=initial_params[3])

# Update figure when sliders are changed
slider_r.on_changed(update)
slider_g.on_changed(update)
slider_b.on_changed(update)
slider_a.on_changed(update)

# Hide axes
plt.axis('off')

plt.show()

