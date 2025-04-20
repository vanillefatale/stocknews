@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! You can now activate the virtual environment using:
echo call venv\Scripts\activate 