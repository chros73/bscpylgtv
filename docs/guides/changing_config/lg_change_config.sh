#!/bin/sh
# LG webOS TV Config Change Script
#
# Tested on: LG OLED77G26LA, webOS25 10.3.0, firmware 33.31.20

NODE_PATH=/tmp/node_modules:/usr/lib/node_modules:/usr/lib/nodejs
export NODE_PATH

# The webos-service node module requires pmloglib, which isn't available
# in the prisoner shell. This stub satisfies the dependency.
# Must be recreated after every reboot since /tmp is tmpfs.
setup_stub() {
    mkdir -p /tmp/node_modules
    echo 'function C(){return{log:function(){},info:function(){},warning:function(){},error:function(){}};}module.exports={log:function(){},info:function(){},warning:function(){},error:function(){},Console:C,Context:function(){return{log:function(){},info:function(){},warning:function(){},error:function(){}};}};' > /tmp/node_modules/pmloglib.js
    echo "[+] pmloglib stub created"
}

# Get current value from configd.
get_configd() {
    node -e '
var pb=require("palmbus"),h=new pb.Handle("",true);
h.call("luna://com.webos.service.config/getConfigs",
    JSON.stringify({configNames:["tv.conti.supportUsedTime"]}))
  .on("response",function(m){console.log("configd: "+m.payload());});
setTimeout(function(){process.exit(1);},1000);'
}

# Set configd overrides, persist through reboot.
set_configd() {
    node -e '
var pb=require("palmbus"),h=new pb.Handle("",true);
h.call("luna://com.webos.service.config/setConfigs",
  JSON.stringify({configs:{"tv.conti.supportUsedTime":true}}))
.on("response",function(m){console.log("[+] configd: "+m.payload());});
setTimeout(function(){process.exit(1);},1000);'
}

# Reboot via luna service
reboot_tv() {
    echo "Rebooting TV..."
    node -e '
var pb=require("palmbus");var h=new pb.Handle("",true);
h.call("luna://com.webos.service.sleep/shutdown/machineReboot", JSON.stringify({"reason":"remoteKey"}));
setTimeout(function(){process.exit(0);},3000);'
}

# --- Main ---
setup_stub

case "$1" in
    get)
        get_configd
        ;;
    set)
        set_configd
        ;;
    reboot)
        reboot_tv
        ;;
    *)
        echo "Usage: $0 <get|set|reboot>"
        echo ""
        echo "Examples:"
        echo "  $0 get           Get current config value"
        echo "  $0 set           Set config value"
        echo "  $0 reboot        Reboot the TV"
        echo ""
        exit 1
        ;;
esac
