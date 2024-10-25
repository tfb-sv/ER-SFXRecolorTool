import os
import json
import shutil
import random
import colorsys
import subprocess
import webbrowser
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from xml.etree import ElementTree as ET
sns.set_theme(rc={'figure.figsize':(18, 18)}, font_scale=1.8, style="white")

def rgb_to_color_name(rgb):
    r, g, b = rgb[:3]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue_angle = h * 360
    if l > 0.9: return 'white', hue_angle, l, s
    elif l < 0.09: return 'black', hue_angle, l, s
    elif s < 0.09: return 'gray', hue_angle, l, s
    elif hue_angle < 9: return 'red', hue_angle, l, s
    elif hue_angle < 45: return 'orange', hue_angle, l, s
    elif hue_angle < 64: return 'yellow', hue_angle, l, s
    elif hue_angle < 160: return 'green', hue_angle, l, s
    elif hue_angle < 236: return 'blue', hue_angle, l, s
    elif hue_angle < 293: return 'purple', hue_angle, l, s
    elif hue_angle < 350: return 'pink', hue_angle, l, s
    elif hue_angle >= 350: return 'red', hue_angle, l, s

def get_all_colors():
    all_colors = ["white", "black", "gray", "red", "orange", 
                  "yellow", "green", "blue", "purple", "pink"]
    return all_colors

def random_init_color():
    all_colors = get_all_colors()
    excludeds = ["white", "black", "gray"]
    filtered_colors = [color for color in all_colors if color not in excludeds]
    random_color = random.choice(filtered_colors)
    return random_color

def witchy_subprocess(command):
    witchy_silent_argument = "-s"   # previously it was "-p"
    command.append(witchy_silent_argument)
    _ = subprocess.run(command)

def prepare_recolor_mission(recolor_mission):
    all_colors = get_all_colors()
    assert all(color in all_colors for color in recolor_mission.keys())
    recolor_mission = {color: [value / 255 for value in rgb] for color, rgb in recolor_mission.items()}
    return recolor_mission

def open_url(): webbrowser.open("https://github.com/tfb-sv/ER-SFXRecolorTool.git")

def obtain_all_sfx_files():
    dcx2folder_dct = {"sfxbnd_commoneffects.ffxbnd.dcx": None,
                      "sfxbnd_commoneffects_dlc02.ffxbnd.dcx": None} 
    for dcx_fn, _ in dcx2folder_dct.items():
        dcx2folder_dct[dcx_fn] = dcx_fn.replace(".", "-") + "-wffxbnd"
    dcx2folder_dct = speed_up_search(dcx2folder_dct)
    return dcx2folder_dct

def speed_up_search(dcx2folder_dct): return dcx2folder_dct   # order common sfx fns to the top

def initialize_paths(config_fn):
    with open(config_fn, "r", encoding="utf8") as f: config = json.load(f)
    dcx2folder_dct = obtain_all_sfx_files()
    sfx_tmp_path = "sfx"
    graph_path = "sfx_palettes"
    elden_ring_abs_path = config["elden_ring_abs_path"].replace("\\", "/")
    mod_abs_path = config["mod_abs_path"].replace("\\", "/")
    witchyBND_path = config["witchyBND_abs_path"].replace("\\", "/")
    witchyBND_path += "/WitchyBND.exe"
    main_path = f"{sfx_tmp_path}/original_files"
    save_path = f"{sfx_tmp_path}/modified_files"
    active_path = f"{sfx_tmp_path}/active_files"
    if not os.path.exists(sfx_tmp_path): os.mkdir(sfx_tmp_path)
    if not os.path.exists(main_path): os.mkdir(main_path)
    if not os.path.exists(save_path): os.mkdir(save_path)
    if os.path.exists(active_path): shutil.rmtree(active_path) 
    os.mkdir(active_path)
    if os.path.exists(graph_path): shutil.rmtree(graph_path) 
    os.mkdir(graph_path)
    paths = {
        "elden_ring_abs_path": elden_ring_abs_path,
        "mod_abs_path": mod_abs_path,
        "witchyBND_abs_path": witchyBND_path,
        "sfx_tmp_path": sfx_tmp_path,
        "graph_path": graph_path,
        "main_path": main_path,
        "save_path": save_path,
        "active_path": active_path
    }
    return paths, dcx2folder_dct

