# Testing Guide - Online Voting System

## Pre-Testing Setup

### 1. Ensure Application is Running
```powershell
cd "d:\College Assignments\TYIT\Project-Code"
.\venv\Scripts\Activate.ps1
python app.py
```

Application should be running at: `http://localhost:5000`

### 2. Generate Test Data (Optional)
```powershell
python generate_test_data.py
```

This creates:
- 3 sample elections
- 12 sample candidates
- 10 test voters (V001-V010)
- Sample votes

## Testing Checklist

### 🏠 Home Page Testing

#### Test Case 1: View Home Page
**Steps:**
1. Navigate to `http://localhost:5000`
2. Verify page loads correctly
3. Check navigation bar
4. Check elections display
5. Check status badges

**Expected Results:**
- ✅ Page loads without errors
- ✅ Navigation shows all links
- ✅ Elections shown with status
- ✅ Feature cards visible
- ✅ Footer displayed

#### Test Case 2: Responsive Design
**Steps:**
1. Open Developer Tools (F12)
2. Toggle device toolbar
3. Test mobile view (375px)
4. Test tablet view (768px)
5. Test desktop view (1920px)

**Expected Results:**
- ✅ Layout adapts to screen size
- ✅ No horizontal scrolling
- ✅ Cards stack properly
- ✅ Navigation collapses on mobile

---

### 👤 Voter Registration & Login

#### Test Case 3: Voter Registration
**Steps:**
1. Click "Voter Register"
2. Fill in form:
   - Voter ID: TEST001
   - Name: Test User
   - Email: test@example.com
   - Password: testpass123
3. Submit form

**Expected Results:**
- ✅ Registration successful
- ✅ Success message shown
- ✅ Redirected to login page

#### Test Case 4: Duplicate Registration
**Steps:**
1. Try to register with same Voter ID
2. Try to register with same email

**Expected Results:**
- ✅ Error message shown
- ✅ Registration prevented
- ✅ User stays on registration page

#### Test Case 5: Voter Login
**Steps:**
1. Navigate to Voter Login
2. Enter credentials:
   - Voter ID: TEST001 (or V001)
   - Password: testpass123 (or password123)
3. Submit

**Expected Results:**
- ✅ Login successful
- ✅ Redirected to voter dashboard
- ✅ Welcome message with name

#### Test Case 6: Invalid Login
**Steps:**
1. Try login with wrong password
2. Try login with non-existent voter ID

**Expected Results:**
- ✅ Error message displayed
- ✅ Login prevented
- ✅ User stays on login page

---

### 🗳️ Voting Process

#### Test Case 7: View Active Elections
**Steps:**
1. Login as voter
2. View dashboard
3. Check active elections list

**Expected Results:**
- ✅ Active elections displayed
- ✅ Election details shown
- ✅ "Vote Now" button visible
- ✅ Already voted elections marked

#### Test Case 8: Cast Vote
**Steps:**
1. Click "Cast Your Vote" on an election
2. View all candidates
3. Select a candidate
4. Confirm vote
5. Submit

**Expected Results:**
- ✅ Candidates displayed correctly
- ✅ Radio button selection works
- ✅ Confirmation dialog appears
- ✅ Vote recorded successfully
- ✅ Success message shown
- ✅ Redirected to dashboard

#### Test Case 9: Prevent Duplicate Voting
**Steps:**
1. Vote in an election
2. Try to vote again in same election
3. Check vote button

**Expected Results:**
- ✅ Cannot vote again
- ✅ "Already Voted" badge shown
- ✅ Vote button disabled

#### Test Case 10: Candidate Selection
**Steps:**
1. On vote page, click on candidate card
2. Try clicking different candidates
3. Check radio button state

**Expected Results:**
- ✅ Card highlights when selected
- ✅ Radio button checks/unchecks
- ✅ Only one candidate selectable
- ✅ Visual feedback works

---

### 👨‍💼 Admin Testing

#### Test Case 11: Admin Login
**Steps:**
1. Navigate to `http://localhost:5000/admin/login`
2. Enter credentials:
   - Username: admin
   - Password: admin123
3. Submit

