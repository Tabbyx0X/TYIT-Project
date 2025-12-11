const express = require('express');
const router = express.Router();
const User = require('../models/User');
const College = require('../models/College');
const { asyncHandler } = require('../middleware/errorHandler');
const { isAuthenticated } = require('../middleware/auth');
const { registerValidation, loginValidation, validate } = require('../middleware/validation');

// @route   POST /api/auth/register
// @desc    Register new user
// @access  Public
router.post('/register', registerValidation, validate, asyncHandler(async (req, res) => {
  const { name, email, password, collegeCode, department, phoneNumber } = req.body;

  // Check if user exists
  let user = await User.findOne({ email: email.toLowerCase() });
  if (user) {
    return res.status(400).json({ 
      success: false, 
      error: 'User already exists with this email' 
    });
  }

  // Verify college code
  const college = await College.findOne({ 
    code: collegeCode.toUpperCase(), 
    isActive: true 
  });

  if (!college) {
    return res.status(400).json({ 
      success: false, 
      error: 'Invalid or inactive college code' 
    });
  }

  if (!college.settings.allowSelfRegistration) {
    return res.status(403).json({ 
      success: false, 
      error: 'Self registration is disabled for this college' 
    });
  }

  // Create user
  user = await User.create({
    name,
    email: email.toLowerCase(),
    password,
    collegeId: college._id,
    department,
    phoneNumber
  });

  // Update college statistics
  college.statistics.totalStudents += 1;
  await college.save();

  // Send token response
  sendTokenResponse(user, 201, res, 'Registration successful');
}));

// @route   POST /api/auth/login
// @desc    Login user
// @access  Public
router.post('/login', loginValidation, validate, asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  // Find user with password
  const user = await User.findOne({ email: email.toLowerCase() })
    .select('+password')
    .populate('collegeId', 'name code');

  if (!user) {
    return res.status(401).json({ 
      success: false, 
      error: 'Invalid credentials' 
    });
  }

  // Check if password matches
  const isMatch = await user.comparePassword(password);
  if (!isMatch) {
    return res.status(401).json({ 
      success: false, 
      error: 'Invalid credentials' 
    });
  }

  if (!user.isActive) {
    return res.status(401).json({ 
      success: false, 
      error: 'Account has been deactivated. Contact admin.' 
    });
  }

  // Update last login
  user.lastLogin = Date.now();
  await user.save();

  sendTokenResponse(user, 200, res, 'Login successful');
}));

// @route   GET /api/auth/me
// @desc    Get current logged in user
// @access  Private
router.get('/me', isAuthenticated, asyncHandler(async (req, res) => {
  const user = await User.findById(req.user.id)
    .populate('collegeId', 'name code logo contact');

  res.json({
    success: true,
    data: user
  });
}));

// @route   PUT /api/auth/update-profile
// @desc    Update user profile
// @access  Private
router.put('/update-profile', isAuthenticated, asyncHandler(async (req, res) => {
  const fieldsToUpdate = {
    name: req.body.name,
    phoneNumber: req.body.phoneNumber,
    department: req.body.department
  };

  const user = await User.findByIdAndUpdate(req.user.id, fieldsToUpdate, {
    new: true,
    runValidators: true
  });

  res.json({
    success: true,
    data: user
  });
}));

// @route   PUT /api/auth/change-password
// @desc    Change password
// @access  Private
router.put('/change-password', isAuthenticated, asyncHandler(async (req, res) => {
  const { currentPassword, newPassword } = req.body;

  const user = await User.findById(req.user.id).select('+password');

  // Check current password
  const isMatch = await user.comparePassword(currentPassword);
  if (!isMatch) {
    return res.status(401).json({ 
      success: false, 
      error: 'Current password is incorrect' 
    });
  }

  user.password = newPassword;
  await user.save();

  res.json({
    success: true,
    message: 'Password updated successfully'
  });
}));

// @route   POST /api/auth/logout
// @desc    Logout user / clear cookie
// @access  Private
router.post('/logout', isAuthenticated, (req, res) => {
  res.cookie('token', 'none', {
    expires: new Date(Date.now() + 10 * 1000),
    httpOnly: true
  });

  res.json({
    success: true,
    message: 'Logged out successfully'
  });
});

// Helper function to get token from model, create cookie and send response
const sendTokenResponse = (user, statusCode, res, message) => {
  const token = user.getSignedJwtToken();

  const options = {
    expires: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production'
  };

  res
    .status(statusCode)
    .cookie('token', token, options)
    .json({
      success: true,
      message,
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        collegeId: user.collegeId
      }
    });
};

module.exports = router;