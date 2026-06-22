# How to Deploy to Render (Free 24/7 Hosting & Permanent HTTPS Link)

Follow these simple steps to host your translator app on Render for free:

## Step 1: Push your code to GitHub

1. Create a free account on [GitHub](https://github.com/) (if you don't have one).
2. Create a new **Public** or **Private** repository on GitHub named `multilanguage-translator`.
3. Open your project folder in VS Code, open a terminal, and run:
   ```bash
   git add .
   git commit -m "Prepare for web deployment"
   git branch -M main
   git remote add origin <YOUR_GITHUB_REPO_URL>
   git push -u origin main
   ```
   *(Replace `<YOUR_GITHUB_REPO_URL>` with your GitHub repository URL, e.g., `https://github.com/username/multilanguage-translator.git`)*

---

## Step 2: Deploy to Render

1. Create a free account on [Render](https://render.com/).
2. On your Render dashboard, click the **New +** button and select **Web Service**.
3. Select **Connect a repository** and choose the `multilanguage-translator` repository you just pushed to GitHub.
4. Configure the settings:
   - **Name:** `voice-translator` (or any name you like)
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Scroll down and click **Create Web Service**.

Render will build and deploy your app. Once finished, you will receive a permanent HTTPS link (e.g., `https://voice-translator.onrender.com`) that you can access anywhere, anytime!
