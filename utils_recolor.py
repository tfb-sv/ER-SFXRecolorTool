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

######################################################################################

def validate_colors(recolor_mission=None):
    all_colors = ["white", "black", "gray", "red", "orange", "yellow", "green", "blue", "purple", "pink"]
    if not recolor_mission: return all_colors
    assert all(color in all_colors for color in recolor_mission.keys())
    return all_colors

######################################################################################

def initialize_paths(config_file):
    with open(config_file, "r", encoding="utf8") as f: config = json.load(f)

    elden_ring_abs_path = config["elden_ring_abs_path"]
    mod_abs_path = config["mod_abs_path"]
    witchyBND_path = config["witchyBND_abs_path"]

    sfx_tmp_path = config["sfx_tmp_path"]
    graph_path = config["graph_path"]
    main_sfx_file_name = config["main_sfx_file_name"]
    main_sfx_folder_name = main_sfx_file_name.replace(".", "-") + "-wffxbnd"
    main_sfx_dlc_file_name = config["main_sfx_dlc_file_name"]
    main_sfx_dlc_folder_name = main_sfx_dlc_file_name.replace(".", "-") + "-wffxbnd"

    main_path = f"{sfx_tmp_path}/orj_backup"
    save_path = f"{sfx_tmp_path}/all_success_altereds"
    active_path = f"{sfx_tmp_path}/active_files"

    if not os.path.exists(main_path): os.mkdir(main_path)
    if not os.path.exists(save_path): os.mkdir(save_path)
    if os.path.exists(active_path): shutil.rmtree(active_path) 
    os.mkdir(active_path)

    paths = {
        "elden_ring_abs_path": elden_ring_abs_path,
        "mod_abs_path": mod_abs_path,
        "witchyBND_abs_path": witchyBND_path,
        "sfx_tmp_path": sfx_tmp_path,
        "graph_path": graph_path,
        "main_sfx_folder_name": main_sfx_folder_name,
        "main_sfx_file_name": main_sfx_file_name,
        "main_sfx_dlc_folder_name": main_sfx_dlc_folder_name,
        "main_sfx_dlc_file_name": main_sfx_dlc_file_name,
        "main_path": main_path,
        "save_path": save_path,
        "active_path": active_path
    }

    return paths

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
            if not isinstance(v[j], list): 
                print(f"\n>> {v[j]} is not a list ! j = {j}, len(v) = {len(v)}. IGNORED.")
                continue
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
                transform=ax.transAxes,
                bbox=dict(facecolor='white'))
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

def prepare_recolor_mission(recolor_mission):
    return {color: [value / 255 for value in rgb] for color, rgb in recolor_mission.items()}

######################################################################################

def check_if_original_files_in_path(paths):
    main_sfx_folder_name = paths['main_sfx_folder_name']
    if not os.path.exists(f"{paths['main_path']}/{main_sfx_folder_name}"):
        print(f'\n>> Original folder {main_sfx_folder_name} could NOT be found. It has started to be decompressed via WitchyBND.\n')
        shutil.copyfile(f"{paths['elden_ring_abs_path']}/{paths['main_sfx_file_name']}", 
                        f"{paths['main_path']}/{paths['main_sfx_file_name']}")
        decompress_main_sfx_file_command = [paths['witchyBND_abs_path'], 
                                            f"{paths['main_path']}/{paths['main_sfx_file_name']}",
                                            '-p']
        _ = subprocess.run(decompress_main_sfx_file_command)
    else: print(f'\n>> Original folder {main_sfx_folder_name} could be found.')
    if not os.path.exists(f"{paths['save_path']}/{main_sfx_folder_name}"):
        print(f'\n>> Updated folder {main_sfx_folder_name} could NOT be found. Original SFX were loaded.')
        shutil.copyfile(f"{paths['main_path']}/{main_sfx_folder_name}", 
                        f"{paths['save_path']}/{main_sfx_folder_name}")
    else: print(f'\n>> Updated folder {main_sfx_folder_name} could be found. Updated SFX were loaded and PROTECTED.')
    main_sfx_dlc_folder_name = paths['main_sfx_dlc_folder_name']
    if not os.path.exists(f"{paths['main_path']}/{main_sfx_dlc_folder_name}"):
        print(f'\n>> Original folder {main_sfx_dlc_folder_name} could NOT be found. It has started to be decompressed via WitchyBND.\n')
        shutil.copyfile(f"{paths['elden_ring_abs_path']}/{paths['main_sfx_dlc_file_name']}", 
                        f"{paths['main_path']}/{paths['main_sfx_dlc_file_name']}")
        decompress_main_sfx_file_command = [paths['witchyBND_abs_path'], 
                                            f"{paths['main_path']}/{paths['main_sfx_dlc_file_name']}",
                                            '-p']
        _ = subprocess.run(decompress_main_sfx_file_command)
    else: print(f'\n>> Original folder {main_sfx_dlc_folder_name} could be found.')
    if not os.path.exists(f"{paths['save_path']}/{main_sfx_dlc_folder_name}"):
        print(f'\n>> Updated folder {main_sfx_dlc_folder_name} could NOT be found. Original SFX were loaded.')
        shutil.copyfile(f"{paths['main_path']}/{main_sfx_dlc_folder_name}", 
                        f"{paths['save_path']}/{main_sfx_dlc_folder_name}")
    else: print(f'\n>> Updated folder {main_sfx_dlc_folder_name} could be found. Updated SFX were loaded and PROTECTED.')


