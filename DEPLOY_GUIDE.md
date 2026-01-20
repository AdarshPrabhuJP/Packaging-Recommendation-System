# Quick Deploy Guide

## Option 1: Railway (Recommended)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Get public URL: `https://your-app.railway.app`

## Option 2: Heroku
1. Go to https://heroku.com
2. Create new app
3. Connect GitHub repository
4. Enable automatic deploys
5. Get URL: `https://your-app.herokuapp.com`

## Option 3: PythonAnywhere
1. Go to https://pythonanywhere.com
2. Upload your code
3. Configure web app
4. Get URL: `https://yourusername.pythonanywhere.com`

## Files Ready:
- ✅ server.py (simple Flask server)
- ✅ Procfile (updated for Railway/Heroku)
- ✅ requirements.txt
- ✅ All deployment configs

## Environment Variables Needed:
- DATABASE_URL (PostgreSQL connection)
- SECRET_KEY (Flask secret)

Your app will be publicly accessible at the provided URL!