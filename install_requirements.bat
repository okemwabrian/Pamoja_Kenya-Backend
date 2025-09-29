@echo off
echo Installing Python packages...
echo =============================

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install Django==5.0.1
pip install djangorestframework==3.14.0
pip install djangorestframework-simplejwt==5.3.0
pip install django-cors-headers==4.3.1
pip install python-decouple==3.8
pip install psycopg2-binary==2.9.9
pip install django-filter==23.5
pip install Pillow==10.2.0

echo =============================
echo Installation complete!
echo You can now run: python manage.py runserver
pause