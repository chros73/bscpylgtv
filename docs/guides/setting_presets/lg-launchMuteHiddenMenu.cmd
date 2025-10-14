@echo off
REM set working directory to the current one
cd "%~dp0"
call lg_constants.cmd

REM Launch 3x Mute button hidden menu
%mcmd% launch_app_with_params com.webos.app.tvhotkey "{\"activateType\": \"mute-hidden-action\"}"
