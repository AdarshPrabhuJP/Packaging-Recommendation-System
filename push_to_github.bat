@echo off
echo Pushing Render deployment fixes to GitHub...

REM Add the remote repository if not already added
git remote add origin https://github.com/AdarshPrabhuJP/Packaging-AI-Recommendation-System.git

REM Add all the new and modified files
git add wsgi.py
git add Procfile
git add test_wsgi.py
git add RENDER_DEPLOY.md
git add .env.example
git add app.py

REM Commit the changes
git commit -m "Fix Render deployment: resolve circular import issue

- Add wsgi.py as WSGI entry point
- Update Procfile to use wsgi:app
- Add deployment guide and test script
- Update .env.example with Render notes"

REM Push to GitHub
git push -u origin main

echo.
echo ✅ Files pushed to GitHub!
echo.
echo Next steps:
echo 1. Go to Render dashboard
echo 2. Redeploy your service
echo 3. The circular import issue should be resolved
echo.
pause