######################################################################################
# conda activate torch-lnn
# cd C:\Users\nural\ER-SFXRecolorTool
# python recolor_sfx.py

import json
from utils_recolor import *
# RUNTIME WARNING KAPAT, PLOT ICIN GELIYOR !
######################################################################################

def main(is_inspection):
    config_fp = "paths_config.json"
    mission_fn = "z.recolor_mission.json"
    with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
    sfx_ids = mission_input["sfx_ids"]
    graph_clm_cnt = 6
    isDeactivateAlpha = False
    
    recolor_mission = prepare_recolor_mission(mission_input["target_colors"])
    validate_colors(recolor_mission)
    paths = initialize_paths(config_fp)
    
    check_if_original_files_in_path(paths)
    
    decompress_fxr_command, compress_xml_command = process_sfx_files(sfx_ids, paths)
    decompress_fxr_files(decompress_fxr_command)
    process_xml_files(recolor_mission, paths["active_path"], paths["graph_path"], 
                      isDeactivateAlpha, graph_clm_cnt, is_inspection)

    if is_inspection:
        print("\n>> Inspection was COMPLETED !\n")
        exit(0)

    compress_xml_files(compress_xml_command)
    move_and_compress_files(paths)
    finalize_process(paths)

###################################################################################### 

if __name__ == "__main__": 
    is_inspection = False
    main(is_inspection)

######################################################################################
