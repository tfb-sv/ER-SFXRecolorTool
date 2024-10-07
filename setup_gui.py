#####################################################################################
import re
import sys
import json
import customtkinter as ctk
from utils_recolor import *
import recolor_sfx
#####################################################################################

config_fp = "paths_config.json"
mission_fn = "z.recolor_mission.json"
assert_text = f"The file {mission_fn} could not be found in the program directory. The program is ABORTED."
assert os.path.exists(mission_fn), assert_text
with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
sfx_ids = mission_input["sfx_ids"]

version_str = "3.1"
year_str = "2024"
owner_str = "ineedthetail"
copyright_text = f"© {year_str} {owner_str}. All rights reserved.\nv{version_str}"

padx_size, pady_size = 10, 10
pad_top, pad_bot = 20, 20
pad_l, pad_r = 40, 40
ph_text = "255, 255, 255"
default_color = "transparent"
theme_color1 = None
theme_color2 = "purple"
text_color1 = "white"
text_color2 = "white"

#####################################################

def on_closing():
    root.destroy()
    sys.exit(0)

#####################################################
    
def update_color_box(entry, color_box, color_box_label):
    color_value = entry.get()
    try:
        color_value += ", 1.0"
        is_rgba, hex_color = convert_color2hex(color_value)
        if is_rgba:
            color_box.configure(fg_color=hex_color)
            color_box_label.configure(text="", bg_color=hex_color)
        else: 
            color_box.configure(fg_color=default_color)
            color_box_label.configure(text="Not Valid", bg_color=default_color)
    except ValueError: 
        color_box.configure(fg_color=default_color)
        if color_value == "": color_box_label.configure(text="")
        else: color_box_label.configure(text="Not Valid", bg_color=default_color)
        
#####################################################

def toggle_color_frame():
    if toggle_var.get() == 1: 
        color_frame.grid()
        recolor_button.configure(text="RECOLOR")
    else: 
        color_frame.grid_remove()
        recolor_button.configure(text="INSPECT")   

#####################################################

def init_update():
    if toggle_var.get() == 1: recolor_button.configure(text="RECOLOR")
    else: recolor_button.configure(text="INSPECT")   

#####################################################        

def convert_color2hex(color_value):
    values = [float(x) if i == 3 else int(x) for i, x in enumerate(re.split(r'[,\s]+', color_value.strip()))]
    if len(values) == 4 and all(0 <= x <= 255 for x in values[:3]) and 0 <= values[3] <= 1:
        alpha = values[3]
        hex_color = '#{:02x}{:02x}{:02x}'.format(*map(int, values[:3]))
        return True, hex_color
    else: return False, None

#####################################################

def create_main_frame(root):
    main_frame = ctk.CTkFrame(root, fg_color=theme_color1)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    return main_frame

#####################################################

def create_toggle_button_frame(main_frame):
    toggle_button_frame = ctk.CTkFrame(main_frame)
    toggle_button_frame.grid(row=0, column=0, padx=padx_size, pady=(pady_size + pad_top, pady_size), columnspan=3)
    return toggle_button_frame

#####################################################

def create_toggle_buttons(toggle_button_frame):
    toggle_inspect = ctk.CTkRadioButton(toggle_button_frame, text="INSPECT", variable=toggle_var, value=0, font=font_ms,
                                        text_color=text_color2, command=toggle_color_frame, fg_color=theme_color2)
    toggle_inspect.grid(row=0, column=0, padx=padx_size)

    toggle_recolor = ctk.CTkRadioButton(toggle_button_frame, text="RECOLOR", variable=toggle_var, value=1, font=font_ms,
                                        text_color=text_color2, command=toggle_color_frame, fg_color=theme_color2)
    toggle_recolor.grid(row=0, column=1, padx=padx_size)

#####################################################

def create_info_label(main_frame, sfx_count):
    info_label = ctk.CTkLabel(main_frame, text=f"{sfx_count} SFX files will be recolored.", font=font_ms, text_color=text_color1)
    info_label.grid(row=1, column=0, padx=padx_size, pady=(pady_size + pad_top, pady_size))

#####################################################

def create_color_frame(main_frame):
    global color_frame
    
    color_frame = ctk.CTkFrame(main_frame, fg_color=theme_color1)
    color_frame.grid(row=2, column=0)
    return color_frame

