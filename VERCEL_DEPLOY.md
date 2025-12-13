# Vercel Deployment - Step by Step Guide

## ✅ Setup Complete!

I've configured your Flask app for Vercel. Here's what was created:

### 📁 Files Created:
- ✅ `api/index.py` - Vercel serverless entry point
- ✅ `vercel.json` - Vercel configuration
- ✅ `.vercelignore` - Files to exclude from deployment

---

## 🚀 Deploy to Vercel (2 Methods)

### **Method 1: Deploy via Web Dashboard (Easiest)**

1. **Go to:** https://vercel.com/signup
2. **Sign up** with GitHub/GitLab/Bitbucket
3. **Click "Add New Project"**
4. **Import your repository:**
   - If not on GitHub yet, push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin YOUR_GITHUB_URL
     git push -u origin main
     ```
5. **Connect repository** on Vercel
6. **Configure:**
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
7. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add:
     ```
     SECRET_KEY = your-super-secret-key-here
     DATABASE_URL = your-database-url (if using external DB)
     ```
8. **Click "Deploy"**

**Your app will be live in 2-3 minutes!** 🎉

---

### **Method 2: Deploy via CLI**

#### **Step 1: Install Vercel CLI**

**Option A - Using npm (if you have Node.js):**
```bash
npm install -g vercel
```

**Option B - Download installer:**
1. Go to: https://vercel.com/download
2. Download for Windows
3. Install and restart terminal

**Option C - Using Scoop (Windows package manager):**
```bash
scoop install vercel-cli
```

#### **Step 2: Login to Vercel**
```bash
vercel login
```
- Opens browser to authenticate
- Choose your account

#### **Step 3: Deploy**

Navigate to your project folder:
```bash
cd "D:\College Assignments\TYIT\Project-Code"
```

Deploy:
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? (Choose your account)
- Link to existing project? **N**
- What's your project's name? `voting-system` (or your choice)
- In which directory is your code located? `./`
- Want to override settings? **N**

**Deployment will start!**

#### **Step 4: Set Environment Variables**
```bash
vercel env add SECRET_KEY
```
Enter your secret key when prompted.

#### **Step 5: Deploy to Production**
```bash
vercel --prod
```

---

## ⚠️ Important Notes for Vercel

### **Database Considerations:**

Your current config uses SQLite, which **won't work** on Vercel (serverless environment).

**You need to use an external database:**

#### **Option 1: PlanetScale (Free MySQL)**
1. Go to: https://planetscale.com
2. Create free account
3. Create database
4. Get connection string
5. Add to Vercel:
   ```bash
   vercel env add DATABASE_URL
   # Paste: mysql+pymysql://user:pass@host/db?ssl_ca=/etc/ssl/cert.pem
   ```

#### **Option 2: Supabase (Free PostgreSQL)**
1. Go to: https://supabase.com
2. Create project
3. Get connection string
4. Update requirements.txt:
   ```txt
   psycopg2-binary==2.9.9
   ```
5. Update config.py:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
   ```

#### **Option 3: MongoDB Atlas (Free NoSQL)**
1. Go to: https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Switch to Flask-PyMongo

---

## 🔧 Update Your Config for Production

Update `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-this'
    
    # For Vercel with external database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Use external database (production)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Use SQLite (local development only)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///voting_system.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
```

---

## 📝 After Deployment Checklist

### **1. Test Your Deployment**
Visit your Vercel URL: `https://your-app.vercel.app`

### **2. Initialize Database**
Run this once after first deployment:

```python
# Create a script: init_db.py
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created!")
```

Then run locally pointing to production DB:
```bash
python init_db.py
```

### **3. Set Up Custom Domain (Optional)**
In Vercel dashboard:
1. Go to your project
2. Settings → Domains
3. Add your domain
4. Update DNS records as shown

---

## 🚨 Common Issues & Solutions

### **Issue 1: "Module not found"**
**Solution:** Make sure all dependencies are in `requirements.txt`

### **Issue 2: "Database connection failed"**
**Solution:** 
- Verify DATABASE_URL is set in Vercel
- Use external database (SQLite doesn't work on Vercel)

### **Issue 3: "Static files not loading"**
**Solution:** 
- Static files are in `/static` folder
- Vercel serves them automatically
- Clear browser cache

### **Issue 4: "Session not persisting"**
**Solution:** 
- Vercel is stateless
- Use external session storage (Redis, DynamoDB)
- Or switch to JWT tokens

---

## 📊 Deployment Status

Once deployed, check:

✅ **Deployment URL:** Shown in terminal or dashboard
✅ **Build Logs:** Check for errors
✅ **Function Logs:** See runtime errors
✅ **Environment Variables:** Verify they're set

---

## 🎯 Quick Commands Reference

```bash
# Deploy
vercel

# Deploy to production
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs

# Open in browser
vercel open

# Remove deployment
vercel rm
```

---

## 💡 Pro Tips

1. **Use Environment Variables** for all secrets
2. **Test locally first** with production DB
3. **Check logs** if something breaks
4. **Use Vercel Analytics** to monitor usage
5. **Set up GitHub integration** for auto-deploys

---

## 🆘 Still Having Issues?

If deployment fails:

1. **Check build logs** in Vercel dashboard
2. **Verify all environment variables** are set
3. **Test database connection** separately
4. **Check Python version** (Vercel supports 3.9-3.12)
5. **Review Vercel Python documentation:** https://vercel.com/docs/functions/serverless-functions/runtimes/python

---

## 🎉 Success Checklist

After successful deployment:

- [ ] App loads at Vercel URL
- [ ] Database connection works
- [ ] Static files (images, CSS) load
- [ ] Login/authentication works
- [ ] Voting functionality works
- [ ] Admin panel accessible
- [ ] No errors in function logs

---

## 🌐 Your Deployed URLs

After deployment, you'll get:

- **Preview:** `https://your-app-git-branch.vercel.app`
- **Production:** `https://your-app.vercel.app`
- **Custom:** `https://your-domain.com` (if configured)

---

**Need help?** Check Vercel's Python documentation or ask for assistance! 🚀
