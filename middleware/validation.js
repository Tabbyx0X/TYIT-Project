const { body, validationResult } = require('express-validator');

exports.validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ 
      success: false, 
      errors: errors.array().map(err => ({ field: err.param, message: err.msg }))
    });
  }
  next();
};

exports.registerValidation = [
  body('name').trim().notEmpty().withMessage('Name is required')
    .isLength({ min: 2, max: 50 }).withMessage('Name must be between 2-50 characters'),
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('collegeCode').trim().notEmpty().withMessage('College code is required')
    .matches(/^[A-Z0-9]{4,10}$/).withMessage('Invalid college code format')
];

exports.loginValidation = [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').notEmpty().withMessage('Password is required')
];

exports.collegeValidation = [
  body('name').trim().notEmpty().withMessage('College name is required'),
  body('code').trim().notEmpty().withMessage('College code is required')
    .matches(/^[A-Z0-9]{4,10}$/).withMessage('College code must be 4-10 alphanumeric characters')
];
