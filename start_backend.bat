@echo off
echo ================================================
echo PAMOJA KENYA BACKEND SERVER
echo ================================================
echo Starting Django backend server...
echo Backend will be available at: http://localhost:8000
echo API endpoints at: http://localhost:8000/api/
echo.
echo Press Ctrl+C to stop the server
echo ================================================
python manage.py runserver 0.0.0.0:8000
pause