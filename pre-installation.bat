
ECHO = try to fix sdl2 for windows platform also docker pull
@for %%i in (python.exe) do @set fixsld2=%%~$PATH:i
set fixsld2=%fixsld2:python.exe=share\sdl2\bin%
echo %fixsld2%
setx path "%fixsld2%;%PATH%"
ECHO = Adding env variable: Done...
docker pull zlatnaspirala/crossk-pack:beta
ECHO = CrosskEngine: docker pull zlatnaspirala/crossk-pack:beta ... Done
