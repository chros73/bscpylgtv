# Change Log

## [v0.4.4](https://github.com/chros73/bscpylgtv/tree/v0.4.4) (2023-02-05)
**Implemented enhancements:**

- Add take_screenshot method
- Add ability to backup and restore 1D LUT, 3D LUT and 3x3 color matrix

## [v0.4.3](https://github.com/chros73/bscpylgtv/tree/v0.4.3) (2023-01-19)
**Implemented enhancements:**

- Use SSL for WebSocket connection by default (required by 2022 models)
- Add optional `-w` command line parameter for connecting without SSL
- Update available settings doc of 2022 models

## [v0.4.2](https://github.com/chros73/bscpylgtv/tree/v0.4.2) (2022-11-01)

**Fixed bugs:**

- Fix truncated large arrays with get calibration commands during returning

## [v0.4.1](https://github.com/chros73/bscpylgtv/tree/v0.4.1) (2022-10-29)
**Implemented enhancements:**

- Add `set_1d_lut_en` and `set_3by3_gamut_en` calibration methods
- Speed up most of the calibration commands by removing checking for calibration support from them:
    - only 3D LUT and Dolby Vision config related commands require `-s` (states) flag
- Modify `calibration_support_info` method to use chip type instead of model name
- Add optional `-c` command line parameter for overriding calibration_info for unsupported chip types
- Update readme

**Fixed bugs:**

- Fix truncated large arrays with get calibration commands during printing

## [v0.4.0](https://github.com/chros73/bscpylgtv/tree/v0.4.0) (2022-10-23)
**Implemented enhancements:**

- Modify `reboot_soft` method to support older WebOS as well
- Add `get_attached_devices` and `eject_attached_device` methods (requires new permission)
- Add `get_calibration_info` method

Calibration:
- Add support for newer OLED models
- Refactor and clean up calibration methods
- Rename `set_1d_en*` methods
- Rename `set_3by3_gamut_data*` methods
- Rename and split `ddc_reset` method into `set_bypass_modes_*` methods
- Add `set_3by3_gamut_data_hdr` method (only used in 2019 models)
- Add `get_*` get calibration methods
- Add support for resetting factory calibration data uploaded via calibration API
- Add Dolby Vision config file generation
- Add support for internal Test Pattern Generator (iTPG)
- Add unit tests
- Update readme

## [v0.3.2](https://github.com/chros73/bscpylgtv/tree/v0.3.2) (2022-07-17)
**Implemented enhancements:**

- Add available settings for 2022 models
- Add new buttons
- Add `reboot_soft` method
- Update readme with more examples
- Add commands and scripts to add support for new firmwares

## [v0.3.1](https://github.com/chros73/bscpylgtv/tree/v0.3.1) (2022-01-03)
**Fixed bugs:**

- Fix getting hello info

## [v0.3.0](https://github.com/chros73/bscpylgtv/tree/v0.3.0) (2022-01-02)
**Implemented enhancements:**

- Add support for turning PC mode on/off properly
- Add support for aiPicture category of picture settings for CX and newer models
- Allow JSON output for couple of methods
- Add available settings to docs

## [v0.2.9](https://github.com/chros73/bscpylgtv/tree/v0.2.9) (2021-12-25)
**Implemented enhancements:**

- Disconnect client when TV is off

**Fixed bugs:**