def core_process(core_input):
    [tree, target_colors, fn, graph_path, cols, isPrePro, is_inspection, ignoreds] = core_input
    all_rgb_groups, all_elm_groups = find_all_groups(tree)
    chosen_rgb_groups, chosen_elm_groups, ignoreds = find_rgb_groups(all_rgb_groups, all_elm_groups, fn, ignoreds, is_inspection)
    plot_input = [chosen_rgb_groups, chosen_elm_groups, target_colors, fn, graph_path, isPrePro]
    will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs = plot_colors(plot_input, cols)
    core_output = [will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs, 
                   chosen_rgb_groups, chosen_elm_groups, all_rgb_groups, all_elm_groups, ignoreds]
    return core_output

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

def fix_rgb_values(new_rgb):
    fixed_rgb = []
    for value in new_rgb:
        fixed_value = value
        if value < 0: fixed_value = -value   # diff = 0 - value   # 0 + (diff)
        elif value > 1: fixed_value = 2 - value   # diff = value - 1   # 1 - (diff)
        fixed_rgb.append(fixed_value)
    return fixed_rgb

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

def find_rgb_groups(all_rgb_groups, all_elm_groups, fn, ignoreds, is_inspection):
    chosen_rgb_groups = {}
    chosen_elm_groups = {}
    for key, v in all_rgb_groups.items():
        elm_v = all_elm_groups[key]
        color_type = key.split("_")[1]
        if color_type in ["One", "Curve2"]: continue
        if len(v) in [4, 18, 23, 28, 33, 38]:
            if len(v) == 18: 
                del v[7:9]
                del elm_v[7:9]
            elif len(v) == 23: 
                del v[7:10]
                del elm_v[7:10] 
            elif len(v) == 33: 
                del v[9:14]
                del elm_v[9:14]
            elif len(v) == 38: 
                del v[9:15]
                del elm_v[9:15] 
            assert len(v) % 4 == 0
            v = [v[i:i+4] for i in range(0, len(v), 4)]  
            elm_v = [elm_v[i:i+4] for i in range(0, len(elm_v), 4)]
        else:
            if is_inspection:
                sfx_id = int(fn[1:-4])
                print(f"\n>> Does not match the pattern, IGNORED.\nSFX ID: {sfx_id} Length: {len(v)} Key: {key}\n")
                if not os.path.exists("errors"): os.mkdir("errors")
                df = pd.DataFrame([v], columns=[f'Value{i+1}' for i in range(len(v))])
                df.to_csv(f'errors/{sfx_id}-{key}.csv', index=False)
                if not ignoreds[sfx_id]: ignoreds[fn] = [key]
                else: ignoreds[sfx_id].extend(key)
            continue
        for j in range(len(v)):
            isAllColor = True
            for k in range(len(v[j])):
                if not 0 <= v[j][k] <= 1: 
                    isAllColor = False
                    break
            if isAllColor: 
                chosen_rgb_groups[f"{key}_{j}_len{len(v)*4}"] = v[j]
                chosen_elm_groups[f"{key}_{j}_len{len(v)*4}"] = elm_v[j]
    return chosen_rgb_groups, chosen_elm_groups, ignoreds

