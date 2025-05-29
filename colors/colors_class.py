def xyz_to_rgb(xyz):
    # Conversion matrix from XYZ to sRGB
    xyz_to_rgb_matrix = [
        [3.2406, -1.5372, -0.4986],
        [-0.9689, 1.8758, 0.0415],
        [0.0557, -0.2040, 1.0570]
    ]
    
    # Convert XYZ to linear RGB
    linear_rgb = [
        xyz_to_rgb_matrix[0][0] * xyz[0] + xyz_to_rgb_matrix[0][1] * xyz[1] + xyz_to_rgb_matrix[0][2] * xyz[2],
        xyz_to_rgb_matrix[1][0] * xyz[0] + xyz_to_rgb_matrix[1][1] * xyz[1] + xyz_to_rgb_matrix[1][2] * xyz[2],
        xyz_to_rgb_matrix[2][0] * xyz[0] + xyz_to_rgb_matrix[2][1] * xyz[1] + xyz_to_rgb_matrix[2][2] * xyz[2]
    ]
    
    # Companding (gamma correction) for linear RGB
    companded_rgb = [0, 0, 0]
    for i in range(3):
        if linear_rgb[i] <= 0.0031308:
            companded_rgb[i] = 12.92 * linear_rgb[i]
        else:
            companded_rgb[i] = 1.055 * (linear_rgb[i] ** (1.0 / 2.4)) - 0.055
    
    # Scale to 8-bit RGB
    rgb = [int(round(x * 255)) for x in companded_rgb]
    
    return rgb

def calculate_luminance(xyz):
    # Calculate luminance Y from XYZ
    return 116 * xyz[1] - 16 if xyz[1] > 0.008856 else 903.3 * xyz[1]

def adjust_brightness(rgb, desired_luminance):
    # Calculate luminance of the RGB color
    luminance = 0.2126 * rgb[0] / 255 + 0.7152 * rgb[1] / 255 + 0.0722 * rgb[2] / 255
    
    if luminance == 0:
        return [0, 0, 0]  # Return black if the color is black
    
    # Adjust RGB values to match the desired luminance
    adjusted_rgb = [int(round(value * (desired_luminance / luminance))) for value in rgb]
    
    # Clamp the adjusted RGB values within the valid range
    adjusted_rgb = [min(max(value, 0), 255) for value in adjusted_rgb]
    
    return adjusted_rgb


def xyz_to_html_color(xyz, desired_luminance=100):
    rgb = xyz_to_rgb(xyz)
    
    # Check if the RGB color is black (luminance = 0)
    if sum(rgb) == 0:
        return "#000000"
    
    adjusted_rgb = adjust_brightness(rgb, desired_luminance)
    return "#{:02X}{:02X}{:02X}".format(adjusted_rgb[0], adjusted_rgb[1], adjusted_rgb[2])

