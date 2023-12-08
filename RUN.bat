@echo off
echo Installing dependencies...
pip install requests beautifulsoup4 art colorama httpx
echo Dependencies installed successfully.

echo.
echo Running Rule34 Image Parser for PO_N...
python "Rule34 Image Parser.py"
pause
