[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

<p align="center">
  <img src="https://github.com/tfb-sv/ER-SFXRecolorTool/blob/main/builder/recolor_icon.png?raw=true" />
</p>

# Elden Ring SFX Recolor Tool

**ER-SFXRecolorTool** is a modding tool for Elden Ring that automates and simplifies the SFX (FXR) recoloring procedure, particularly the cumbersome task of finding and adjusting RGBA values within the XML files. The tool is built upon a pattern I identified in the RGBA values within the XML files, and this information is used throughout the tool.

- [NexusMods Page](https://www.nexusmods.com/eldenring/mods/xxxx)

## Prerequisites
- Ensure all game files are uncompressed using [UXM Selective Unpacker](https://github.com/Nordgaren/UXM-Selective-Unpack.git).
- Be familiar with and ready to use [ModEngine2](https://github.com/soulsmods/ModEngine2.git).
- Download [WitchyBND](https://github.com/ividyon/WitchyBND.git) to your computer.

## Notes
- Does not make any changes to the original game folder, ensuring the integrity of the game files is maintained.
- Applies toning to entered RGB values, making the recoloring appear more realistic and aesthetically pleasing.
- No manual transfers of SFX-related files or folders are required.
- Black, white, and gray colors as target colors have not been extensively tested, and the in-game results may not be as desired.

## Installation
1. Download the latest release of this tool.
2. Place the downloaded folder in a directory, such as the `Users`, where file read/write permissions are unrestricted.

## Configuration
- Modify the `path_config.json` to reflect your system paths.
- Enter the SFX (FXR) IDs you want to modify into the `recolor_mission.json`.

## Usage
0. Ensure that the steps outlined in the **Configuration** section are completed.
1. Run `ER-SFXRecolorTool.exe`.
2. Ensure **INSPECTION** mode is selected.
3. Click the **INSPECT** button.
4. After inspection, the tool automatically switches from **INSPECTION** to **RECOLORING** mode.
5. Review the color palettes displayed, and decide which colors to change.
6. Enter new RGB values for the colors you want to change into the tool's interface.
7. Click the **RECOLOR** button.
8. Launch the game using **ModEngine2** after the recoloring session is complete, no further action is needed.
9. (Optional) Fine-tune entered RGB values as needed. You may repeat the recoloring session in **RECOLORING** mode and check the effects in-game after each adjustment until the results meet your expectations.

## Additional Information
- Logs are stored with a datetime tag in the `logs` folder for each recoloring session.
- Changes are saved in the `recolor_mission.json`, which automatically loads when the tool starts.
- The before and after colors of the SFX are available in the `sfx_palettes`, which is reset at the beginning of each session.
- To completely reset all modifications and start from scratch, simply delete the `sfx\modified_files` folder.
- To update the tool, simply replace the existing tool folder with the new version.

## Hints
- Group similar SFX files together for bulk modifications and restart the tool for the recoloring session of each group.
- Several iterations may be needed to achieve the desired result due to in-game lightning settings and the simplicity of the toning approach.
- SFX IDs can be seen within the [Blacksmith](https://github.com/vawser/Smithbox.git) under tabs like **Bullet**, **SpEffectVfxParam**, etc. Alternatively, [FromSoftware FXR IDS](https://docs.google.com/spreadsheets/d/1gmUiSpJtxFFl0g04MWMIIs37W13Yjp-WUxtbyv99JIQ/edit?gid=866341224#gid=866341224) or similar Google spreadsheets can also be used to obtain SFX IDs.

## TODOs
1. Incorporate CLI commands into the tool.
2. Add support for other SFX-related DCX files, beyond the `sfxbnd_commoneffects.ffxbnd.dcx` and the `sfxbnd_commoneffects_dlc02.ffxbnd.dcx`.
3. Remove the need to restart the tool for changes in the `recolor_mission.json` to take effect.
4. Integrate the alpha (opacity) value into the recoloring procedure.
5. Switch f-strings used for handling path operations to the `os` module.
6. Link the window that opens after recoloring to a checkbox.

## Contributing
Feedback and contributions are highly valued. Issues or suggestions for improvements can be reported by opening an issue on the GitHub repository or posting a bug on NexusMods. Please report any anomalies or `IGNORED` messages in the message boxes. If you encounter `IGNORED` messages, including the CSV files in the `errors` folder into your issue report would be greatly appreciated.

## License
© 2024 [ineedthetail](https://github.com/tfb-sv).

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

ER-SFXRecolorTool uses the following licensed work(s):
- [WitchyBND](https://github.com/ividyon/WitchyBND.git) by [ividyon](https://github.com/ividyon) (see [License](https://github.com/ividyon/WitchyBND/blob/main/LICENSE))

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