**Expected Results:**
- ✅ Login successful
- ✅ Redirected to admin dashboard
- ✅ Statistics visible

#### Test Case 12: Admin Dashboard
**Steps:**
1. Login as admin
2. View dashboard
3. Check statistics cards
4. View elections table

**Expected Results:**
- ✅ Total elections count correct
- ✅ Total candidates count correct
- ✅ Total voters count correct
- ✅ Total votes count correct
- ✅ Elections table displays all elections
- ✅ Action buttons work

#### Test Case 13: Create Election
**Steps:**
1. From dashboard, click "Create Election"
2. Fill form:
   - Title: Test Election
   - Description: Test Description
   - Start Date: Future date
   - End Date: Date after start
3. Submit

**Expected Results:**
- ✅ Election created successfully
- ✅ Success message shown
- ✅ Redirected to elections list
- ✅ New election appears in list
- ✅ Status is "upcoming"

#### Test Case 14: Edit Election
**Steps:**
1. Click "Edit" on an election
2. Modify title or dates
3. Submit changes

**Expected Results:**
- ✅ Form pre-filled with data
- ✅ Changes saved successfully
- ✅ Success message shown
- ✅ Updated data displayed

#### Test Case 15: Delete Election
**Steps:**
1. Click "Delete" on an election
2. Confirm deletion

**Expected Results:**
- ✅ Confirmation dialog appears
- ✅ Election deleted
- ✅ Success message shown
- ✅ Election removed from list
- ✅ Related candidates deleted (cascade)

#### Test Case 16: Add Candidate
**Steps:**
1. Click "Manage Candidates" for an election
2. Click "Add Candidate"
3. Fill form:
   - Name: Test Candidate
   - Party: Test Party
   - Description: Test Description
   - Photo URL: (optional)
4. Submit

**Expected Results:**
- ✅ Candidate created successfully
- ✅ Success message shown
- ✅ Candidate appears in grid
- ✅ Default icon if no photo

#### Test Case 17: Edit Candidate
**Steps:**
1. Click "Edit" on a candidate
2. Modify details
3. Submit

**Expected Results:**
- ✅ Form pre-filled
- ✅ Changes saved
- ✅ Updated data displayed

#### Test Case 18: Delete Candidate
**Steps:**
1. Click "Delete" on a candidate
2. Confirm deletion

**Expected Results:**
- ✅ Confirmation dialog
- ✅ Candidate deleted
- ✅ Success message
- ✅ Removed from grid

---

### 📊 Results & Charts

#### Test Case 19: View Results
**Steps:**
1. Login as admin
2. Click "View Results" for an election
3. Check charts and data

**Expected Results:**
- ✅ Bar chart displays correctly
- ✅ Pie chart displays correctly
- ✅ Vote counts accurate
- ✅ Percentages calculated correctly
- ✅ Detailed results table shown
- ✅ Total votes correct

#### Test Case 20: Real-time Updates
**Steps:**
1. Open results page in one browser
2. Open voter page in another browser
3. Cast a vote
4. Wait 10 seconds on results page

**Expected Results:**
- ✅ Charts update automatically
- ✅ Vote count increases
- ✅ Percentages recalculate
- ✅ No page refresh needed

#### Test Case 21: Chart Interactions
**Steps:**
1. On results page
2. Hover over chart elements
3. Check tooltips

**Expected Results:**
- ✅ Tooltips show on hover
- ✅ Vote counts displayed
- ✅ Percentages shown in pie chart
- ✅ Legend clickable

#### Test Case 22: Empty Results
**Steps:**
1. Create new election
2. Add candidates
3. View results (no votes)

**Expected Results:**
- ✅ Charts display with zero values
- ✅ "0 votes" shown
- ✅ No errors
- ✅ Percentages show 0%

---

### 🔒 Security Testing

#### Test Case 23: Authentication Required
**Steps:**
1. Try accessing `/admin/dashboard` without login
2. Try accessing `/voter/dashboard` without login

**Expected Results:**
- ✅ Redirected to login page
- ✅ Access denied message
- ✅ Cannot access protected routes

