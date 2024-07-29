######################################################################################
import os
import json
import shutil
import colorsys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from xml.etree import ElementTree as ET
sns.set_theme(rc={'figure.figsize':(18, 18)}, font_scale=1.8, style="white")
######################################################################################

def core_process(core_input):
    [tree, target_colors, fn, graph_path, isDeactivateAlpha, cols, isPrePro] = core_input
    all_rgb_groups, all_elm_groups = find_all_groups(tree)
    chosen_rgb_groups, chosen_elm_groups = find_rgb_groups(all_rgb_groups, all_elm_groups)
    plot_input = [chosen_rgb_groups, chosen_elm_groups, target_colors, fn, graph_path, isPrePro]
    will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs = plot_colors(plot_input, isDeactivateAlpha, cols)
    core_output = [will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs, chosen_rgb_groups, chosen_elm_groups, all_rgb_groups, all_elm_groups]
    return core_output

######################################################################################

def create_toning(will_be_changed_rgbs, will_be_changed_clrs, recolor_mission):
    color_groups = {color: [] for color in recolor_mission.keys()}
    for key in will_be_changed_rgbs:
        color_name = will_be_changed_clrs[key]
        color_groups[color_name].append(will_be_changed_rgbs[key])
    average_rgbs = {color: np.mean(rgbs, axis=0) for color, rgbs in color_groups.items() if rgbs}
    will_be_changed_rgbs_new = {}
    for key, color_name in will_be_changed_clrs.items():
        old_rgb = will_be_changed_rgbs[key]
        new_rgb = recolor_mission[color_name]
        avg_rgb = average_rgbs[color_name]
        diff = old_rgb - avg_rgb
        newest_rgb = new_rgb + diff
        fixed_newest_rgb = fix_rgb_values(newest_rgb)
        will_be_changed_rgbs_new[key] = fixed_newest_rgb
    return will_be_changed_rgbs_new

######################################################################################

def rgb_to_color_name(rgb):
    r, g, b = rgb[:3]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue_angle = h * 360
    if l > 0.9: return 'white'
    elif l < 0.1: return 'black'
    elif s < 0.15: return 'grey'
    elif hue_angle < 15 or hue_angle >= 330: return 'red'
    elif hue_angle < 45: return 'orange'
    elif hue_angle < 90: return 'yellow'
    elif hue_angle < 150: return 'green'
    elif hue_angle < 270: return 'blue'
    elif hue_angle < 330: return 'purple'

######################################################################################

def fix_rgb_values(new_rgb):
    fixed_rgb = []
    for value in new_rgb:
        fixed_value = value
        if value < 0: fixed_value = - value   # diff = 0 - value   # 0 + (diff)
        elif value > 1: fixed_value = 2 - value   # diff = value - 1   # 1 - (diff)
        fixed_rgb.append(fixed_value)
    return fixed_rgb

######################################################################################

def find_all_groups(tree):
    root = tree.getroot()
    all_rgb_groups = {}
    all_elm_groups = {}
    cnt = 0
    for prop_elm in root.findall(".//Property"):
        if prop_elm.get('PropertyType') == "Color":
            interp_type = prop_elm.get('InterpolationType')
            is_loop_type = prop_elm.get('IsLoop')
            rgb_group = []
            elm_group = []
            for float_elm in prop_elm.findall("./Fields/Float"):
                value = float_elm.get('Value')
                rgb_group.append(float(value))
                elm_group.append(float_elm)
            all_rgb_groups[f"{cnt}_{interp_type}_{is_loop_type}"] = rgb_group
            all_elm_groups[f"{cnt}_{interp_type}_{is_loop_type}"] = elm_group
            cnt += 1
    return all_rgb_groups, all_elm_groups

######################################################################################

def find_rgb_groups(all_rgb_groups, all_elm_groups):
    chosen_rgb_groups = {}
    chosen_elm_groups = {}
    for key, v in all_rgb_groups.items():
        elm_v = all_elm_groups[key]
        color_type = key.split("_")[1]
        if color_type in ["One", "Curve2"]: continue
        if len(v) in [4, 18, 23, 28]:
            if len(v) == 18: 
                del v[7:9]
                del elm_v[7:9]
            elif len(v) == 23: 
                del v[7:10]
                del elm_v[7:10]
            assert len(v) % 4 == 0
            v = [v[i:i+4] for i in range(0, len(v), 4)]  
            elm_v = [elm_v[i:i+4] for i in range(0, len(elm_v), 4)]  
        for j in range(len(v)):
            isAllColor = True
            for k in range(len(v[j])):
                if not 0 <= v[j][k] <= 1: 
                    isAllColor = False
                    break
            if isAllColor: 
                chosen_rgb_groups[f"{key}_{j}_len{len(v)*4}"] = v[j]
                chosen_elm_groups[f"{key}_{j}_len{len(v)*4}"] = elm_v[j]
    return chosen_rgb_groups, chosen_elm_groups

