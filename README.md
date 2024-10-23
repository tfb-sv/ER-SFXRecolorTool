[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

<p align="center">
  <img src="https://github.com/tfb-sv/ER-SFXRecolorTool/blob/main/builder/recolor_icon.png?raw=true" />
</p>

# Elden Ring SFX Recolor Tool

**ER-SFXRecolorTool** is a modding tool for Elden Ring that automates and simplifies the SFX (FXR) recoloring process, particularly the cumbersome task of finding and adjusting RGBA values within the XML files. *I have identified a pattern for RGBA values in the XML files and utilized this information into this tool.*

- [NexusMods Page](https://www.nexusmods.com/eldenring/mods/xxxx)

## Prerequisites
- Ensure all game files are uncompressed using [UXM Selective Unpacker](https://github.com/Nordgaren/UXM-Selective-Unpack.git).
- Be familiar with and ready to use [ModEngine2](https://github.com/soulsmods/ModEngine2.git).
- Download [WitchyBND](https://github.com/ividyon/WitchyBND.git) to your computer.

## Notes
- This tool is specifically designed to operate on the **Windows** platform.
- The tool does not make any changes to the original game folder, ensuring the integrity of the game files is maintained.
- Applies toning to entered RGB values, making the recoloring appear more realistic and aesthetically pleasing.
- No manual transfers of SFX-related files or folders are required.
- Black, white, and gray colors as target colors have not been extensively tested, and the in-game results may not be as desired.

## Installation
1. Download the latest release of this tool.
2. Place the downloaded folder in a directory, such as the `Users` directory, *where file read/write permissions are unrestricted*.

## Configuration
- Modify the `path_config.json` to reflect your system paths.
- Enter the SFX (FXR) numbers you want to modify into the `recolor_mission.json`.

## Usage
0. Ensure that the steps outlined in the **Configuration** section are completed.
1. Run `ER-SFXRecolorTool.exe`.
2. Ensure **INSPECTION** mode is selected.
3. Click the **INSPECT** button.
4. After inspection, the tool automatically switches from **INSPECTION** to **RECOLORING** mode.
5. Review the color palettes displayed, and decide which colors to change.
6. Enter new RGB values for the colors you want to change into the tool's interface.
7. Click the **RECOLOR** button.
8. ?? Launch the game using **ModEngine2** after the recoloring session is complete, no further action is needed.
9. (Optional) Fine-tune entered RGB values as needed. You may repeat the recoloring session from **RECOLORING** mode and check the effects in-game after each adjustment until the results meet your satisfaction.

## Additional Information
- Logs are stored with a datetime tag in the `logs` folder for each recoloring session.
- Changes are saved in the `recolor_mission.json`, which automatically loads when the tool starts.
- The before and after colors of the SFX are available in the `sfx_palettes`, which is reset at the beginning of each recoloring session.
- The inspection session is not strictly necessary, but it serves as an important sanity check.
- To completely reset all modifications and start from scratch, simply delete the `sfx/modified_files` folder.
- If there are no mods in the `ModEngine2` folder, use `ModEngine2/mod` as one of the required inputs for the `path_config.json`.
- You need to edit the `ModEngine2/config_eldenring.toml` for the **Launch game after recoloring** checkbox option if you are using a mod folder name that is different from the default.
- JSON files are editable with text editors like **Notepad++**.

## Hints
- Group similar SFX files together for bulk modifications and restart the tool for the recoloring session of each group.
- Several iterations may be needed until a satisfactory result is achieved.
- SFX IDs can be seen within the [Blacksmith](https://github.com/vawser/Smithbox.git) under tabs like **Bullet**, **SpEffectVfxParam**, etc. Alternatively, [FromSoftware FXR IDS](https://docs.google.com/spreadsheets/d/1gmUiSpJtxFFl0g04MWMIIs37W13Yjp-WUxtbyv99JIQ/edit?gid=866341224#gid=866341224) or similar Google spreadsheets can also be used to obtain SFX IDs.

## TODOs
1. Incorporate CLI commands into the tool.
2. Add support for other SFX-related DCX files, beyond the `sfxbnd_commoneffects.ffxbnd.dcx` and the `sfxbnd_commoneffects_dlc02.ffxbnd.dcx`.
3. Remove the need to restart the tool for changes in the `recolor_mission.json` to take effect.
4. Integrate the alpha (opacity) value into the tool??procedure.

## Contributing
Feedback and contributions are highly valued. Issues or suggestions for improvements can be reported by opening an issue on the GitHub repository or posting a bug on NexusMods. ?? Please report any anomalies or `IGNORED` outputs seen in the command line.

Your feedback?? helps improve the tool for all users!

## License
© 2024 [ineedthetail](https://github.com/tfb-sv).

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

ER-SFXRecolorTool is built using the following licensed work(s):
- [WitchyBND](https://github.com/ividyon/WitchyBND.git) by [ividyon](https://github.com/ividyon) (see [License](https://github.com/ividyon/WitchyBND/blob/main/LICENSE))

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
