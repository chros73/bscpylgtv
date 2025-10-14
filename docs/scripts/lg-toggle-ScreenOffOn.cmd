@echo off
REM toggle Screen off/on

REM set current dir, current and cookie file name variables
SET dname=%~dp0
SET fname=%~n0
SET cname=%fname%.coo

REM set working directory to the current one and import LG constants
cd %dname%
call lg_constants.cmd

if exist %cname% (
	REM exit app and delete cookie
	%mcmd% turn_screen_on
	del /q %cname%
) else (
	REM launch app and create cookie
	%mcmd% turn_screen_off
	echo 1 > %cname%
)
