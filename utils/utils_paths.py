import os
import json
import shutil
from pathlib import Path
from datetime import datetime

from utils.utils_common import log, witchy_subprocess, custom_json_dumper
from utils.utils_download import download_Witchy, download_ME2, download_UXM

def first_controls(config_fn, mission_fn):
    # assert_config_text = f"\n>> The file {config_fn} could not be found in the tool directory. The tool is ABORTED.\n"
    assert_mission_text = f"\n>> The file {mission_fn} could not be found in the tool directory. The tool is ABORTED.\n"
    assert_length_text = f"\n>> There must be at least 1 SFX ID in the {mission_fn} file. The tool is ABORTED.\n"
    # assert os.path.exists(config_fn), assert_config_text
    prepare_tools(config_fn)
    assert os.path.exists(mission_fn), assert_mission_text
    with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
    sfx_ids = mission_input["sfx_ids"]
    assert len(sfx_ids) > 0, assert_length_text
    suffix = "" if len(sfx_ids) == 1 else "s"
    return mission_input, sfx_ids, suffix

def prepare_tools(config_fn):
    if not os.path.exists(config_fn): 
        download_Witchy()
        download_ME2()
        download_UXM()
    else: check_tools_are_ready(config_fn)
        
def check_tools_are_ready(config_fn):
    with open(config_fn, "r", encoding="utf8") as f: config = json.load(f)
    elden_ring_abs_path = config.get("elden_ring_abs_path", "").replace("\\", "/")
    mod_abs_path = config.get("mod_abs_path", "").replace("\\", "/")
    mod_engine_abs_path = str(Path(mod_abs_path).parent).replace("\\", "/")
    witchyBND_path = config.get("witchyBND_abs_path", "").replace("\\", "/")
    witchyBND_path += "/WitchyBND.exe"
    if not os.path.exists(f"{elden_ring_abs_path}/Game/eldenring.exe"): pass
    if not os.path.exists(f"{elden_ring_abs_path}/Game/sfx"): pass
    if not os.path.exists(f"{mod_engine_abs_path}/launchmod_eldenring.bat"): pass
    if not os.path.exists(witchyBND_path): pass

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

def obtain_all_sfx_files():
    dcx2folder_dct = {"sfxbnd_commoneffects.ffxbnd.dcx": None,
                      "sfxbnd_commoneffects_dlc02.ffxbnd.dcx": None} 
    for dcx_fn, _ in dcx2folder_dct.items():
        dcx2folder_dct[dcx_fn] = dcx_fn.replace(".", "-") + "-wffxbnd"
    dcx2folder_dct = speed_up_search(dcx2folder_dct)
    return dcx2folder_dct

def speed_up_search(dcx2folder_dct): return dcx2folder_dct   # order common sfx fns to the top

def check_dcx_folder_in_path(paths, dcx_fn, dcx_folder_name):
    elden_ring_abs_path = paths["elden_ring_abs_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    main_path = paths['main_path']
    save_path = paths['save_path']
    if not os.path.exists(f"{main_path}/{dcx_folder_name}"):
        log.info(f'\t- Decompressing original "{dcx_folder_name}"..')
        from_fp = f"{elden_ring_abs_path}/Game/sfx/{dcx_fn}"
        to_fp = f"{main_path}/{dcx_fn}"
        command_fp = f"{main_path}/{dcx_fn}"
        shutil.copyfile(from_fp, to_fp)
        command = [witchyBND_path, command_fp]
        witchy_subprocess(command)
    else: log.info(f'\t- Found original "{dcx_folder_name}".')
    if not os.path.exists(f"{save_path}/{dcx_folder_name}"):
        log.info(f'\t- Loading modified "{dcx_folder_name}"..')
        from_fp = f"{main_path}/{dcx_folder_name}"
        to_fp = f"{save_path}/{dcx_folder_name}"
        shutil.copytree(from_fp, to_fp)
    else: log.info(f'\t- Found modified "{dcx_folder_name}".')

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
    prev_folder_name = "prev_missions"
    if not os.path.exists(prev_folder_name): os.mkdir(prev_folder_name)
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_sn = f"{prev_folder_name}/{mission_fn[:-4]}_{curr_time}.json"
    custom_json_dumper(mission_input, log_sn)
    custom_json_dumper(mission_input, mission_fn)
    log.info("\n>> Recoloring was COMPLETED.\n")

def move_and_compress_files(paths, sfx2dcx_dct, change_info, dcx2folder_dct):
    active_path = paths["active_path"]
    save_path = paths["save_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    for fn in os.listdir(active_path):
        from_path = f"{active_path}/{fn}"
        if fn.endswith(".fxr"): 
            final_dest = f"{save_path}/{sfx2dcx_dct[fn]}/effect/{fn}"
            shutil.move(from_path, final_dest) 
    for cnt, (dcx_fn, is_changed) in enumerate(change_info.items()):
        if is_changed:
            dcx_folder_name = dcx2folder_dct[dcx_fn]
            log.info(f'\t{cnt + 1} - Compressing "{dcx_folder_name}"..')
            witchy_subprocess([witchyBND_path, f"{save_path}/{dcx_folder_name}"])
