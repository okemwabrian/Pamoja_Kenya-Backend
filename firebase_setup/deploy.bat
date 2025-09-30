@echo off
echo Deploying Pamoja Kenya Firebase Functions...
echo.

echo Step 1: Installing dependencies...
call npm install

echo.
echo Step 2: Deploying functions to Firebase...
call firebase deploy --only functions

echo.
echo Deployment complete!
echo.
echo Your email function URL:
echo https://us-central1-pamoja-kenya.cloudfunctions.net/sendEmail
echo.
echo Test email function:
echo https://us-central1-pamoja-kenya.cloudfunctions.net/testEmail
echo.
pause