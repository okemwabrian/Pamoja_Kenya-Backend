@echo off
echo Setting up Pamoja Kenya Firebase Functions...
echo.

echo Step 1: Installing Firebase CLI globally...
call npm install -g firebase-tools

echo.
echo Step 2: Login to Firebase...
call firebase login

echo.
echo Step 3: Setting Gmail app password...
echo Please enter your Gmail app password (16 characters):
set /p gmail_password="Gmail App Password: "
call firebase functions:config:set gmail.password="%gmail_password%"

echo.
echo Step 4: Installing project dependencies...
call npm install

echo.
echo Setup complete! Now run deploy.bat to deploy functions.
echo.
pause