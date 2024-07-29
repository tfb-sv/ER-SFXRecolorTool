######################################################################################
from utils.utils_recolor import *
# RUNTIME WARNING KAPAT, PLOT ICIN GELIYOR !
######################################################################################

def main():
    config_fp = "utils/paths_config.json"
    mission_fn = "z.recolor_mission.json"
    mission_input = load_mission_input(mission_fn)
    sfx_ids = mission_input["sfx_ids"]
    recolor_mission = prepare_recolor_mission(mission_input["target_colors"])
    validate_colors(recolor_mission)
    paths = initialize_paths(config_fp)
    all_fxr_fps, all_xml_fps = process_sfx_files(sfx_ids, paths)
    decompress_fxr_files(all_fxr_fps)
    process_xml_files(paths["active"], recolor_mission, paths["graph"], False, 6)
    compress_xml_files(all_xml_fps)
    move_and_compress_files(paths["active"], paths["save"], 
                            paths["main_sfx_folder_name"], paths["witchyBND"])
    finalize_process(paths["save"], paths["main_sfx_file_name"], 
                     paths["elden_ring"], paths["UXM"])

###################################################################################### 

if __name__ == "__main__": main()

######################################################################################
