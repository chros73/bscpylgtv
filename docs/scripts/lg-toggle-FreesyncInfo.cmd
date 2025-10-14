@echo off
REM toggle Freesync info

REM set current dir, current and cookie file name variables
SET dname=%~dp0
SET fname=%~n0
SET cname=%fname%.coo

REM set working directory to the current one and import LG constants
cd %dname%
call lg_constants.cmd

if exist %cname% (
	REM exit app and delete cookie
	%mcmd% button BACK
	del /q %cname%
) else (
	REM launch app and create cookie
	%mcmd% launch_app_with_params com.webos.app.tvhotkey "{\"activateType\": \"freesync-info\"}"
	echo 1 > %cname%
)
