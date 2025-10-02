@echo off
echo 🚀 Starting Pamoja Kenya Backend Verification
echo ============================================

echo.
echo 📊 Step 1: Creating test data...
python create_test_data.py

echo.
echo 🔧 Step 2: Starting Django server...
start /B python manage.py runserver

echo.
echo ⏳ Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo 🧪 Step 3: Running verification tests...
python backend_verification_test.py

echo.
echo 📧 Step 4: Testing email system...
python test_email_system.py

echo.
echo ✅ Verification complete!
echo Check the results above for any issues.
echo.
echo 📝 Manual test commands available in:
echo    BACKEND_COMMUNICATION_VERIFICATION.md
echo.
pause