######################################################################################

def process_sfx_files(sfx_ids, paths):
    decompress_fxr_command = [paths["witchyBND_abs_path"]]
    for sfx_id in sfx_ids:
        sfx_fn = f"f000{sfx_id}.fxr"
        sfx_path = f"{paths['main_path']}/{paths['main_sfx_folder_name']}/effect/{sfx_fn}"
        if not os.path.exists(sfx_path): 
            print(f">> {sfx_id} could not be found in game files !")
            continue
        main_fp = f"{paths['main_path']}/{sfx_fn}"
        active_fp = f"{paths['active_path']}/{sfx_fn}"
        shutil.copyfile(sfx_path, main_fp)
        shutil.copyfile(sfx_path, active_fp)
        decompress_fxr_command.append(active_fp)
    decompress_fxr_command.append("-p")
    compress_xml_command = [f"{fxr_file}.xml" for fxr_file in decompress_fxr_command[1:-1]]
    compress_xml_command = [decompress_fxr_command[0]] + compress_xml_command + [decompress_fxr_command[-1]]
    return decompress_fxr_command, compress_xml_command

######################################################################################

def decompress_fxr_files(decompress_fxr_command):
    _ = subprocess.run(decompress_fxr_command)
    print('\n>> FXR files were decompressed to XML files via WitchyBND.\n')

######################################################################################

def process_xml_files(recolor_mission, active_path, graph_path, isDeactivateAlpha, cols, is_inspection):
    cnt = 0
    for fn in os.listdir(active_path):
        xml_path = f"{active_path}/{fn}"
        if not fn.endswith(".xml"): 
            os.remove(xml_path)
            continue
        cnt += 1
        with open(xml_path, "r", encoding="utf8") as f: first_2line = f.readlines()[:2]
        print(f">> {cnt} - {fn} has started to be processed..")
        tree = ET.parse(xml_path)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, isDeactivateAlpha, cols, "pre"]
        core_output = core_process(core_input)
        if is_inspection: continue
        [will_be_changed_rgbs, will_be_changed_elms, will_be_changed_clrs, chosen_rgb_groups, chosen_elm_groups, all_rgb_groups, all_elm_groups] = core_output
        will_be_changed_rgbs_new = create_toning(will_be_changed_rgbs, will_be_changed_clrs, recolor_mission)
        for key, elms in will_be_changed_elms.items():
            new_rgb_values = will_be_changed_rgbs_new[key]
            for i in range(3): 
                elms[i].set('Value', str(new_rgb_values[i])) 
            tree.write(xml_path)   # , encoding="utf-8", xml_declaration=True
            replace_first_2_lines(xml_path, first_2line)
        core_input = [tree, recolor_mission.keys(), fn, graph_path, isDeactivateAlpha, cols, "pro"]
        _ = core_process(core_input)
    print("\n")

######################################################################################

def compress_xml_files(compress_xml_command):
    _ = subprocess.run(compress_xml_command)
    print('\n>> XML files were compressed to FXR files via WitchyBND.')

######################################################################################

def move_and_compress_files(paths):
    active_path = paths["active_path"]
    save_path = paths["save_path"]
    main_sfx_folder_name = paths["main_sfx_folder_name"]
    witchyBND_path = paths["witchyBND_abs_path"]
    for fn in os.listdir(active_path):
        from_path = f"{active_path}/{fn}"
        to_path = f"{save_path}/{fn}"
        final_dest = f"{save_path}/{main_sfx_folder_name}/effect/{fn}"
        if fn.endswith(".fxr"): shutil.move(from_path, final_dest) 
        # shutil.move(from_path, to_path)
    _ = subprocess.run([witchyBND_path, f"{save_path}/{main_sfx_folder_name}", "-p"])
    print(f'\n>> Folder {main_sfx_folder_name} was compressed via WitchyBND.')

######################################################################################

def finalize_process(paths):
    save_path = paths["save_path"]
    main_sfx_file_name = paths["main_sfx_file_name"]
    mod_abs_path = paths["mod_abs_path"]
    fp = f"{save_path}/{main_sfx_file_name}"
    mod_fp = f"{mod_abs_path}/{main_sfx_file_name}"
    shutil.copyfile(fp, mod_fp)
    # save mission file !   # here
    print("\n>> Process was COMPLETED !\n")

######################################################################################
    