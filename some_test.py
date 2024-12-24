import shutil
import subprocess
from xml.etree import ElementTree as ET
from utils.utils_recolor import find_all_groups, find_rgb_groups

sfx_id = 530701
sfx_fn = f"f{str(sfx_id).zfill(9)}.fxr"
sfx_from_fp = f"sfx/original_files/sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd/effect/{sfx_fn}" 
sfx_to_fp = f"sfx/active_files/{sfx_fn}" 
shutil.copyfile(sfx_from_fp, sfx_to_fp)

witchyBND_abs_path = "C:\\Users\\nural\\ERTools\\.standalones\\WitchyBND".replace("\\", "/")
witchyBND_abs_path += "/WitchyBND.exe"

command = [witchyBND_abs_path, sfx_to_fp, "-s"]
_ = subprocess.run(command)

xml_fn = f"{sfx_fn}.xml"
xml_fp = f"{sfx_to_fp}.xml"
tree = ET.parse(xml_fp)

all_rgb_groups, all_elm_groups = find_all_groups(tree)
chosen_rgb_groups, chosen_elm_groups, ignoreds = find_rgb_groups(all_rgb_groups, all_elm_groups, xml_fn, {}, False)

