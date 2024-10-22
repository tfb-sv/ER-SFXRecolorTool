#####################################################################################
import os
import re
import sys
import json
import shutil
import threading
from pathlib import Path
import customtkinter as ctk
from tkinter.messagebox import showinfo
from utils_recolor import *
import recolor_sfx
#####################################################################################

is_debug = False

config_fn = "paths_config.json"
mission_fn = "recolor_mission.json"
assert_config_text = f"\n>> The file {config_fn} could not be found in the program directory. The program is ABORTED.\n"
assert_mission_text = f"\n>> The file {mission_fn} could not be found in the program directory. The program is ABORTED.\n"
assert os.path.exists(config_fn), assert_config_text
assert os.path.exists(mission_fn), assert_mission_text
with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
sfx_ids = mission_input["sfx_ids"]

version_str = "1.0.0"
year_str = "2024"
owner_str = "ineedthetail"
copyright_text = f"\u00A9 {year_str} {owner_str}. Licensed under CC BY-NC-SA 4.0.\nv{version_str}"
init_text = f"{len(sfx_ids)} SFX files will be inspected."

all_colors = get_all_colors()
all_colors_texts = ["black", "white", "white", "white", "black", 
                    "black", "white", "white", "white", "black"]

theme_color2 = random_init_color()
text_color2 = all_colors_texts[all_colors.index(theme_color2)]

padx_size, pady_size = 10, 10
pad_top, pad_bot = 20, 20
pad_l, pad_r = 40, 40
ph_text = "255, 255, 255"
default_color = "transparent"
theme_color1 = None
text_color1 = "white"

#####################################################################################

def on_closing():
    root.destroy()
    sys.exit(0)

#####################################################################################
    
def update_color_box(entry, color_box, color_box_label):
    color_value = entry.get()
    is_rgba, hex_color, _ = convert_rgba2hex(color_value)
    if is_rgba:
        color_box.configure(fg_color=hex_color)
        color_box_label.configure(text="", bg_color=hex_color)
    else: 
        color_box.configure(fg_color=default_color)
        if color_value.strip() == "": color_box_label.configure(text="", bg_color=default_color)
        else: color_box_label.configure(text="Not Valid", bg_color=default_color)
        
#####################################################################################

def toggle_update():
    global color_frame, recolor_button, info_label, checkbox_frame
    
    if toggle_var.get() == 1: 
        color_frame.grid()
        checkbox_frame.grid()
        recolor_button.configure(text="RECOLOR")
        info_label.configure(text=f"{len(sfx_ids)} SFX files will be recolored.")
    else: 
        color_frame.grid_remove()
        checkbox_frame.grid_remove()
        recolor_button.configure(text="INSPECT")   
        info_label.configure(text=f"{len(sfx_ids)} SFX files will be inspected.")

##################################################################################### 

def get_toggle_text():
    if toggle_var.get() == 0: text = toggle_inspect.cget("text")
    elif toggle_var.get() == 1: text = toggle_recolor.cget("text")
    return text

#####################################################################################       

def convert_rgba2hex(color_value):
    try:
        if color_value.strip().endswith(','): return False, None, None
        color_value += ", 1.0"
        values = [float(x) if i == 3 else int(x) for i, x in enumerate(re.split(r'[,\s]+', color_value.strip()))]
        if len(values) == 4 and all(0 <= x <= 255 for x in values[:3]) and 0 <= values[3] <= 1:
            alpha = values[3]
            hex_color = '#{:02x}{:02x}{:02x}'.format(*map(int, values[:3]))
            return True, hex_color, values
        else: return False, None, None
    except ValueError: return False, None, None

#####################################################################################

def create_main_frame(root):
    main_frame = ctk.CTkFrame(root, fg_color=theme_color1)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    return main_frame

#####################################################################################

def create_toggle_frame(main_frame, row, column):
    global toggle_inspect, toggle_recolor
    
    toggle_button_frame = ctk.CTkFrame(main_frame)
    toggle_button_frame.grid(row=row, column=column, padx=padx_size, pady=(pady_size + pad_top, pady_size), columnspan=3)

    toggle_inspect = ctk.CTkRadioButton(toggle_button_frame, text="INSPECTION", variable=toggle_var, value=0, font=font_ms,
                                        text_color=text_color1, command=toggle_update, fg_color=theme_color2)
    toggle_inspect.grid(row=0, column=0, padx=padx_size)

    toggle_recolor = ctk.CTkRadioButton(toggle_button_frame, text="RECOLORING", variable=toggle_var, value=1, font=font_ms,
                                        text_color=text_color1, command=toggle_update, fg_color=theme_color2)
    toggle_recolor.grid(row=0, column=1, padx=padx_size)