- Fix client reconnect (Closes [#2](https://github.com/chros73/bscpylgtv/pull/2))
- Fix other properties as well during disconnecting (e.g. storage, states)

## [v0.2.8](https://github.com/chros73/bscpylgtv/tree/v0.2.8) (2021-12-23)
**Implemented enhancements:**

- Allow minimum websocket package version (required by Home Assistant)

## [v0.2.7](https://github.com/chros73/bscpylgtv/tree/v0.2.7) (2021-12-19)
**Implemented enhancements:**

- Add new buttons
- Add `input_button` method

## [v0.2.6](https://github.com/chros73/bscpylgtv/tree/v0.2.6) (2021-12-18)
**Implemented enhancements:**

- Modify and remove unnecessary `turn_screen_*` methods

## [v0.2.5](https://github.com/chros73/bscpylgtv/tree/v0.2.5) (2021-12-17)
**Implemented enhancements:**

- Add optional `-o` command line parameter for getting hello info
- Add new buttons

**Fixed bugs:**

- Fix unhandled exception when QuickStart+ and TV is off (See [#1](https://github.com/chros73/bscpylgtv/pull/1))

## [v0.2.4](https://github.com/chros73/bscpylgtv/tree/v0.2.4) (2021-12-13)
**Implemented enhancements:**

- Add optional `-v` command line parameter for displaying version number
- Remove unnecessary button methods
- Add new buttons

## [v0.2.3](https://github.com/chros73/bscpylgtv/tree/v0.2.3) (2021-12-04)
**Implemented enhancements:**

- Add optional `-s` command line parameter for setting static states and state updates
- Remove obsolete `-g` command line parameter
- Pass `self` into state update callback functions

**Fixed bugs:**

- Make subscribed state updates fail more gracefully when not supported
- Fix result of couple of state updates

## [v0.2.2](https://github.com/chros73/bscpylgtv/tree/v0.2.2) (2021-12-01)
**Implemented enhancements:**

- Refactor key db methods into external storage class
- Remove obsolete `-d` command line parameter
- Required Python version >= 3.8

## [v0.2.1](https://github.com/chros73/bscpylgtv/tree/v0.2.1) (2021-11-27)
**Implemented enhancements:**

- Fix `turn_screen_off` and  `turn_screen_on` commands
- Add info about triggering hidden menus
- Add useful scripting examples into docs directory

## [v0.2.0](https://github.com/chros73/bscpylgtv/tree/v0.2.0) (2021-11-23)
**Implemented enhancements:**

- Add back previously removed calibration functionality
- Make calibration functionality optional (requires numpy package)
- Add optional `-d` command line parameter for disabling key file
- Publish Python package
- Upload optimized win64 binaries to release (lite: without calibration functionality)

## [v0.1.1](https://github.com/chros73/bscpylgtv/tree/v0.1.1) (2021-11-22)
**Implemented enhancements:**

- Add back previously removed subscribed and handler tasks

## [v0.1.0](https://github.com/chros73/bscpylgtv/tree/v0.1.0) (2021-10-02)
**Implemented enhancements:**

- Add optional `-k` command line parameter for client key
- Add optional `-p` command line parameter for path to key file
- Add optional `-l` command line parameter for listing all client keys from a key file

## [v0.0.9](https://github.com/chros73/bscpylgtv/tree/v0.0.9) (2021-10-01)
**Implemented enhancements:**

- Add `set_option_settings` function

## [v0.0.8](https://github.com/chros73/bscpylgtv/tree/v0.0.8) (2021-09-26)
**Implemented enhancements:**

- Add `get_apps_all` function

## [v0.0.7](https://github.com/chros73/bscpylgtv/tree/v0.0.7) (2021-09-25)
**Implemented enhancements:**

- Replace CX valid settings with C1 ones

## [v0.0.6](https://github.com/chros73/bscpylgtv/tree/v0.0.6) (2021-09-25)
**Implemented enhancements:**

- Replace C8 examples with CX ones

## [v0.0.5](https://github.com/chros73/bscpylgtv/tree/v0.0.5) (2021-09-24)
**Implemented enhancements:**

- Update default picture settings with CX expert2 preset
- Update docs

## [v0.0.4](https://github.com/chros73/bscpylgtv/tree/v0.0.4) (2021-09-23)
**Implemented enhancements:**

- Add `get_system_settings` function
- Add `get_configs` function
- Add info about launching Service Menus

## [v0.0.3 - Initial release](https://github.com/chros73/bscpylgtv/tree/v0.0.3) (2021-09-19)
**Implemented enhancements:**

- Remove calibration related functions
- Make commands run faster
- Add support for dictionary and list types in cmd line params
- Add `set_other_settings` function (can be used to turn PC mode on/off)
- Add `show_screen_saver` function
- Add `set_configs` function