######################################################################################

def plot_colors(plot_input, isDeactivateAlpha=False, cols=6):
    [chosen_rgb_groups, chosen_elm_groups, target_colors, fn, sp, isPrePro] = plot_input
    total_colors = len(chosen_rgb_groups)
    if total_colors == 0: rows, cols = 1, 1
    else:
        rows = total_colors // cols + (1 if total_colors % cols else 0)
    fig, axs = plt.subplots(rows, 
                            cols, 
                            figsize=(cols*2, rows*3),
                            dpi=300,
                            constrained_layout=True)
    if not isinstance(axs, np.ndarray): axs = [axs]
    else: axs = axs.flatten()
    will_be_changed_rgbs = {}
    will_be_changed_elms = {}
    will_be_changed_clrs = {}
    for i, (k, rgb) in enumerate(chosen_rgb_groups.items()):
        color_text = rgb_to_color_name(rgb)
        if color_text in target_colors: 
            will_be_changed_rgbs[k] = chosen_rgb_groups[k] 
            will_be_changed_elms[k] = chosen_elm_groups[k]  
            will_be_changed_clrs[k] = color_text
        ax = axs[i]
        if isDeactivateAlpha: rgb[3] = 1.0
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=rgb))
        ax.axis('off')
        ax.text(0.5, 0.5, color_text, fontsize=12, 
                ha='center', va='center', color="black",
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
        rgb_text = f"{int(np.round(rgb[0]*255, 0))}, {int(np.round(rgb[1]*255, 0))}, {int(np.round(rgb[2]*255, 0))}, {np.round(rgb[3], 2)}"
        ax.text(0.5, 0.9, rgb_text, fontsize=10, 
                ha='center', va='top', color="black",
                transform=ax.transAxes)
        ax.set_title(k, fontsize=8)
    if total_colors < rows * cols:
        for i in range(total_colors, rows * cols):
            axs[i].axis('off')
    fig.suptitle(f"\n{fn} > All Colors ({isPrePro.capitalize()})\n", fontsize=35)
    plt.savefig(f"{sp}/{fn.split('.')[0]}_{isPrePro}.png", dpi=300, bbox_inches='tight')
    # plt.show()
    return will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs
    
######################################################################################

def plot_1color(rgb):   # For debugging
    plt.figure(figsize=(2, 2))
    plt.imshow([[rgb]])
    plt.axis('off')
    plt.show()
    
######################################################################################

def replace_first_2_lines(xml_path, first_2line):
    with open(xml_path, "r", encoding="utf8") as f: new_xml = f.readlines()[1:]
    with open(xml_path, "w", encoding="utf8") as f: f.write(''.join(first_2line) + ''.join(new_xml))
    
######################################################################################
######################################################################################

def load_mission_input(filepath):
    with open(filepath, "r", encoding="utf8") as f: return json.load(f)

######################################################################################

def prepare_recolor_mission(recolor_mission):
    return {color: [value / 255 for value in rgb] for color, rgb in recolor_mission.items()}

######################################################################################

def validate_colors(recolor_mission):
    all_colors = ["white", "red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]
    assert all(color in all_colors for color in recolor_mission.keys())

######################################################################################

def initialize_paths(config_file):
    with open(config_file, "r", encoding="utf8") as f: config = json.load(f)

    sfx_abs_path = config["sfx_abs_path"]
    graph_path = config["graph_path"]
    main_sfx_folder_name = config["main_sfx_folder_name"]
    main_sfx_file_name = config["main_sfx_file_name"]
    elden_ring_abs_path = config["elden_ring_abs_path"]
    witchyBND_path = config["witchyBND_path"]
    UXM_path = config["UXM_path"]

    main_path = f"{sfx_abs_path}/orj_backup"
    save_path = f"{sfx_abs_path}/all_success_altereds"
    active_path = f"{sfx_abs_path}/active_files"

    if not os.path.exists(active_path): os.mkdir(active_path)
    
    paths = {
        "sfx_abs_path": sfx_abs_path,
        "graph_path": graph_path,
        "main_sfx_folder_name": main_sfx_folder_name,
        "main_sfx_file_name": main_sfx_file_name,
        "elden_ring_abs_path": elden_ring_abs_path,
        "witchyBND_path": witchyBND_path,
        "UXM_path": UXM_path,
        "main": main_path,
        "save": save_path,
        "active": active_path
    }
    
    return paths

######################################################################################

def process_sfx_files(sfx_ids, paths):
    all_fxr_fps = [paths["witchyBND"]]
    for sfx_id in sfx_ids:
        sfx_fn = f"f000{sfx_id}.fxr"
        sfx_path = f"{paths['main']}/{paths['main_sfx_folder_name']}/effect/{sfx_fn}"
        if not os.path.exists(sfx_path): 
            print(f">> {sfx_id} could not be found in game files !")
            continue
        shutil.copyfile(sfx_path, f"{paths['main']}/{sfx_fn}")
        shutil.copyfile(sfx_path, f"{paths['active']}/{sfx_fn}")
        all_fxr_fps.append(f"{paths['active']}/{sfx_fn}")
    all_fxr_fps.append("-p")
    all_xml_fps = [f"{fxr_file}.xml" for fxr_file in all_fxr_fps[1:-1]]
    all_xml_fps = [all_fxr_fps[0]] + all_xml_fps + [all_fxr_fps[-1]]
    return all_fxr_fps, all_xml_fps

######################################################################################

def decompress_fxr_files(all_fxr_fps):
    _ = subprocess.run(all_fxr_fps)
    print('\n>> FXR files are decompressed to XML files via WitchyBND')

######################################################################################

def process_xml_files(active_path, recolor_mission, graph_path, isDeactivateAlpha, cols):
    cnt = 0
    for fn in os.listdir(active_path):
        xml_path = f"{active_path}/{fn}"
        if not fn.endswith(".xml"): 
            os.remove(xml_path)
            continue
        cnt += 1
        with open(xml_path, "r", encoding="utf8") as f: first_2line = f.readlines()[:2]
        print(f">> {cnt} - {fn} is started to process..")
        tree = ET.parse(xml_path)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, isDeactivateAlpha, cols, "pre"]
        core_output = core_process(core_input)
        [will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs, chosen_rgb_groups, chosen_elm_groups, all_rgb_groups, all_elm_groups] = core_output
        will_be_changed_rgbs_new = create_toning(will_be_changed_rgbs, will_be_changed_clrs, recolor_mission)
        for key, elms in will_be_changed_elms.items():
            new_rgb_values = will_be_changed_rgbs_new[key]
            for i in range(3): 
                elms[i].set('Value', str(new_rgb_values[i])) 
            tree.write(xml_path)
            replace_first_2_lines(xml_path, first_2line)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, isDeactivateAlpha, cols, "pro"]
        _ = core_process(core_input)

######################################################################################

def compress_xml_files(all_xml_fps):
    _ = subprocess.run(all_xml_fps)
    print('\n>> XML files are compressed to FXR files via WitchyBND')

######################################################################################

def move_and_compress_files(active_path, save_path, main_sfx_folder_name, witchyBND_path):
    for fn in os.listdir(active_path):
        from_path = f"{active_path}/{fn}"
        to_path = f"{save_path}/{fn}"
        final_dest = f"{save_path}/{main_sfx_folder_name}/effect/{fn}"
        if fn.endswith(".fxr"): shutil.copyfile(from_path, final_dest) 
        shutil.move(from_path, to_path)
    _ = subprocess.run([witchyBND_path, f"{save_path}/{main_sfx_folder_name}", "-p"])
    print(f'\n>> "{main_sfx_folder_name}" folder is compressed via WitchyBND')

######################################################################################

def finalize_process(save_path, main_sfx_file_name, elden_ring_abs_path, UXM_path):
    shutil.copyfile(f"{save_path}/{main_sfx_file_name}", f"{elden_ring_abs_path}/{main_sfx_file_name}")
    print("\n>> Process is COMPLETED ! Please remember to patch the game via UXM !\n")
    subprocess.run([UXM_path])

######################################################################################
    