#####################################################

def create_color_labels_and_entries(color_frame, all_colors, all_colors_texts):
    for i, color in enumerate(all_colors):
        label_color_box = ctk.CTkFrame(color_frame, width=100, height=30, fg_color=color)
        label_color_box.grid(row=i + 1, column=0, padx=(padx_size + pad_l, padx_size), pady=pady_size)

        label = ctk.CTkLabel(color_frame, text=color.capitalize(), width=100, font=font_ms,
                             text_color=all_colors_texts[i], bg_color=color)
        label.grid(row=i + 1, column=0, padx=(padx_size + pad_l, padx_size), pady=pady_size)

        entry = ctk.CTkEntry(color_frame, width=150, height=30, placeholder_text=ph_text, font=font_ms)
        entry.grid(row=i + 1, column=1, padx=padx_size, pady=pady_size)

        color_box = ctk.CTkFrame(color_frame, width=100, height=30, fg_color=default_color)
        color_box.grid(row=i + 1, column=2, padx=(padx_size, padx_size + pad_r), pady=pady_size)

        color_box_label = ctk.CTkLabel(color_frame, text="", width=100, font=font_ms, text_color="red", bg_color=default_color)
        color_box_label.grid(row=i + 1, column=2, padx=(padx_size, padx_size + pad_r), pady=pady_size)

        entry.bind("<KeyRelease>", lambda event, e=entry, cb=color_box, cbl=color_box_label: update_color_box(e, cb, cbl))
        
        init_color_update(color, entry, color_box, color_box_label)

#####################################################

def init_color_update(color, entry, color_box, color_box_label):
    if mission_input.get("target_colors"):
        if mission_input.get("target_colors").get(color): 
            target_rgba_in = mission_input["target_colors"][color]
            target_rgba = ', '.join(map(str, target_rgba_in))
            is_rgba, hex_color = convert_color2hex(target_rgba)
            if is_rgba: 
                rgb_text = ', '.join(map(str, target_rgba_in[:3]))
                entry.insert(0, rgb_text)
                color_box.configure(fg_color=hex_color)
                color_box_label.configure(text="", bg_color=hex_color) 

#####################################################

def create_recolor_button(main_frame):
    recolor_button = ctk.CTkButton(main_frame, text="INSPECT", command=lambda: recolor_sfx.main(not toggle_var.get()),
                                   fg_color=theme_color2, text_color=text_color2, width=130, height=50, font=font_size)
    recolor_button.grid(row=3, column=0, padx=padx_size, pady=(pady_size + pad_top, pady_size + pad_bot))
    return recolor_button

#####################################################

def create_copyright_label(main_frame):
    text_copyright = ctk.CTkLabel(main_frame, text=copyright_text, font=font_ms, text_color=text_color1)
    text_copyright.grid(row=4, column=0, padx=(padx_size + pad_l, padx_size + pad_r), pady=(pady_size + pad_top, pady_size + pad_bot))

#####################################################################################

def setup_ui():
    global root, recolor_button, toggle_var
    global font_ms, font_size, font_bold
    
    root = ctk.CTk()
    root.title(f"ER-SFXRecolorTool v{version_str}")
    root.resizable(False, False)

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    font_name = "Helvetica"
    font_ms = ctk.CTkFont(family=font_name, size=14)
    font_size = ctk.CTkFont(family=font_name, size=17, weight="bold")
    font_bold = ctk.CTkFont(family=font_name, size=16, weight="bold")
    
    main_frame = create_main_frame(root)
    toggle_var = ctk.IntVar()
    toggle_var.set(1 if mission_input.get("target_colors") else 0)
    
    toggle_button_frame = create_toggle_button_frame(main_frame)
    create_toggle_buttons(toggle_button_frame)
    create_info_label(main_frame, len(sfx_ids))

    color_frame = create_color_frame(main_frame)
    all_colors = validate_colors()
    all_colors_texts = ["black", "white", "white", "white", "black", "black", "white", "white", "white", "black"]
    create_color_labels_and_entries(color_frame, all_colors, all_colors_texts)

    recolor_button = create_recolor_button(main_frame)
    create_copyright_label(main_frame)

    init_update()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

#####################################################################################

def main():
    try: setup_ui()
    except: pass

#####################################################################################

if __name__ == '__main__': main()

#####################################################################################
