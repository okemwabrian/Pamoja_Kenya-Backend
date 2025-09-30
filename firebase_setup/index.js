const functions = require('firebase-functions');
const nodemailer = require('nodemailer');

// Configure Gmail transporter
const transporter = nodemailer.createTransporter({
  service: 'gmail',
  auth: {
    user: 'pamojakeny@gmail.com',
    pass: functions.config().gmail.password // Set via: firebase functions:config:set gmail.password="your-app-password"
  }
});

// Send Email Function
exports.sendEmail = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).send('');
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { to, subject, html, text } = req.body;

  // Validate required fields
  if (!to || !subject || (!html && !text)) {
    res.status(400).json({ error: 'Missing required fields: to, subject, and html or text' });
    return;
  }

  try {
    const mailOptions = {
      from: 'Pamoja Kenya MN <pamojakeny@gmail.com>',
      to: to,
      subject: subject,
      html: html,
      text: text || html.replace(/<[^>]*>/g, '') // Strip HTML if no text provided
    };

    const result = await transporter.sendMail(mailOptions);
    
    console.log('Email sent successfully:', result.messageId);
    res.status(200).json({ 
      success: true, 
      messageId: result.messageId,
      message: 'Email sent successfully' 
    });

  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ 
      error: 'Failed to send email', 
      details: error.message 
    });
  }
});

// Send Bulk Emails Function
exports.sendBulkEmails = functions.https.onRequest(async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).send('');
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { emails } = req.body; // Array of email objects

  if (!emails || !Array.isArray(emails)) {
    res.status(400).json({ error: 'emails array is required' });
    return;
  }

  const results = [];
  const errors = [];

  for (const email of emails) {
    try {
      const mailOptions = {
        from: 'Pamoja Kenya MN <pamojakeny@gmail.com>',
        to: email.to,
        subject: email.subject,
        html: email.html,
        text: email.text || email.html.replace(/<[^>]*>/g, '')
      };

      const result = await transporter.sendMail(mailOptions);
      results.push({ to: email.to, messageId: result.messageId, success: true });

    } catch (error) {
      console.error(`Error sending email to ${email.to}:`, error);
      errors.push({ to: email.to, error: error.message });
    }
  }

  res.status(200).json({
    success: true,
    sent: results.length,
    failed: errors.length,
    results: results,
    errors: errors
  });
});

// Test Function
exports.testEmail = functions.https.onRequest(async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  
  try {
    const testEmail = {
      from: 'Pamoja Kenya MN <pamojakeny@gmail.com>',
      to: 'pamojakeny@gmail.com',
      subject: 'Firebase Functions Test Email',
      html: '<h1>Test Email</h1><p>Firebase Functions email service is working!</p>',
      text: 'Test Email - Firebase Functions email service is working!'
    };

    const result = await transporter.sendMail(testEmail);
    
    res.status(200).json({
      success: true,
      message: 'Test email sent successfully',
      messageId: result.messageId
    });

  } catch (error) {
    console.error('Test email error:', error);
    res.status(500).json({
      error: 'Test email failed',
      details: error.message
    });
  }
});