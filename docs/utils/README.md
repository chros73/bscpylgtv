## Utility commands and scripts
This is a collection of useful commands and scripts to add support for new firmwares in the future and make PRs easier to do.

### Decompiling firmware
After installing [epk2extract](https://github.com/openlgtv/epk2extract), take a look at the [keys/AES.key](https://github.com/openlgtv/epk2extract/blob/master/keys/AES.key)  file whether there's a key for the given firmware. If there is then download and unzip the firmware into `build_linux` directory and decompile it by running:
```sh
fakeroot ./epk2extract new_firmware.epk
```
We are mostly interested in the `rootfs*` direcory, that's where most of the commands below works from.

### Creating a new available_settings_*.md file

#### Getting available Inputs, Presets, Dynamic ranges, settings for different categories:
Use the `merge_settings.py` script:
- create a new directery with the name of the model, e.g. `C2` and copy the following files into it:
    - `etc/palm/defaultSettings.json`
    - `etc/palm/description.json`
    - `usr/palm/services/com.webos.service.apiadapter/adapters/settings/valid-settings.js`
- run the script: `merge_settings.py C2`
- it spits out the merged settings MD file e.g. `C2/available_settings_C2.md`

#### Getting available Config keys:
```sh
find etc/configd/layers -type f -name "*.json" -printf "%f\n" | sort -u | sed 's/json$/\*/'
```
Note that couple of keys will be missing from this list (e.g tv.nyx, tv.hw, tv.rmm, com.webos.service.config), so we have to look through `usr/palm/applications/com.palm.app.settings/main.js` file manually as well to add the missing ones. Also it doesn't hurt to try them out manually with our device whether they are indeed valid. 

#### Adding more Buttons
These need to be tested manually whether they work or not! Take a look at these files:
- usr/share/X11/xkb/keycodes/lg
- usr/sbin/network-input-service

Also this one:
```sh
strings usr/sbin/lginput2 | grep -i '^KEY_' | sort -u | cut -d "_" -f 2,3,4,5,6,7,8
```

#### Getting part of DoVi config:
DoVi config files of newer models are located in `usr/share/pqdb/dolby` directory.
