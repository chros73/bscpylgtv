@echo off
REM toggle inStart Service Menu

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
	%mcmd% launch_app_with_params com.webos.app.factorywin "{\"id\":\"executeFactory\", \"irKey\":\"inStart\"}"
	timeout 2
	%mcmd% number_button 0
	%mcmd% number_button 4
	%mcmd% number_button 1
	%mcmd% number_button 3
	echo 1 > %cname%
)
