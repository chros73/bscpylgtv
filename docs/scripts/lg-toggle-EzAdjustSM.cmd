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
	del /q %cname%
	%mcmd% close_app com.webos.app.factorywin
) else (
	REM launch app and create cookie
	%mcmd% launch_app_with_params com.webos.app.factorywin "{\"id\":\"executeFactory\", \"irKey\":\"ezAdjust\"}" , ^
	sleep 2 , ^
	button 0 , ^
	button 4 , ^
	button 1 , ^
	button 3

	echo 1 > %cname%
)
