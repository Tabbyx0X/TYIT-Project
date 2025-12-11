# 🧪 Testing Guide - Updated Features

## Prerequisites
Ensure the application is running:
```powershell
python app.py
```

---

## 1. Security Features Testing

### Test 1.1: Session Timeout
**Objective**: Verify session expires after 1 hour

**Steps**:
1. Login as admin or voter
2. Wait for 1 hour (or modify `PERMANENT_SESSION_LIFETIME` in config.py to 60 seconds for testing)
3. Try to access a protected page
4. **Expected**: Redirected to login with message "Please log in to access this page."

**Status**: ⬜ Pass ⬜ Fail

---

### Test 1.2: Security Headers
**Objective**: Verify security headers are present

**Steps**:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Access any page (e.g., http://localhost:5000)
4. Click on the request and check Response Headers
5. **Expected Headers**:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: SAMEORIGIN`
   - `X-XSS-Protection: 1; mode=block`

**Status**: ⬜ Pass ⬜ Fail

---

## 2. Input Validation Testing

### Test 2.1: Voter ID Validation
**Objective**: Ensure invalid Voter IDs are rejected

**Test Cases**:
| Input | Expected Result | Status |
|-------|-----------------|--------|
| `ABC` (too short) | Error: "Invalid Voter ID format" | ⬜ Pass ⬜ Fail |
| `ABCDEFGHIJ1234567890X` (too long) | Error: "Invalid Voter ID format" | ⬜ Pass ⬜ Fail |
| `ABC@123` (special chars) | Error: "Invalid Voter ID format" | ⬜ Pass ⬜ Fail |
| `VOTER12345` (valid) | Success | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/voter/register

---

### Test 2.2: Email Validation
**Objective**: Ensure invalid emails are rejected

**Test Cases**:
| Input | Expected Result | Status |
|-------|-----------------|--------|
| `notanemail` | Error: "Invalid email format" | ⬜ Pass ⬜ Fail |
| `test@` | Error: "Invalid email format" | ⬜ Pass ⬜ Fail |
| `@example.com` | Error: "Invalid email format" | ⬜ Pass ⬜ Fail |
| `test@example.com` (valid) | Success | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/voter/register

---

### Test 2.3: Password Validation
**Objective**: Ensure weak passwords are rejected

**Test Cases**:
| Input | Expected Result | Status |
|-------|-----------------|--------|
| `12345` (too short) | Error: "Password must be at least 6 characters" | ⬜ Pass ⬜ Fail |
| `abc` (too short) | Error: "Password must be at least 6 characters" | ⬜ Pass ⬜ Fail |
| `password123` (valid) | Success | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/voter/register

---

### Test 2.4: Password Confirmation
**Objective**: Ensure passwords must match

**Steps**:
1. Go to voter registration
2. Enter valid voter ID, name, email
3. Enter password: `password123`
4. Enter confirm password: `password456` (different)
5. Submit form
6. **Expected**: Error "Passwords do not match"

**Status**: ⬜ Pass ⬜ Fail

---

## 3. Service Layer Testing

### Test 3.1: Admin Authentication Service
**Objective**: Test authenticate_admin() function

**Test Cases**:
| Username | Password | Expected Result | Status |
|----------|----------|-----------------|--------|
| `admin` | `admin123` | Success | ⬜ Pass ⬜ Fail |
| `root` | `root` | Success | ⬜ Pass ⬜ Fail |
| `admin` | `wrong` | Error: "Invalid username or password" | ⬜ Pass ⬜ Fail |
| `nonexistent` | `any` | Error: "Invalid username or password" | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/admin/login

---

### Test 3.2: Get Active Elections Service
**Objective**: Test get_active_elections() function

**Steps**:
1. Login as admin
2. Create an election with start_date in past and end_date in future
3. Create another election with both dates in future
4. Login as voter
5. Check voter dashboard
6. **Expected**: Only the active election is shown

**Status**: ⬜ Pass ⬜ Fail

---

### Test 3.3: Vote Recording Service
**Objective**: Test record_vote() with validation

**Test Cases**:

**Case A: Valid Vote**
1. Login as voter
2. Go to active election
3. Select a candidate
4. Submit vote
5. **Expected**: Success message "Vote recorded successfully"

**Status**: ⬜ Pass ⬜ Fail

**Case B: Invalid Candidate**
1. Use browser DevTools to modify candidate_id to invalid value
2. Submit vote
3. **Expected**: Error "Invalid candidate selection"

**Status**: ⬜ Pass ⬜ Fail

**Case C: Duplicate Vote**
1. Vote in an election
2. Try to vote again in the same election
3. **Expected**: Warning "You have already voted in this election"

**Status**: ⬜ Pass ⬜ Fail

---

## 4. Error Handler Testing

### Test 4.1: 404 Error Handler
**Objective**: Test not found pages

**Steps**:
1. Access non-existent URL: http://localhost:5000/nonexistent
2. **Expected**: 
   - Flash message: "The requested page was not found"
   - Redirected to home page

**Status**: ⬜ Pass ⬜ Fail

---

### Test 4.2: 500 Error Handler
**Objective**: Test server error handling

**Steps** (requires code modification for testing):
1. Temporarily add a line that causes an error (e.g., `1/0`)
2. Access the route
3. **Expected**:
   - Flash message: "An internal error occurred"
   - Database rolled back
   - Redirected to home page

**Status**: ⬜ Pass ⬜ Fail

---

## 5. Election Management Testing

### Test 5.1: Create Election with Invalid Dates
**Objective**: Test date range validation

**Test Cases**:
| Start Date | End Date | Expected Result | Status |
|------------|----------|-----------------|--------|
| 2024-01-01 10:00 | 2024-01-01 09:00 | Error: "End date must be after start date" | ⬜ Pass ⬜ Fail |
| 2024-01-01 10:00 | 2024-01-01 10:00 | Error: "End date must be after start date" | ⬜ Pass ⬜ Fail |
| 2024-01-01 10:00 | 2024-01-02 10:00 | Success | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/admin/elections/add

---

### Test 5.2: Create Election with Empty Fields
**Objective**: Test required field validation

**Steps**:
1. Login as admin
2. Go to Add Election
3. Leave title empty
4. Fill other fields
5. Submit
6. **Expected**: Error "Election title is required"

**Status**: ⬜ Pass ⬜ Fail

---

## 6. Candidate Management Testing

### Test 6.1: Add Candidate with Empty Required Fields
**Objective**: Test required field validation

**Test Cases**:
| Name | Party | Expected Result | Status |
|------|-------|-----------------|--------|
| Empty | "Party A" | Error: "Candidate name is required" | ⬜ Pass ⬜ Fail |
| "John Doe" | Empty | Error: "Party name is required" | ⬜ Pass ⬜ Fail |
| "John Doe" | "Party A" | Success | ⬜ Pass ⬜ Fail |

**URL**: http://localhost:5000/admin/elections/1/candidates/add

---

## 7. Voter Registration Testing

### Test 7.1: Complete Registration Flow
**Objective**: Test full registration with all validations

**Steps**:
1. Go to voter registration
2. Fill all fields with valid data:
   - Voter ID: `VOTER12345`
   - Name: `Test Voter`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
3. Submit
4. **Expected**: Success message and redirect to login

**Status**: ⬜ Pass ⬜ Fail

---

### Test 7.2: Duplicate Voter ID
**Objective**: Test duplicate prevention

**Steps**:
1. Register a voter with ID `VOTER11111`
2. Try to register another voter with same ID
3. **Expected**: Error "Voter ID already exists!"

**Status**: ⬜ Pass ⬜ Fail

---

### Test 7.3: Duplicate Email
**Objective**: Test duplicate email prevention

**Steps**:
1. Register a voter with email `test@example.com`
2. Try to register another voter with same email
3. **Expected**: Error "Email already registered!"

**Status**: ⬜ Pass ⬜ Fail

---

## 8. Voting Flow Testing

### Test 8.1: Complete Voting Flow
**Objective**: Test end-to-end voting process

**Steps**:
1. Login as voter
2. View active elections on dashboard
3. Click "Vote" on an active election
4. View candidate list
5. Select a candidate
6. Confirm vote
7. **Expected**: 
   - Success message "Your vote has been recorded successfully!"
   - Returned to dashboard
   - Election shows "Already Voted" status

**Status**: ⬜ Pass ⬜ Fail

---

### Test 8.2: Vote in Inactive Election
**Objective**: Test voting prevention in inactive elections

**Steps**:
1. Login as admin
2. Create election with start_date in future
3. Login as voter
4. Try to access vote URL directly: `/voter/vote/<election_id>`
5. **Expected**: Warning "This election is not currently active!"

**Status**: ⬜ Pass ⬜ Fail

---

### Test 8.3: Unauthorized Voting Access
**Objective**: Test authentication requirement

**Steps**:
1. Logout from voter account (if logged in)
2. Try to access: http://localhost:5000/voter/dashboard
3. **Expected**: 
   - Warning "Please login first!"
   - Redirected to voter login

**Status**: ⬜ Pass ⬜ Fail

---

## 9. Results API Testing

### Test 9.1: API Response Format
**Objective**: Test enhanced API response

**Steps**:
1. Create an election with candidates
2. Cast some votes
3. Access API: http://localhost:5000/api/elections/1/results
4. **Expected JSON**:
```json
{
  "election_id": 1,
  "election_title": "Election Name",
  "results": [
    {"id": 1, "name": "Candidate", "party": "Party", "votes": 5}
  ],
  "total_votes": 5
}
```

**Status**: ⬜ Pass ⬜ Fail

---

### Test 9.2: API Error Handling
**Objective**: Test invalid election ID

**Steps**:
1. Access API with invalid ID: http://localhost:5000/api/elections/99999/results
2. **Expected**: 
   - Status Code: 404
   - JSON: `{"error": "Election not found"}`

**Status**: ⬜ Pass ⬜ Fail

---

## 10. Admin Dashboard Testing

### Test 10.1: Statistics Display
**Objective**: Test statistics using service layer

**Steps**:
1. Login as admin
2. Go to dashboard
3. **Expected**: Display shows:
   - Total Elections
   - Total Candidates
   - Total Voters
   - Total Votes
4. Verify numbers match database counts

**Status**: ⬜ Pass ⬜ Fail

---

## Test Summary

### Total Tests: 30+

**Security Tests**: ⬜⬜⬜⬜⬜⬜
**Validation Tests**: ⬜⬜⬜⬜⬜⬜⬜⬜
**Service Layer Tests**: ⬜⬜⬜⬜⬜
**Error Handler Tests**: ⬜⬜⬜
**Election Tests**: ⬜⬜⬜
**Candidate Tests**: ⬜⬜
**Voter Registration Tests**: ⬜⬜⬜⬜
**Voting Tests**: ⬜⬜⬜⬜
**API Tests**: ⬜⬜⬜
**Dashboard Tests**: ⬜⬜

---

## Quick Test Commands

### Test with Python Shell
```python
from app import app, db
from app import authenticate_admin, authenticate_voter
from app import validate_email, validate_voter_id, validate_password

with app.app_context():
    # Test admin auth
    admin, error = authenticate_admin('admin', 'admin123')
    print(f"Admin auth: {admin is not None}, Error: {error}")
    
    # Test validations
    print(f"Email valid: {validate_email('test@example.com')}")
    print(f"Email invalid: {validate_email('notanemail')}")
    print(f"Voter ID valid: {validate_voter_id('VOTER12345')}")
    print(f"Voter ID invalid: {validate_voter_id('ABC')}")
    print(f"Password valid: {validate_password('password123')}")
    print(f"Password invalid: {validate_password('pass')}")
```

### Test API with curl
```bash
# Test results API
curl http://localhost:5000/api/elections/1/results

# Test with invalid ID
curl http://localhost:5000/api/elections/99999/results
```

---

## Notes

- ✅ Mark test as **Pass** if it behaves as expected
- ⚠️ Mark test as **Fail** if it doesn't behave as expected
- 📝 Add notes for any unexpected behavior
- 🔄 Re-test after fixes

---

## Continuous Testing

For ongoing development:
1. Run these tests after any code changes
2. Add new tests for new features
3. Document any test failures
4. Update expected results if requirements change

---

## Automated Testing (Future)

Consider implementing:
- Unit tests with pytest
- Integration tests
- Load testing
- Security scanning
- Code coverage reports