#####################################################################################

def create_info_label(main_frame, row, column):
    global info_label
    
    info_label = ctk.CTkLabel(main_frame, text=init_text, 
                              font=font_ms, text_color=text_color1)
    info_label.grid(row=row, column=column, padx=padx_size, pady=(pady_size + pad_top, pady_size))

#####################################################################################
    
def create_progress_bar(main_frame, row, column):
    global progress_bar
    
    progress_bar = ctk.CTkProgressBar(main_frame, width=300,
                                      progress_color=theme_color2, fg_color=theme_color1)
    progress_bar.grid(row=row, column=column, padx=padx_size, pady=pady_size)
    progress_bar.grid_remove()

#####################################################################################

def create_color_frame(main_frame, row, column, all_colors, all_colors_texts):
    global color_frame, entry_widgets
    
    color_frame = ctk.CTkFrame(main_frame, fg_color=theme_color1)
    color_frame.grid(row=row, column=column)

    header_l = ctk.CTkLabel(color_frame, text="Old Color", width=100, font=font_bold,
                            text_color=text_color1, bg_color=default_color)
    header_l.grid(row=0, column=0, padx=(padx_size + pad_l, padx_size), pady=pady_size)
    
    header_m = ctk.CTkLabel(color_frame, text="New RGB", width=100, font=font_bold,
                            text_color=text_color1, bg_color=default_color)
    header_m.grid(row=0, column=1, padx=padx_size, pady=pady_size)
    
    header_r = ctk.CTkLabel(color_frame, text="New Color", width=100, font=font_bold,
                            text_color=text_color1, bg_color=default_color)
    header_r.grid(row=0, column=2, padx=(padx_size, padx_size + pad_r), pady=pady_size)

    entry_widgets = {}
    for i, color in enumerate(all_colors):
        label_color_box = ctk.CTkFrame(color_frame, width=100, height=30, fg_color=color)
        label_color_box.grid(row=i + 1, column=0, padx=(padx_size + pad_l, padx_size), pady=pady_size)

        label = ctk.CTkLabel(color_frame, text=color.capitalize(), width=100, font=font_ms,
                             text_color=all_colors_texts[i], bg_color=color)
        label.grid(row=i + 1, column=0, padx=(padx_size + pad_l, padx_size), pady=pady_size)

        entry = ctk.CTkEntry(color_frame, width=150, height=30, placeholder_text=ph_text, font=font_ms)
        entry.grid(row=i + 1, column=1, padx=padx_size, pady=pady_size)
        entry_widgets[color] = entry

        color_box = ctk.CTkFrame(color_frame, width=100, height=30, fg_color=default_color)
        color_box.grid(row=i + 1, column=2, padx=(padx_size, padx_size + pad_r), pady=pady_size)

        color_box_label = ctk.CTkLabel(color_frame, text="", width=100, 
                                       font=font_ms, text_color="red", bg_color=default_color)
        color_box_label.grid(row=i + 1, column=2, padx=(padx_size, padx_size + pad_r), pady=pady_size)

        entry.bind("<KeyRelease>", lambda event, e=entry, cb=color_box, cbl=color_box_label: update_color_box(e, cb, cbl))
        
        init_color_update(color, entry, color_box, color_box_label)

#####################################################################################

def init_color_update(color, entry, color_box, color_box_label):
    if mission_input.get("target_colors"):
        if mission_input.get("target_colors").get(color): 
            target_rgba_in = mission_input["target_colors"][color]
            rgb_text = ', '.join(map(str, target_rgba_in[:3]))
            is_rgba, hex_color, _ = convert_rgba2hex(rgb_text)
            if is_rgba: 
                entry.insert(0, rgb_text)
                color_box.configure(fg_color=hex_color)
                color_box_label.configure(text="", bg_color=hex_color) 

#####################################################################################

def create_checkbox_frame(main_frame, row, column):
    global checkbox_frame, checkbox
    
    checkbox_frame = ctk.CTkFrame(main_frame)
    checkbox_frame.grid(row=row, column=column, padx=padx_size, pady=pady_size)
    
    checkbox = ctk.CTkCheckBox(checkbox_frame, text="", variable=checkbox_var)
    checkbox.grid(row=0, column=0, padx=padx_size)
    
    checkbox_label = ctk.CTkLabel(checkbox_frame, text="Launch game after recoloring (with ModEngine2)", 
                                  font=font_ms, text_color=text_color1)
    checkbox_label.grid(row=0, column=1, padx=padx_size)

