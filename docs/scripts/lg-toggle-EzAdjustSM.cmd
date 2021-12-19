@echo off
REM toggle ezAdjust Service Menu

REM set current dir, current and cookie file name variables
SET dname=%~dp0
SET fname=%~n0
SET cname=%fname%.coo

REM set working directory to the current one and import LG constants
cd %dname%
call lg_constants.cmd

if exist %cname% (
	REM exit app and delete cookie
	%mcmd% close_app com.webos.app.factorywin
	del /q %cname%
) else (
	REM launch app and create cookie
	%mcmd% launch_app_with_params com.webos.app.factorywin "{\"id\":\"executeFactory\", \"irKey\":\"ezAdjust\"}"
	timeout 2
	%mcmd% button 0
	%mcmd% button 4
	%mcmd% button 1
	%mcmd% button 3
	echo 1 > %cname%
)
