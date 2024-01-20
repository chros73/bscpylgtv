## First use

### On the TV
- enable TV On With Mobile under General - Devices - External Devices
- take a note of your IPv4 address under General - Network

### Install Windows binaries
[Download](https://github.com/chros73/bscpylgtv/releases) the lite or full version of the app, extract it into a directory, then open a cmd window from the bscpylgtv directory (it needs to be run from this directory all the time).

Run this command first to try it out, you will get a pairing prompt on the TV that you have to accept then it will display an info screen (not with built-in apps):

```sh
bscpylgtvcommand 192.168.1.18 button INFO
```

A `.aiopylgtv.sqlite` key db file will be created in the current directory that stores the key and the IP address for future connections.

### Notes about Windows binaries
- they don't require Python to be installed
    - you can't do python scripting then, but you can do Windows batch file scripting
- they are completely portable, meaning you can put it into any directory
    - you can have the lite version in one directory and the full version in another (e.g. you can use the lite version for all operations except for calibration tasks)
- you can add the `-p` command line switch to every request to specify the key db file and put that key db file into just one place, eg: `D:\config\.aiopylgtv.sqlite`
- the real power comes with windows batch scripting when it's paired with other utilities (e.g. [madvr-js-remote](https://github.com/chros73/madvr-js-remote) or [HTWebRemote
](https://github.com/nicko88/HTWebRemote) on Windows)

