@echo off
setlocal
set "PLUGIN_ROOT=%~dp0.."
if not defined COLLAB_TTT_DATA_DIR set "COLLAB_TTT_DATA_DIR=%LOCALAPPDATA%\CollaborativeTicTacToe"
if not exist "%COLLAB_TTT_DATA_DIR%" mkdir "%COLLAB_TTT_DATA_DIR%"
set "COLLAB_TTT_DB=%COLLAB_TTT_DATA_DIR%\games.sqlite3"
"%PLUGIN_ROOT%\.venv\Scripts\collab-tic-tac-toe-mcp.exe"
