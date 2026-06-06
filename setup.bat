@echo off
echo ==================================================
echo Installing Prilaksa Voice Assistant Dependencies
echo ==================================================
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==================================================
echo Setup complete! 
echo To run Prilaksa, use the command: python main.py
echo ==================================================
pause
