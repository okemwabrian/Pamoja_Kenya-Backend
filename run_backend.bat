@echo off
echo Starting Pamoja Kenya Backend Setup...
echo =====================================

echo Installing requirements...
pip install -r requirements.txt

echo Setting up database...
python setup_database.py

echo Starting Django server...
python manage.py runserver 0.0.0.0:8000

pause