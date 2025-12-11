const express = require('express');
const router = express.Router();
const College = require('../models/College');
const User = require('../models/User');
const { asyncHandler } = require('../middleware/errorHandler');
const { isAuthenticated, authorize, filterByCollege } = require('../middleware/auth');
const { collegeValidation, validate } = require('../middleware/validation');

// @route   POST /api/college/create
// @desc    Create new college
// @access  Private/Admin
router.post('/create', isAuthenticated, authorize('admin'), 
  collegeValidation, validate, asyncHandler(async (req, res) => {
  
  const { name, code, address, contact, departments } = req.body;

  const existingCollege = await College.findOne({ 
    $or: [{ code: code.toUpperCase() }, { name }] 
  });
  
  if (existingCollege) {
    return res.status(400).json({ 
      success: false, 
      error: 'College with this name or code already exists' 
    });
  }

  const college = await College.create({
    name,
    code: code.toUpperCase(),
    address,
    contact,
    departments: departments || [],
    adminId: req.user._id
  });

  res.status(201).json({ 
    success: true, 
    message: 'College created successfully', 
    data: college 
  });
}));

// @route   POST /api/college/verify-code
// @desc    Verify college code
// @access  Public
router.post('/verify-code', asyncHandler(async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ 
      success: false, 
      error: 'College code is required' 
    });
  }

  const college = await College.findOne({ 
    code: code.toUpperCase(), 
    isActive: true 
  }).select('name code logo settings');

  if (!college) {
    return res.status(404).json({ 
      success: false, 
      error: 'Invalid or inactive college code' 
    });
  }

  res.json({ 
    success: true, 
    data: {
      valid: true,
      collegeName: college.name,
      logo: college.logo,
      allowRegistration: college.settings.allowSelfRegistration
    }
  });
}));

// @route   GET /api/college/list
// @desc    Get all colleges
// @access  Private/Admin
router.get('/list', isAuthenticated, authorize('admin'), 
  asyncHandler(async (req, res) => {
  
  const { page = 1, limit = 10, search, isActive } = req.query;
  
  const query = {};
  if (search) {
    query.$or = [
      { name: { $regex: search, $options: 'i' } },
      { code: { $regex: search, $options: 'i' } }
    ];
  }
  if (isActive !== undefined) {
    query.isActive = isActive === 'true';
  }

  const colleges = await College.find(query)
    .populate('adminId', 'name email')
    .limit(limit * 1)
    .skip((page - 1) * limit)
    .sort({ createdAt: -1 });

  const count = await College.countDocuments(query);

  res.json({
    success: true,
    data: colleges,
    pagination: {
      total: count,
      page: parseInt(page),
      pages: Math.ceil(count / limit)
    }
  });
}));

// @route   GET /api/college/:id
// @desc    Get single college details
// @access  Private
router.get('/:id', isAuthenticated, asyncHandler(async (req, res) => {
  const college = await College.findById(req.params.id)
    .populate('adminId', 'name email')
    .populate('departments.head', 'name email');

  if (!college) {
    return res.status(404).json({ 
      success: false, 
      error: 'College not found' 
    });
  }

  res.json({ 
    success: true, 
    data: college 
  });
}));

// @route   PUT /api/college/:id
// @desc    Update college
// @access  Private/Admin
router.put('/:id', isAuthenticated, authorize('admin'), 
  asyncHandler(async (req, res) => {
  
  const college = await College.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }
  );

  if (!college) {
    return res.status(404).json({ 
      success: false, 
      error: 'College not found' 
    });
  }

  res.json({ 
    success: true, 
    message: 'College updated successfully',
    data: college 
  });
}));

// @route   GET /api/college/:id/dashboard
// @desc    Get college dashboard statistics
// @access  Private/Admin
router.get('/:id/dashboard', isAuthenticated, authorize('admin', 'teacher'), 
  asyncHandler(async (req, res) => {
  
  const collegeId = req.params.id;

  const [
    totalStudents,
    totalTeachers,
    activeStudents,
    departmentStats
  ] = await Promise.all([
    User.countDocuments({ collegeId, role: 'student' }),
    User.countDocuments({ collegeId, role: 'teacher' }),
    User.countDocuments({ collegeId, role: 'student', isActive: true }),
    User.aggregate([
      { $match: { collegeId: require('mongoose').Types.ObjectId(collegeId) } },
      { $group: { 
          _id: '$department', 
          count: { $sum: 1 } 
        } 
      }
    ])
  ]);

  const college = await College.findById(collegeId);

  res.json({
    success: true,
    data: {
      college: {
        name: college.name,
        code: college.code
      },
      statistics: {
        totalStudents,
        totalTeachers,
        activeStudents,
        totalUsers: totalStudents + totalTeachers
      },
      departmentStats,
      recentActivity: [] // Can be extended later
    }
  });
}));

// @route   DELETE /api/college/:id
// @desc    Delete/Deactivate college
// @access  Private/Admin
router.delete('/:id', isAuthenticated, authorize('admin'), 
  asyncHandler(async (req, res) => {
  
  const college = await College.findById(req.params.id);

  if (!college) {
    return res.status(404).json({ 
      success: false, 
      error: 'College not found' 
    });
  }

  // Soft delete - just deactivate
  college.isActive = false;
  await college.save();

  // Deactivate all users from this college
  await User.updateMany(
    { collegeId: req.params.id },
    { isActive: false }
  );

  res.json({ 
    success: true, 
    message: 'College deactivated successfully' 
  });
}));

module.exports = router;
