# How to Change Admin Password

There are **3 ways** to change the admin password:

---

## Method 1: Through Web Interface (Easiest) ⭐

1. **Login as admin:**
   - Go to: `http://localhost:5000/admin/login`
   - Enter your username and password

2. **Go to Profile:**
   - Click the "Profile" button (top-right of dashboard)
   - Or go directly to: `http://localhost:5000/admin/profile`

3. **Change Password:**
   - Enter your current password
   - Enter your new password (min 6 characters)
   - Confirm your new password
   - Click "Change Password"

4. **Done!** ✅
   - You'll see a success message
   - Your password is now updated

---

## Method 2: Using Password Reset Script (For Locked Accounts)

If you've forgotten your password or can't login:

1. **Open terminal/PowerShell** in your project directory

2. **Run the script:**
   ```powershell
   python admin_password_reset.py
   ```
   Or with virtual environment:
   ```powershell
   & "D:/College Assignments/TYIT/Project-Code/venv/Scripts/python.exe" admin_password_reset.py
   ```

3. **Choose option 1** (Change admin password)

4. **Follow the prompts:**
   - Enter admin username (default: `admin`)
   - Enter new password
   - Confirm new password

5. **Done!** ✅

---

## Method 3: Using MySQL/Database Directly (Advanced)

1. **Generate password hash** (Python):
   ```python
   from werkzeug.security import generate_password_hash
   new_hash = generate_password_hash('your_new_password')
   print(new_hash)
   ```

2. **Update database:**
   ```sql
   USE voting_system;
   UPDATE admins 
   SET password_hash = 'your_generated_hash_here' 
   WHERE username = 'admin';
   ```

---

## Quick Reference

### Default Admin Credentials
- **Username:** `admin`
- **Password:** `admin123`

### Other Admin Accounts
- **Username:** `root`
- **Password:** `root`

### Password Requirements
- ✅ Minimum 6 characters
- ✅ No special requirements (but recommended to use strong passwords)

### Security Tips
- 🔒 Use a strong password with letters, numbers, and symbols
- 🔒 Change the default password immediately after setup
- 🔒 Don't share your admin credentials
- 🔒 Use different passwords for different accounts

---

## Troubleshooting

### "Current password is incorrect"
- Make sure you're entering the correct current password
- Try using the password reset script (Method 2)

### "Admin user not found"
- Use the password reset script option 2 to list all admin users
- Check the username spelling

### Can't access the web interface
- Make sure the Flask app is running: `python app.py`
- Check if you can access: `http://localhost:5000`
- Use Method 2 (password reset script) instead

### Forgot username
Run the password reset script and choose option 2 to list all admin users:
```powershell
python admin_password_reset.py
# Choose option 2
```

---

## Need More Help?

Check these files:
- `README.md` - Main documentation
- `QUICK_START.md` - Getting started guide
- `TESTING_GUIDE.md` - Testing instructions

Or run the admin management utility for more options:
```powershell
python admin_password_reset.py
```
