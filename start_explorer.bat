@echo off
cd /d "%~dp0"
echo Starting local server for the GP access explorer...
echo Keep this window open while you use it. Close it when done.
rem start the server first (minimised), give it a moment, then open the browser
start "gp-explorer-server" /min cmd /c "python -m http.server 2>nul || py -m http.server"
timeout /t 2 /nobreak >nul
start "" http://localhost:8000/research/explore.html
echo Explorer opened in your browser. This window can stay open or be closed;
echo the minimised "gp-explorer-server" window is the actual server.
pause
