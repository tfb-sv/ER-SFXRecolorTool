######################################################################################
import json
from utils_recolor import *
# RUNTIME WARNING KAPAT, PLOT ICIN GELIYOR !
######################################################################################

def main():
    config_fp = "paths_config.json"
    mission_fn = "z.recolor_mission.json"
    with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
    sfx_ids = mission_input["sfx_ids"]
    recolor_mission = prepare_recolor_mission(mission_input["target_colors"])
    validate_colors(recolor_mission)
    paths = initialize_paths(config_fp)
    check_if_original_files_in_path(paths)
    
    decompress_command, compress_xml_command = process_sfx_files(sfx_ids, paths)
    decompress_fxr_files(decompress_command)
    process_xml_files(paths["active_path"], recolor_mission, paths["graph_path"], False, 6)
    compress_xml_files(compress_xml_command)
    
    move_and_compress_files(paths["active_path"], paths["save_path"], 
                            paths["main_sfx_folder_name"], paths["witchyBND_abs_path"])
    finalize_process(paths["save_path"], paths["main_sfx_file_name"], 
                     paths["mod_abs_path"], paths["UXM_abs_path"])

###################################################################################### 

if __name__ == "__main__": main()

######################################################################################
