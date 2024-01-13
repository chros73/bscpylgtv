## Utility commands and scripts
This is a collection of useful commands and scripts to add support for new firmwares in the future and make PRs easier to do.

### Decompiling firmware
After installing [epk2extract](https://github.com/openlgtv/epk2extract), take a look at the [keys/AES.key](https://github.com/openlgtv/epk2extract/blob/master/keys/AES.key)  file whether there's a key for the given firmware. If there is then download and unzip the firmware into `build_linux` directory and decompile it by running:
```sh
fakeroot ./epk2extract new_firmware.epk
```
We are mostly interested in the `rootfs*` direcory, that's where most of the commands below works from.

### Creating a new available_settings_*.md file

#### Getting available Inputs:
```sh
grep category etc/palm/defaultSettings.json | cut -d '.' -f 1 | grep picture | cut -d '$' -f 2 | sort -u
```

#### Getting available Picture modes (presets):
```sh
grep category etc/palm/defaultSettings.json | grep picture | cut -d '.' -f 2 | sort -u
```

#### Getting available Dynamic range modes:
```sh
grep category etc/palm/defaultSettings.json | grep picture | cut -d '.' -f 4 | cut -d '"' -f 1 | sort -u
```

#### Getting available Stereoscopic modes:
```sh
grep category etc/palm/defaultSettings.json | grep picture | cut -d '.' -f 3 | sort -u
```

#### Getting available settings for aiPicture, Picture, Option, Other categories use the `merge_settings.py` script:
- edit `model` and `category` variables in it
- place and rename the `defaultSettings.json` file according to the model variable into the same directory as e.g. `defaultSettings-C2.json` 
- run the script: `merge_settings.py`
- it spits out the merged settings file e.g. other-C2.json
- repeat the steps for all the other categories

#### Getting available settings for System category form `getSettingsValidKeySet` section of:
```sh
cat usr/palm/services/com.webos.service.apiadapter/adapters/settings/valid-settings.js
```

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
