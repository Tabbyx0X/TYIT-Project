const mongoose = require('mongoose');

const collegeSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Please provide college name'],
    trim: true,
    unique: true
  },
  code: {
    type: String,
    required: [true, 'Please provide college code'],
    unique: true,
    uppercase: true,
    trim: true,
    match: [/^[A-Z0-9]{4,10}$/, 'College code must be 4-10 alphanumeric characters']
  },
  adminId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  address: {
    street: String,
    city: String,
    state: String,
    pincode: String,
    country: { type: String, default: 'India' }
  },
  contact: {
    email: {
      type: String,
      match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please provide a valid email']
    },
    phone: String,
    website: String
  },
  departments: [{
    name: String,
    code: String,
    head: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
  }],
  logo: {
    type: String,
    default: '/images/default-college-logo.png'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  settings: {
    allowSelfRegistration: { type: Boolean, default: true },
    requireEmailVerification: { type: Boolean, default: false },
    maxStudents: { type: Number, default: 10000 },
    academicYear: String
  },
  statistics: {
    totalStudents: { type: Number, default: 0 },
    totalTeachers: { type: Number, default: 0 },
    totalDepartments: { type: Number, default: 0 }
  }
}, {
  timestamps: true
});

// Update statistics before saving
collegeSchema.pre('save', function(next) {
  this.statistics.totalDepartments = this.departments.length;
  next();
});

module.exports = mongoose.model('College', collegeSchema);