def plot_colors(plot_input, cols):
    [chosen_rgb_groups, chosen_elm_groups, target_colors, fn, sp, isPrePro] = plot_input
    isBeforeAfter = "Before" if isPrePro == "pre" else "After"
    total_colors = len(chosen_rgb_groups)
    if total_colors == 0: rows, cols = 1, 1
    else: rows = total_colors // cols + (1 if total_colors % cols else 0)
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
        color_text, _, _, _ = rgb_to_color_name(rgb)
        if color_text in target_colors: 
            will_be_changed_rgbs[k] = chosen_rgb_groups[k] 
            will_be_changed_elms[k] = chosen_elm_groups[k]  
            will_be_changed_clrs[k] = color_text
        ax = axs[i]
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=rgb))
        ax.axis('off')
        ax.text(0.5, 0.5, color_text, fontsize=12, 
                ha='center', va='center', color="black",
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
        rgbs = [int(np.round(rgb[0]*255, 0)),
                int(np.round(rgb[1]*255, 0)),
                int(np.round(rgb[2]*255, 0)),
                np.round(rgb[3], 2)]
        rgb_text = f"{rgbs[0]}, {rgbs[1]}, {rgbs[2]}, {rgbs[3]}"
        ax.text(0.5, 0.9, rgb_text, fontsize=10, 
                ha='center', va='top', color="black",
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
        ax.set_title(k, fontsize=8)
    if total_colors < rows * cols:
        for i in range(total_colors, rows * cols):
            axs[i].axis('off')
    fig.suptitle(f"\n{fn} > All Colors ({isBeforeAfter})\n", fontsize=35)
    plt.savefig(f"{sp}/{fn.split('.')[0]}_{isPrePro}.png", dpi=300, bbox_inches='tight')
    return will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs

def replace_first_2_lines(xml_path, first_2line):
    with open(xml_path, "r", encoding="utf8") as f: new_xml = f.readlines()[1:]
    with open(xml_path, "w", encoding="utf8") as f: f.write(''.join(first_2line) + ''.join(new_xml))

def check_dcx_folder_in_path(paths, dcx_fn, dcx_folder_name):
    elden_ring_abs_path = paths["elden_ring_abs_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    main_path = paths['main_path']
    save_path = paths['save_path']
    if not os.path.exists(f"{main_path}/{dcx_folder_name}"):
        print(f'\t- Original "{dcx_folder_name}" NOT found. Decompressing original DCXs..')
        from_fp = f"{elden_ring_abs_path}/Game/sfx/{dcx_fn}"
        to_fp = f"{main_path}/{dcx_fn}"
        command_fp = f"{main_path}/{dcx_fn}"
        shutil.copyfile(from_fp, to_fp)
        command = [witchyBND_path, command_fp]
        witchy_subprocess(command)
    else: print(f'\t- Original "{dcx_folder_name}" found.')
    if not os.path.exists(f"{save_path}/{dcx_folder_name}"):
        print(f'\t- Modified "{dcx_folder_name}" NOT found. Loading original FXRs..')
        from_fp = f"{main_path}/{dcx_folder_name}"
        to_fp = f"{save_path}/{dcx_folder_name}"
        shutil.copytree(from_fp, to_fp)
    else: print(f'\t- Modified "{dcx_folder_name}" found.')
        
def check_dcx_folders_in_paths(paths, dcx2folder_dct):
    for dcx_fn, dcx_folder_name in dcx2folder_dct.items():
        check_dcx_folder_in_path(paths, dcx_fn, dcx_folder_name)

def process_sfx_files(sfx_ids, paths, dcx2folder_dct):
    main_path = paths['main_path']
    active_path = paths['active_path']
    decompress_fxr_command = [paths["witchyBND_abs_path"]]
    sfx2dcx_dct = {}
    change_info = {}
    not_exists = []
    for sfx_id in sfx_ids:
        sfx_fn = f"f{str(sfx_id).zfill(9)}.fxr"
        is_found = False
        for dcx_fn, dcx_folder_name in dcx2folder_dct.items():
            sfx_path = f"{main_path}/{dcx_folder_name}/effect/{sfx_fn}"
            change_info[dcx_fn] = False
            if os.path.exists(sfx_path): 
                sfx_final_path = sfx_path
                sfx2dcx_dct[sfx_fn] = sfx_path
                change_info[dcx_fn] = True
                is_found = True
            if is_found: break
        if not is_found: 
            print(f">> {sfx_id} NOT found in game files.")
            not_exists.append(sfx_id)
            continue
        active_fp = f"{active_path}/{sfx_fn}"
        shutil.copyfile(sfx_final_path, active_fp)
        decompress_fxr_command.append(active_fp)
    compress_xml_command = [f"{fxr_file}.xml" for fxr_file in decompress_fxr_command[1:-1]]
    compress_xml_command = [decompress_fxr_command[0]] + compress_xml_command
    return [decompress_fxr_command, compress_xml_command, sfx2dcx_dct, change_info, not_exists]

def process_xml_files(recolor_mission, active_path, graph_path, cols, 
                      is_inspection, info_label, progress_bar, norm_coef, mn, mx):
    progress_text_main = info_label.cget("text")
    percentage_range = mx - mn
    ignoreds = {}
    all_xmls = [fn for fn in os.listdir(active_path) if fn.endswith(".xml")]
    for cnt, fn in enumerate(all_xmls):
        sfx_id = int(fn[1:-8])
        xml_path = f"{active_path}/{fn}"
        with open(xml_path, "r", encoding="utf8") as f: first_2line = f.readlines()[:2]
        print(f'\t{cnt + 1} - Processing SFX {sfx_id}..')
        progress_text = f"{progress_text_main} ({cnt + 1}/{len(all_xmls)})"
        info_label.configure(text=progress_text)
        progress_number = mn + (cnt * (percentage_range / len(all_xmls)))
        assert mx > progress_number
        progress_bar.set(progress_number * norm_coef)
        tree = ET.parse(xml_path)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, cols, "pre", is_inspection, ignoreds]
        core_output = core_process(core_input)
        if is_inspection: continue
        [will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs, 
         chosen_rgb_groups, chosen_elm_groups, all_rgb_groups, all_elm_groups, ignoreds] = core_output
        will_be_changed_rgbs_new = create_toning(will_be_changed_rgbs, will_be_changed_clrs, recolor_mission)
        for key, elms in will_be_changed_elms.items():
            new_rgb_values = will_be_changed_rgbs_new[key]
            for i in range(3): 
                elms[i].set('Value', str(new_rgb_values[i])) 
            tree.write(xml_path)
            replace_first_2_lines(xml_path, first_2line)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, cols, "pro", is_inspection, ignoreds]
        _ = core_process(core_input)
    return ignoreds

def move_and_compress_files(paths, sfx2dcx_dct, change_info, dcx2folder_dct):
    active_path = paths["active_path"]
    save_path = paths["save_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    for fn in os.listdir(active_path):
        from_path = f"{active_path}/{fn}"
        if fn.endswith(".fxr"): 
            final_dest = sfx2dcx_dct[fn]
            shutil.move(from_path, final_dest) 
    for dcx_fn, is_changed in change_info.items():
        if is_changed:
            dcx_folder_name = dcx2folder_dct[dcx_fn]
            print(f'\n>> Compressing "{dcx_folder_name}"..')
            witchy_subprocess([witchyBND_path, f"{save_path}/{dcx_folder_name}"])

def finalize_process(paths, mission_input, mission_fn, recolor_mission, change_info):
    save_path = paths["save_path"]
    mod_abs_path = paths["mod_abs_path"]
    if not os.path.exists(f"{mod_abs_path}/sfx"): os.mkdir(f"{mod_abs_path}/sfx")
    for dcx_fn, is_changed in change_info.items():
        fp = f"{save_path}/{dcx_fn}"
        mod_fp = f"{mod_abs_path}/sfx/{dcx_fn}"
        if is_changed: shutil.copyfile(fp, mod_fp)
    for color, rgba in recolor_mission.items():
        mission_input["target_colors"][color] = rgba 
    if not os.path.exists("logs"): os.mkdir("logs")
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_sn = f"logs/{mission_fn}_{curr_time}.json"
    custom_json_dumper(mission_input, log_sn)
    custom_json_dumper(mission_input, mission_fn)
    print("\n>> Recoloring was COMPLETED.\n")

def custom_json_dumper(data, fp, indent=4):
    with open(fp, 'w', encoding='utf8') as f:
        f.write('{\n')
        key_text1 = f'{" " * indent}"sfx_ids": ['
        f.write(key_text1)
        for i, item in enumerate(data['sfx_ids']):
            if i != 0: f.write(" " * len(key_text1))
            f.write(f'{item}')
            if i < len(data['sfx_ids']) - 1: f.write(',\n')
            else: f.write('],\n')
        key_text2 = f'{" " * indent}"target_colors": {{'
        f.write(key_text2)
        for i, (key, value) in enumerate(data['target_colors'].items()):
            if i != 0: f.write(" " * len(key_text2))
            f.write(f'"{key}": {value}')
            if i < len(data['target_colors']) - 1: f.write(',\n')
            else: f.write('}\n')
        f.write('}')