#### Test Case 24: Password Security
**Steps:**
1. Register a new user
2. Check database (password_hash column)

**Expected Results:**
- ✅ Password is hashed
- ✅ Not stored as plain text
- ✅ Hash starts with 'pbkdf2:sha256'

#### Test Case 25: SQL Injection Prevention
**Steps:**
1. Try login with: `' OR '1'='1`
2. Try in voter ID field
3. Try in search fields

**Expected Results:**
- ✅ Injection attempt fails
- ✅ No database error
- ✅ Invalid credentials message

#### Test Case 26: Session Management
**Steps:**
1. Login as admin
2. Close browser
3. Reopen browser
4. Try to access admin pages

**Expected Results:**
- ✅ Session persists (depending on config)
- ✅ Or requires re-login
- ✅ No unauthorized access

---

### 🌐 API Testing

#### Test Case 27: Results API
**Steps:**
1. Make GET request to `/api/elections/1/results`
2. Check response

**Expected Results:**
- ✅ JSON response received
- ✅ Contains candidate data
- ✅ Vote counts included
- ✅ Valid JSON format

**Test with curl:**
```powershell
curl http://localhost:5000/api/elections/1/results
```

---

### 🐛 Error Handling

#### Test Case 28: Invalid Routes
**Steps:**
1. Navigate to `/invalid-page`
2. Navigate to `/admin/elections/999`

**Expected Results:**
- ✅ 404 error or redirect
- ✅ User-friendly message
- ✅ No application crash

#### Test Case 29: Form Validation
**Steps:**
1. Submit empty forms
2. Submit invalid dates (end before start)
3. Submit invalid email format

**Expected Results:**
- ✅ Validation errors shown
- ✅ Form not submitted
- ✅ User can correct errors

#### Test Case 30: Database Connection Error
**Steps:**
1. Stop MySQL service
2. Try to access application

**Expected Results:**
- ✅ Error message displayed
- ✅ Application doesn't crash
- ✅ Helpful error information

---

## Performance Testing

### Test Case 31: Page Load Time
**Steps:**
1. Open Developer Tools
2. Navigate to Network tab
3. Load various pages
4. Check load times

**Expected Results:**
- ✅ Pages load under 2 seconds
- ✅ No unnecessary requests
- ✅ Assets cached properly

### Test Case 32: Database Queries
**Steps:**
1. Enable SQLAlchemy echo
2. Perform various actions
3. Check console for queries

**Expected Results:**
- ✅ Efficient queries (no N+1 problem)
- ✅ Proper use of relationships
- ✅ Indexed columns used

---

## Browser Compatibility

### Test Case 33: Cross-Browser Testing
**Browsers to Test:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if available)

**Expected Results:**
- ✅ Works in all browsers
- ✅ Layout consistent
- ✅ No JavaScript errors

---

## Test Data

### Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Test Voters (if generated):**
- Voter ID: `V001` to `V010`
- Password: `password123`

**Custom Test User:**
- Voter ID: `TEST001`
- Password: `testpass123`

---

## Testing Workflow

### Quick Test (5 minutes)
1. ✅ Home page loads
2. ✅ Admin login works
3. ✅ Create election
4. ✅ Add candidates
5. ✅ Voter login
6. ✅ Cast vote
7. ✅ View results

### Full Test (30 minutes)
Run all 33 test cases above

### Regression Test
After any code change, run:
1. Authentication tests
2. Voting tests
3. Results tests

---

## Bug Reporting Template

If you find a bug:

```
**Bug Title:** 
Brief description

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happened

**Environment:**
- Browser: 
- OS: 
- Python version:
- MySQL version:

**Screenshots:**
(if applicable)
```

---

## Test Results Template

```
Test Date: __________
Tester: __________

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Home Page | ✅ | |
| 2 | Responsive | ✅ | |
| ... | ... | ... | ... |

Overall Status: ✅ Pass / ❌ Fail
```

---

## Automated Testing (Future)

For future enhancement, consider:
- Unit tests with pytest
- Integration tests
- Selenium for browser automation
- Load testing with Locust

---

**Happy Testing! 🧪**

Make sure to test thoroughly before your demonstration!
