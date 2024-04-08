import seaborn as sns

def heatmap_color(value):
    """
    Assigns a warm heatmap color based on the given value using colors similar to "rocket" palette in seaborn.
    """
    rocket_palette = sns.color_palette("flare", as_cmap=True)
    rgba_color = rocket_palette(value)
    rgb_color = rgba_color[:3]  # Extract RGB values, excluding alpha
    hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]*255), int(rgb_color[1]*255), int(rgb_color[2]*255))
    return hex_color

if __name__ == '__main__':
    # Example usage:
    # Test the function with a value between 0 and 1
    value = 0.5  # Example value
    color = heatmap_color(value)
    print(color)  # This will return the hexadecimal RGB color code