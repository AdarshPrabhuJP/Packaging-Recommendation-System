# Render Deployment Guide

## Issue Fixed ✅

The main issue was a **circular import** in `app.py`. This has been resolved by:

1. Creating a new `wsgi.py` file as the WSGI entry point
2. Updating `Procfile` to use `wsgi:app` instead of `app:app`

## Deployment Steps

### 1. Pre-deployment Checklist

- [x] Fixed circular import issue
- [x] Created `wsgi.py` entry point
- [x] Updated `Procfile`
- [ ] Set up PostgreSQL database on Render
- [ ] Configure environment variables

### 2. Database Setup on Render

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Choose a name (e.g., `packaging-db`)
   - Select region and plan
   - Note the connection details

2. **Get Database URL:**
   - After creation, copy the "External Database URL"
   - Format: `postgresql://user:password@host:port/database`

### 3. Web Service Setup

1. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Choose branch (usually `main`)

2. **Configure Build Settings:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: (leave empty - uses Procfile)
   ```

3. **Environment Variables:**
   Add these in Render dashboard:
   ```
   DATABASE_URL=<your-postgresql-url-from-step-2>
   SECRET_KEY=<generate-a-secure-random-key>
   PYTHON_VERSION=3.11.7
   ```

### 4. Database Initialization

After deployment, you need to initialize the database:

1. **Connect to your Render shell:**
   - Go to your web service dashboard
   - Click "Shell" tab
   - Run these commands:

   ```bash
   # Initialize database schema
   python database/init_db.py
   
   # Import data
   python database/import_data.py
   ```

### 5. Verify Deployment

Test these endpoints:
- `https://your-app.onrender.com/` - Main page
- `https://your-app.onrender.com/api/health` - Health check
- `https://your-app.onrender.com/api/materials` - Materials API

## Common Issues & Solutions

### Issue 1: "Failed to find attribute 'app' in 'app'"
**Solution:** ✅ Fixed by creating `wsgi.py`

### Issue 2: Database Connection Error
**Solution:** 
- Ensure `DATABASE_URL` environment variable is set
- Check database is running and accessible
- Verify connection string format

### Issue 3: Missing Models
**Solution:**
- Models are included in the repository
- If missing, retrain using: `python src/ml_models.py`

### Issue 4: Import Errors
**Solution:**
- All dependencies are in `requirements.txt`
- If issues persist, check Python version compatibility

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `PYTHON_VERSION` | Python runtime version | `3.11.7` |

## File Structure Changes

```
├── wsgi.py              # ✅ NEW: WSGI entry point
├── app.py               # ✅ UPDATED: Removed circular import
├── Procfile             # ✅ UPDATED: Uses wsgi:app
├── test_wsgi.py         # ✅ NEW: Test WSGI setup
└── RENDER_DEPLOY.md     # ✅ NEW: This guide
```

## Testing Locally

Before deploying, test the WSGI setup:

```bash
# Test WSGI import
python test_wsgi.py

# Test with Gunicorn (same as Render)
gunicorn wsgi:app --bind 0.0.0.0:5000
```

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Verify all environment variables are set
3. Ensure database is initialized
4. Test endpoints individually

The main circular import issue has been resolved. Your app should now deploy successfully on Render! 🚀