#####################################################################################

def create_recolor_button(main_frame, row, column):
    global recolor_button

    recolor_button = ctk.CTkButton(main_frame, text="INSPECT", 
                                   command=lambda: threading.Thread(target=start_recoloring_procedure, 
                                                                    daemon=True).start(),
                                   fg_color=theme_color2, text_color=text_color2, 
                                   width=130, height=50, font=font_size)
    recolor_button.grid(row=row, column=column, padx=padx_size, pady=(pady_size + pad_top, pady_size + pad_bot))

#####################################################################################

def create_copyright_label(main_frame, row, column):
    text_copyright = ctk.CTkButton(main_frame, text=copyright_text, 
                                   command=open_url,
                                   hover=False,
                                   fg_color=default_color, text_color=text_color1, 
                                   width=100, height=30, font=font_ms)
    text_copyright.grid(row=row, column=column, padx=(padx_size + pad_l, padx_size + pad_r), 
                        pady=(pady_size + pad_top, pady_size + pad_bot))

#####################################################################################
    
def start_recoloring_procedure():  
    global entry_widgets, info_label, recolor_button, progress_bar, checkbox
    global toggle_inspect, toggle_recolor

    # os.system('cls')

    is_inspection = not toggle_var.get()
    is_run_after = checkbox_var.get()
    mod_name = get_toggle_text()
    
    final_text = f"{mod_name.capitalize()} was completed successfully."

    progress_bar.set(0)
    progress_bar.grid()
    info_label.configure(text=f"{mod_name.capitalize()} procedure was started, please wait..")
    checkbox.configure(state="disabled")
    recolor_button.configure(state="disabled")
    toggle_inspect.configure(state="disabled")
    toggle_recolor.configure(state="disabled")
    
    recolor_mission = {}
    if not is_inspection:
        for color, entry in entry_widgets.items():
            entry.configure(state="disabled")
            color_value = entry.get()
            is_color, _, rgba_list = convert_rgba2hex(color_value)
            if is_color: recolor_mission[color] = rgba_list 
    recolor_info = [is_inspection, recolor_mission, 
                    config_fn, mission_fn, mission_input, sfx_ids, is_debug]
    paths = recolor_sfx.main(recolor_info, progress_bar, info_label)
    mod_engine_abs_path = str(Path(paths["mod_abs_path"]).parent).replace("\\", "/")
    progress_bar.set(1)
    info_label.configure(text=final_text)
    
    showinfo(f"{mod_name.upper()} COMPLETED", 
             final_text)

    shutil.rmtree(paths["active_path"]) 
    os.mkdir(paths["active_path"])
    progress_bar.set(0)
    progress_bar.grid_remove()
    info_label.configure(text=init_text)
    checkbox.configure(state="normal")
    recolor_button.configure(state="normal")
    toggle_inspect.configure(state="normal")
    toggle_recolor.configure(state="normal")
    if not is_inspection: 
        for entry in entry_widgets.values():
            entry.configure(state="normal")
        if is_run_after: subprocess.run([f"{mod_engine_abs_path}/launchmod_eldenring.bat"])
    else:
        toggle_var.set(1)
        toggle_update()

#####################################################################################

def setup_ui():
    global root, toggle_var, checkbox_var, progress_bar
    global font_ms, font_size, font_bold
    
    root = ctk.CTk()
    root.title(f"ER-SFXRecolorTool")
    root.resizable(False, False)

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    font_name = "Helvetica"
    font_ms = ctk.CTkFont(family=font_name, size=14)
    font_size = ctk.CTkFont(family=font_name, size=17, weight="bold")
    font_bold = ctk.CTkFont(family=font_name, size=16, weight="bold")
    
    toggle_var = ctk.IntVar()
    toggle_var.set(1 if mission_input.get("target_colors") else 0)
    checkbox_var = ctk.IntVar()
    checkbox_var.set(0)
    
    main_frame = create_main_frame(root)
    create_toggle_frame(main_frame, 0, 0)
    create_info_label(main_frame, 1, 0)
    create_progress_bar(main_frame, 2, 0)
    create_color_frame(main_frame, 3, 0, all_colors, all_colors_texts)
    create_checkbox_frame(main_frame, 4, 0)
    create_recolor_button(main_frame, 5, 0)
    create_copyright_label(main_frame, 6, 0)

    toggle_update()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

#####################################################################################
