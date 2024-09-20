######################################################################################
import colorsys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(rc={'figure.figsize':(18, 18)}, font_scale=1.8, style="white")
######################################################################################

def test_random_rgb_colors(num_colors, rgbs=None):
    def rgb_to_color_name(rgb):
        r, g, b = rgb[:3]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        hue_angle = h * 360
        if l > 0.9: return 'white', hue_angle, l, s
        elif l < 0.09: return 'black', hue_angle, l, s
        elif s < 0.09: return 'grey', hue_angle, l, s
        elif hue_angle < 9: return 'red', hue_angle, l, s
        elif hue_angle < 45: return 'orange', hue_angle, l, s
        elif hue_angle < 64: return 'yellow', hue_angle, l, s
        elif hue_angle < 160: return 'green', hue_angle, l, s
        elif hue_angle < 236: return 'blue', hue_angle, l, s
        elif hue_angle < 293: return 'purple', hue_angle, l, s
        elif hue_angle < 350: return 'pink', hue_angle, l, s
        elif hue_angle >= 350: return 'red', hue_angle, l, s
    ################################################
    if rgbs: num_colors = len(rgbs) 
    cols = 5
    rows = num_colors // cols + (1 if num_colors % cols else 0)
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2), dpi=100)
    axs = axs.flatten()
    if not rgbs:
        rgbs = []
        for i in range(num_colors):
            rgb = np.random.rand(3)
            rgbs.append(rgb)
    for i in range(num_colors):
        rgb = rgbs[i]
        color_name, hue_angle, l, s = rgb_to_color_name(rgb)
        hue_angle = int(np.round(hue_angle, 0))
        l = np.round(l, 2)
        s = np.round(s, 2)
        ax = axs[i]
        ax.imshow([[rgb]])
        ax.axis('off')
        ax.text(0.5, 0.5, color_name, fontsize=12, 
                ha='center', va='center', color="black",
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
        ax.text(0.5, 0.9, f'{hue_angle}, {l}, {s}', fontsize=10, 
                ha='center', va='top', color="black",
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
        ax.set_title(f'{i}', fontsize=12)
    for i in range(num_colors, rows * cols):
        axs[i].axis('off')
    plt.show()
    return rgbs

######################################################################################

rgbs = test_random_rgb_colors(25)

# rgbs = test_random_rgb_colors(25, rgbs)

######################################################################################