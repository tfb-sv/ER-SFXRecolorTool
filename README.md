[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

<p align="center">
  <img src="https://github.com/tfb-sv/ER-SFXRecolorTool/blob/main/builders/recolor_logo.png?raw=true" />
</p>

# Elden Ring SFX Recolor Tool

**ER-SFXRecolorTool** is a modding tool for Elden Ring that automates and simplifies the SFX (FXR) recoloring procedure, particularly the cumbersome task of finding and adjusting RGBA values in XML files. The tool is built upon specific patterns I identified within these values.

- [NexusMods Page](https://www.nexusmods.com/eldenring/mods/6795)

## Prerequisites
- Ensure all game files are unpacked using [UXM Selective Unpacker](https://github.com/Nordgaren/UXM-Selective-Unpack.git).
- Be familiar with and ready to use [ModEngine2](https://github.com/soulsmods/ModEngine2.git) and [WitchyBND](https://github.com/ividyon/WitchyBND.git).

## Installation
1. Download the latest release of this tool.
2. Extract the tool folder from the downloaded file.
3. Place the extracted folder in a directory, such as the `Users\<your-windows-username>`, where file read/write permissions are unrestricted.

## Configuration
- Modify the `paths_config.json` to reflect your system paths.
- Enter the SFX (FXR) IDs you want to modify into the `recolor_mission.json`.

## Usage
1. Ensure that the steps outlined in the **Configuration** section are completed.
2. Launch the `ER-SFXRecolorTool.exe`.
3. Ensure **INSPECTION** mode is selected.
4. Click the **INSPECT** button.
5. After inspection, the tool automatically switches from **INSPECTION** to **RECOLORING** mode.
6. Review the color palettes displayed, and decide which colors to change.
7. Enter new RGB values for the colors you want to change into the tool's interface.
8. Click the **RECOLOR** button.
9. Launch the game using **ModEngine2** after the recoloring session is complete, no further action is needed.
10. (Optional) Fine-tune entered RGB values as needed. You may repeat the recoloring session in **RECOLORING** mode and check the effects in-game after each adjustment until the results meet your expectations.

## Known Issues
- The tool may sometimes get stuck in **INSPECTION** mode. As a temporary solution, instead of using **INSPECTION** mode, you can directly use **RECOLORING** mode to recolor a random color with a random RGB value. Once the process is complete, check the `sfx_palettes` folder for the color palettes and identify the colors you want to recolor. Then, recolor those specific colors with the desired RGB values.
- Recoloring attempts to black (0, 0, 0) as the new RGB values often result in green instead of black, or it may not turn out as desired. Similar issues might occur with white and gray colors, as they have not been extensively tested.

## Notes
- Covers SFX files of DLC as well as those from the base game.
- Examples can be found in the `examples` folder.
- Specifically designed to operate on the **Windows** platform.
- Does not make any changes to the original game folder, ensuring the integrity of the game files is maintained.
- Applies toning to entered RGB values, making the recoloring appear more realistic and aesthetically pleasing.
- No manual transfers of SFX-related files or folders are required.

## Additional Information
- The log file, `log.txt`, is reset and saved for each session. Any errors are recorded in this log file.
- `recolor_mission.json` files are stored with a datetime tag in the `prev_missions` folder for each recoloring session.
- Changes are saved in the `recolor_mission.json`, which automatically loads when the tool starts.
- The before and after color palettes of the SFX are available in the `sfx_palettes` folder, which is reset at the beginning of each session.
- To completely reset all modifications and start from scratch, simply delete the `sfx\modified_files` folder.
- To update the tool, replace the existing tool folder with the new version.
- Processes may take some time to complete, especially when compressing DCXs.

## Hints
- Group similar SFX files together for bulk modifications and restart the tool for the recoloring session of each group.
- Several iterations may be needed to achieve the desired result due to the simplicity of the toning approach.
- SFX IDs can be seen within the [Blacksmith](https://github.com/vawser/Smithbox.git) under tabs like **Bullet**, **SpEffectVfxParam**, etc. Alternatively, [FromSoftware FXR IDS](https://docs.google.com/spreadsheets/d/1gmUiSpJtxFFl0g04MWMIIs37W13Yjp-WUxtbyv99JIQ/edit?gid=866341224#gid=866341224) or similar Google spreadsheets can also be used to obtain SFX IDs.

## TODOs
- Resolve the issues listed under the **Known Issues** section.
- Incorporate CLI commands into the tool.
- Add support for other SFX-related DCX files, beyond the `sfxbnd_commoneffects.ffxbnd.dcx` and the `sfxbnd_commoneffects_dlc02.ffxbnd.dcx`.
- Remove the need to restart the tool for changes in the `recolor_mission.json` to take effect.
- Integrate the alpha (opacity) value into the recoloring procedure.
- Switch f-strings used for handling path operations to the `os` module.
- Explore more reliable toning approaches.
- Apply the quick compress option for the DCX compression processes.
- Include a button to open the tool folder.

## Contributing
Feedback and contributions are highly valued. Issues or suggestions for improvements can be reported by opening an issue on the **GitHub** repository, or by creating a post or posting a bug on **NexusMods**. Please report any anomalies or `IGNORED` messages in the message boxes. If you encounter `IGNORED` messages, including the CSV files in the `errors` folder into your issue report would be greatly appreciated.

## License
© 2024 [ineedthetail](https://github.com/tfb-sv).

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

**ER-SFXRecolorTool** uses the following licensed works:
- [WitchyBND](https://github.com/ividyon/WitchyBND.git) by [ividyon](https://github.com/ividyon) (see [License](https://github.com/ividyon/WitchyBND/blob/main/LICENSE))
- [ModEngine2](https://github.com/soulsmods/ModEngine2.git) by [SoulsMods](https://github.com/soulsmods) (see [License](https://github.com/soulsmods/ModEngine2/blob/main/LICENSE-MIT))

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Recoloring Attempts

### Successful Attempts:

- **Lightning Spear**
  - Orange: OK
  - Black: FAILED (it seems green)
- **Lightning Strike** (and its sparks)
  - Orange: OK
- **Ancient Lightning Spear** (of Gransax)
  - Orange: OK
- **Moonlight Sword**
  - Turquoise: OK
  - Red: OK
- **Glinstone Scrap**
  - Turquoise: OK
- **Founding Rain of Stars** (not complete, initial SFX seem to be in its original color)
  - Orange: OK
- **Nuke of Placidusax** (can't be sure due to too much visual effects)
  - Orange: OK
- **Comet Azur**
  - Green: OK
- **Comet**
  - Green: OK
- **Glinstone Arc**
  - Green: OK

### Failed Attempts:

- **Head of Frenzied Flame**
  - Purple: FAILED
  - Black: FAILED
- **Scarlet Aeonia** (actually some of the colors are changed, but there is a texture file that needs to be recolored, and this feature isn't implemented yet)
  - Turquoise: FAILED
