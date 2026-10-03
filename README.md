# 🎓 Canvas Announcements Notifier

Get instant push notifications on your phone whenever a professor posts a new announcement on Canvas. 

This project uses Python, GitHub Actions, and [cron-job.org](https://cron-job.org/) to reliably check your courses and send alerts via [ntfy.sh](https://ntfy.sh/).

## 🚀 How to set up your own notifier (No coding required)

### Step 1: Create your private repository
Since you will be handling your personal Canvas URLs, you need your own private copy of this code.
1. Click the green **"Use this template"** button at the top right of this page and select **"Create a new repository"**.
2. Name your repository (e.g., `my-canvas-bot`).
3. **CRITICAL:** Select **Private** so your Canvas data remains hidden from the public.
4. Click **Create repository**.

### Step 2: Set up the Ntfy app
1. Download the free **ntfy** app on your phone (iOS or Android).
2. Open the app and click the **+** button to subscribe to a new topic.
3. Invent a unique, hard-to-guess topic name (e.g., `canvas_cs_john_9827`). 

*Note: Treat this topic name like a password. Anyone who knows it can send notifications to your phone, so choose a hard name to guess.*

### Step 3: Add your Canvas courses to GitHub
First, go to your Canvas dashboard, enter a course, click on **Announcements**, and click the **External Feed (RSS)** link to copy the URL. Repeat this for all the courses you want to track.

Now, go to your new private GitHub repository:
1. Go to **Settings > Secrets and variables > Actions**.
2. Click **New repository secret**.
   - **Name:** `NTFY_TOPIC`
   - **Secret:** Paste the exact topic name you created in Step 2.
3. Click **New repository secret** again.
   - **Name:** `CANVAS_FEEDS`
   - **Secret:** Create a JSON object mapping the name of your courses to their RSS URLs:
   ```json
   {
     "Data Structures": "https://canvas.edu/feeds/announcements/111.atom",
     "Physics II": "https://canvas.edu/feeds/announcements/222.atom"
   }
   ```

   *(Important: You can use JSONLint to validate your text before pasting it.).*

### Step 4: Grant bot permissions
1. In your repository, go to **Settings > Actions > General**.
2. Scroll down to **Workflow permissions**.
3. Select **Read and write permissions**.
4. Check *"Allow GitHub Actions to create and approve pull requests"* and click **Save**.

### Step 5: Generate a Fine-Grained GitHub Token
For security reasons (since external services will hold the token), we use a fine-grained token scoped strictly to this repository instead of a classic token.
1. Click your GitHub profile picture (top right) > **Settings** > **Developer settings**.
2. Go to **Personal access tokens** > **Fine-grained tokens** and click **Generate new token**.
3. Name the token (e.g., `Cron Canvas Bot`).
4. Under **Repository access**, select **Only select repositories** and choose your private Canvas bot repository.
5. Under **Repository permissions**, grant **Read and write** access to **Contents**, **Secrets**, and **Actions**.
6. Click **Generate token** and copy the value starting with `github_pat_`.

### Step 6: Configure the trigger in cron-job.org
We use an external cron job to guarantee execution without GitHub's internal delays.
1. Create a free account at [cron-job.org](https://cron-job.org/) and click **Create cronjob**.
2. **Title:** Enter a name like `Cron Canvas Notifier`.
3. **URL:** `https://api.github.com/repos/<YOUR_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/main.yml/dispatches` 
4. **Schedule (Crontab Expression):** You can set exactly when you want the bot to run. For example, using `*/30 6-23 * * *` will run the check every 30 minutes, except during the early morning hours (midnight to 5:59 AM) to save GitHub Action minutes.
5. Go to the **Advanced** section:
   * **Request method:** `POST`
   * **Request body:** Select Custom and enter `{"ref": "main"}`
6. Under **Headers**, add the following three key-value pairs:
   * `Content-Type`: `application/json`
   * `Accept`: `application/vnd.github.v3+json`
   * `Authorization`: `Bearer github_pat_YOUR_TOKEN` (replace with your exact token from Step 5).
7. Save the cronjob!

**You're all set!** 
The external cron will now perfectly trigger your GitHub Action on schedule.