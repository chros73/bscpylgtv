# LG webOS TV Config Change (No Root Required)

Change a config value on LG webOS TVs in configd overrides.

**Tested on:** LG OLED77G26LA, webOS25 10.3.0, firmware 33.31.20

## Why This Exists

Previously, changing config values required root access. This method uses NodeJS, which has no such restriction. No root required.

## Usage

### Prerequisites

- TV and computer on the same network
- LG Developer Mode enabled on the TV

### 1. Enable Developer Mode

1. On the TV, open the **LG Content Store**
2. Search for and install **Developer Mode**
3. Open the Developer Mode app and sign in with your LG account
4. Enable **Dev Mode Status** (the TV will reboot)
5. After reboot, re-open Developer Mode and enable **Key Server**

### 2. Download the SSH Key

With Key Server enabled, run on your **computer**:

```bash
# Run on computer
wget http://<TV_IP>:9991/webos_rsa -O lg_private.key
chmod 600 lg_private.key
```

### 3. Copy Script and SSH In

Run on your **computer**:

```bash
# Run on computer — copy script to TV
scp -i lg_private.key \
    -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    -P 9922 change_region.sh prisoner@<TV_IP>:/tmp/

# Run on computer — SSH into TV
ssh -i lg_private.key \
    -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    -p 9922 prisoner@<TV_IP>
```

> **Note:** You will be prompted for a passphrase — this is shown on the **Developer Mode app** screen on your TV. It is **case-sensitive**. The `-o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa` flags are required because the TV uses the legacy `ssh-rsa` algorithm that newer SSH clients disable by default.

### 4. Change a config value

Once SSH'd into the TV:

```bash
# Run on TV — Get current config value
sh /tmp/lg_change_config.sh get

# Run on TV — Set config value
sh /tmp/lg_change_config.sh set
```

Reboot the TV (optional):

```bash
# Run on TV
sh /tmp/lg_change_config.sh reboot
```

> **Note:** The script and pmloglib stub live in `/tmp`, which is cleared on every reboot. You'll need to copy the script again after a reboot if you want to re-run it.

### Verify via EZ-Adjust (optional)

You can visually confirm the area code using [bscpylgtv](https://github.com/chros73/bscpylgtv):

1. Send the **IN-START** (or **EZ-Adjust**) service remote command to open the service menu (code: 0413)

### Changing other config values

To change a different config value, replace the config name and value in `get_configd()` and `set_configd()` functions.

## Troubleshooting

### SSH connection refused
- Ensure developer mode is enabled on the TV
- Use port 9922, not 22
- Add `-o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa` flags

## How It Works

LG webOS has three layers of region configuration:

1. **NVRAM** (hardware) — `contiArea2All` packed value, read by `factorymanager` at boot
2. **configd** (software) — priority-based config system, overridable via `setConfigs`
3. **Settings DB** — user-facing settings like country name

The `factorymanager` service has an internal ACL that blocks writing `contiArea2All` from unauthorized callers. Even the anonymous palmbus Handle (which bypasses luna-service2 bus security) gets "Permission denied."

However, `com.webos.service.lowlevelstorage` provides direct NVRAM read/write access through its `getData`/`setData` methods without any such restriction. This service is the same one that `hw-option-gen` uses to export NVRAM values to selector files at boot.

### Key Technical Details

- **Anonymous palmbus Handle**: `new pb.Handle("", true)` creates an anonymous private-bus client that bypasses luna-service2 identity checks
- **pmloglib stub**: The webos-service node module requires pmloglib, which isn't available in the prisoner shell. A stub module satisfies the dependency.
- **lowlevelstorage dbids**: Valid database groups are `system`, `factory`, `micom`, `audio`
- **Persistence**: NVRAM writes survive reboots, power cycles, and factory resets of software settings

## Shell Limitations

The prisoner shell on webOS is BusyBox-based with several restrictions:

- **No heredocs** — `cat << EOF` doesn't work. Use `echo 'content' > file` or `cat > file` with Ctrl+D instead.
- **No `luna-send`** — the binary is root-only (`-rwx------`). Use the palmbus node module via the anonymous Handle instead.
- **`luna-send-pub`** is available but limited to the public bus — most write operations are blocked.
- **`strings` command** cannot access binaries in `/usr/sbin/` (not readable by prisoner).
- **BusyBox `grep`** doesn't support `\|` alternation — use `grep -E 'a|b'` instead.
- **`/tmp` is tmpfs** — everything in `/tmp` is lost on reboot, including the script and pmloglib stub.

## Disclaimer

This is for educational and personal use. Modifying TV firmware settings may void your warranty. The author is not responsible for any damages to your TV. Use at your own risk.

## Credits

- [epk2extract](https://github.com/openlgtv/epk2extract) by Smx for firmware extraction
- [bscpylgtv](https://github.com/chros73/bscpylgtv) — library to control webOS based LG TVs, used to access EZ-Adjust
- [lg-geolock-bypass](https://github.com/lennylxx/lg-geolock-bypass) — LG webOS TV Region Change
