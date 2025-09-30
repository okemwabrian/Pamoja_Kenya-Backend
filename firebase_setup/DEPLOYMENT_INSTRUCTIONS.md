# Firebase Functions Deployment Instructions

## Prerequisites
1. Install Node.js (version 18 or higher)
2. Install Firebase CLI: `npm install -g firebase-tools`

## Setup Steps

### 1. Gmail App Password Setup
1. Go to your Gmail account settings
2. Enable 2-Factor Authentication
3. Go to Security → App passwords
4. Generate an app password for "Mail"
5. Copy the 16-character password

### 2. Firebase Project Setup
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project: "Pamoja Kenya"
3. Enable Cloud Functions
4. Note your project ID (usually: pamoja-kenya)

### 3. Deploy Functions
```bash
# Navigate to firebase_setup directory
cd firebase_setup

# Login to Firebase
firebase login

# Set your Gmail app password
firebase functions:config:set gmail.password="your-16-character-app-password"

# Install dependencies
npm install

# Deploy functions
firebase deploy --only functions
```

### 4. Get Function URLs
After deployment, you'll get URLs like:
- `https://us-central1-pamoja-kenya.cloudfunctions.net/sendEmail`
- `https://us-central1-pamoja-kenya.cloudfunctions.net/testEmail`

### 5. Update Django Settings
Add to your `.env` file:
```env
USE_FIREBASE_EMAIL=True
FIREBASE_EMAIL_FUNCTION_URL=https://us-central1-pamoja-kenya.cloudfunctions.net/sendEmail
```

### 6. Test Email Function
Visit: `https://us-central1-pamoja-kenya.cloudfunctions.net/testEmail`

## Available Functions

### sendEmail
- **URL**: `/sendEmail`
- **Method**: POST
- **Body**: `{ "to": "email@example.com", "subject": "Subject", "html": "<h1>HTML content</h1>" }`

### sendBulkEmails
- **URL**: `/sendBulkEmails`
- **Method**: POST
- **Body**: `{ "emails": [{ "to": "email1@example.com", "subject": "Subject 1", "html": "Content 1" }] }`

### testEmail
- **URL**: `/testEmail`
- **Method**: GET
- **Purpose**: Send test email to pamojakeny@gmail.com

## Troubleshooting

### Common Issues:
1. **Gmail password error**: Make sure you're using the app password, not your regular Gmail password
2. **CORS errors**: Functions include CORS headers for web requests
3. **Deployment errors**: Ensure you're logged into Firebase CLI with correct account

### View Logs:
```bash
firebase functions:log
```

### Local Testing:
```bash
firebase emulators:start --only functions
```

## Security Notes
- Gmail app password is stored securely in Firebase Functions config
- Functions include basic validation and error handling
- CORS is enabled for web requests