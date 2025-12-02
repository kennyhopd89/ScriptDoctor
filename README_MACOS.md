# 🍎 Script Doctor Pro - macOS User Guide

## Quick Start for Non-Technical Users

This guide will help you set up and run **Script Doctor Pro** on your Mac, even if you've never used Terminal or programming tools before.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **macOS 10.15 (Catalina) or later**
  - Works on both Intel and Apple Silicon (M1/M2/M3) Macs
- ✅ **Internet connection** (for installation and API access)
- ✅ **Google Gemini API Key** (free, we'll show you how to get one)

---

## 🚀 Installation (One-Time Setup)

### Step 1: Download the App

1. Download the **Script Doctor Pro** folder
2. Unzip it if needed
3. Move the folder to a convenient location (e.g., your Desktop or Documents)

### Step 2: Run the Installer

**Option A: Double-Click Method (Recommended)**

1. Open the **Script Doctor Pro** folder
2. Find the file named `install_macos.sh`
3. **Right-click** on it and select **"Open"** (or **"Open With" → "Terminal"**)
4. If macOS warns you about opening a file from the internet:
   - Click **"Open"** in the security dialog
   - Or go to **System Settings → Privacy & Security** and click **"Open Anyway"**

**Option B: Terminal Method**

1. Open **Terminal** (you can find it in Applications → Utilities)
2. Type `cd ` (with a space after cd)
3. Drag the **Script Doctor Pro** folder into the Terminal window
4. Press **Enter**
5. Type: `chmod +x install_macos.sh`
6. Press **Enter**
7. Type: `./install_macos.sh`
8. Press **Enter**

### Step 3: Follow the Installation

The installer will:

1. ✅ Check your macOS version
2. ✅ Install **Homebrew** (if needed) - a tool to install other tools
   - If asked, enter your Mac password (it won't show on screen, that's normal)
3. ✅ Install **Python** (if needed) - the programming language the app uses
4. ✅ Create a safe environment for the app
5. ✅ Download and install all required components
6. ✅ Ask for your **Gemini API Key** (see next section)

**Total installation time**: 5-10 minutes (depending on your internet speed)

### Step 4: Get Your Gemini API Key

During installation, you'll be asked for a **Gemini API Key**. Here's how to get one:

1. Visit: **https://ai.google.dev/**
2. Click the button **"Get API Key in Google AI Studio"**
3. Sign in with your **Google account** (Gmail)
4. Click **"Create API Key"** or **"Get API Key"**
5. Click **"Create API key in new project"**
6. **Copy** the API key that appears
7. **Paste** it into the Terminal when asked

**Note**: The Gemini API is free for moderate use. You won't be charged unless you use it heavily.

**Don't have your key ready?** You can skip this step and add it later (see FAQ section).

### Step 5: Installation Complete! 🎉

When you see "✓ Installation Complete!", you're all set!

The installer will ask if you want to start the app now. Choose **Yes** to test it immediately.

---

## 🎬 Running the App (Every Time You Use It)

After installation, starting the app is super easy:

### Method 1: Double-Click (Easiest)

1. Open the **Script Doctor Pro** folder
2. **Double-click** the file named `run_app_macos.command`
3. The app will open in your **web browser** automatically
4. If macOS asks for permission, click **"Open"**

### Method 2: Terminal

1. Open **Terminal**
2. Navigate to the folder: `cd /path/to/ScriptDoctor_App`
3. Run: `./run_app_macos.command`

### What You'll See

- A **Terminal window** opens with status messages
- Your **web browser** opens automatically
- The app appears at **http://localhost:8501**
- You're ready to upload and analyze screenplays!

**Important**: Keep the Terminal window open while using the app. Closing it will stop the app.

---

## 🛑 Stopping the App

When you're done:

1. Go to the **Terminal window**
2. Press **Ctrl + C** (hold Control and press C)
3. The app will stop gracefully
4. You can close the Terminal window

---

## 📖 Using the App

### First Time Setup (in the App)

If you skipped entering the API key during installation:

1. Look at the **left sidebar** in the app
2. Find the **"Cấu hình AI"** section
3. Paste your **Gemini API Key** in the text box
4. Click **"Kiểm tra kết nối"** to test it
5. Wait for **"Kết nối thành công!"** (Connection successful!)

### Basic Workflow

1. **Tab 1: Review & Phân tích**
   - Click **"Upload file PDF"**
   - Select your screenplay PDF
   - Click **"🔍 Phân tích Lại Kịch bản (Dual View)"**
   - Wait ~30 seconds for analysis

2. **Tab 2: Brainstorm Sáng tạo**
   - Select a scene from the sidebar
   - Edit the script
   - Add director's notes
   - Click **"Brainstorm Ideas"**
   - Review AI suggestions

3. **Tab 3: Lập Kế hoạch (Action Plan)**
   - Create a strategic editing plan
   - Use **AI Auto-Fix** for quick improvements
   - Track progress with checkboxes

4. **Export**
   - Click **"Tạo file Word (.docx)"** in the sidebar
   - Download your polished screenplay

For detailed feature explanations, see **README.md** or **QUICKSTART.md**.

---

## 🆘 Troubleshooting

### Problem: "Permission denied" when running scripts

**Solution**:
```bash
# Open Terminal in the app folder, then run:
chmod +x install_macos.sh
chmod +x run_app_macos.command
```

### Problem: "Homebrew is not installed" and installation fails

**Solution**:
1. Install Homebrew manually from: **https://brew.sh**
2. Copy and paste the installation command from the website
3. After Homebrew is installed, run `install_macos.sh` again

### Problem: "Python not found" or "Wrong Python version"

**Solution**:
```bash
# Install Python 3.11 via Homebrew:
brew install python@3.11
```

### Problem: "Virtual environment not found" when launching

**Solution**:
You need to run the installer first:
```bash
./install_macos.sh
```

### Problem: API key not working

**Possible causes**:
1. ❌ Typo when copying the key → Copy again carefully
2. ❌ Key not activated → Wait a few minutes after creating it
3. ❌ API not enabled → Check Google Cloud Console

**Solution**:
1. Get a new API key from https://ai.google.dev/
2. Edit the `.env` file in the app folder:
   ```
   GEMINI_API_KEY=your_new_key_here
   ```
3. Save and restart the app

### Problem: App opens but shows errors

**Solution**:
```bash
# Reinstall dependencies:
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Problem: Browser doesn't open automatically

**Solution**:
Manually open your browser and go to: **http://localhost:8501**

### Problem: Port 8501 already in use

**Solution**:
Another instance is running. Either:
- Close the other Terminal window running the app
- OR use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## 💡 Tips for macOS Users

### Making Scripts Easier to Run

**Option 1: Add to Dock**
1. Drag `run_app_macos.command` to your **Dock**
2. Click it anytime to launch the app

**Option 2: Create an Alias**
1. Right-click `run_app_macos.command`
2. Select **"Make Alias"**
3. Move the alias to your Desktop or Applications folder

**Option 3: Use Spotlight**
1. Press **Cmd + Space**
2. Type "run_app_macos"
3. Press **Enter**

### Terminal Tips

- **Ctrl + C**: Stop the app
- **Cmd + T**: New Terminal tab
- **Cmd + K**: Clear Terminal screen
- **Arrow Up**: Recall previous command

---

## 🔐 Security & Privacy

### What Gets Installed?

- **Homebrew**: Package manager (safe, trusted by millions)
- **Python 3.11**: Programming language (official Python.org version)
- **Python packages**: Listed in `requirements.txt` (all from official PyPI repository)

### Where Is Data Stored?

- **Scripts**: Only on your Mac (in the `data/` folder)
- **API calls**: Sent to Google Gemini for AI analysis
- **API key**: Stored locally in `.env` file (never shared)

### Is This Safe?

✅ Yes! The app:
- Runs entirely on your Mac
- Uses official, trusted software
- Doesn't collect or upload personal data
- Only sends screenplay text to Gemini API for analysis

---

## 📁 File Structure

```
Script Doctor Pro/
├── install_macos.sh          ← Run this once to set up
├── run_app_macos.command     ← Double-click this to start app
├── README_MACOS.md           ← This file
├── app.py                    ← Main application
├── requirements.txt          ← List of dependencies
├── .env                      ← Your API key (created during setup)
├── .venv/                    ← Python environment (auto-created)
└── data/                     ← Your saved sessions
```

---

## ❓ FAQ

### Q: Do I need to know how to code?
**A**: No! Just follow this guide step-by-step.

### Q: Is this free?
**A**: The app is free. The Gemini API is free for moderate use (generous free tier).

### Q: Can I move the app folder after installation?
**A**: Yes, but you may need to run `install_macos.sh` again to fix paths.

### Q: How do I update the app?
**A**: Download the new version and run `install_macos.sh` again (it will preserve your settings).

### Q: Can I use this offline?
**A**: No, the AI features require internet access to communicate with Gemini API.

### Q: What if I get a "zsh: permission denied" error?
**A**: Run `chmod +x *.sh *.command` in the app folder via Terminal.

### Q: I forgot my API key, where can I find it?
**A**: 
- Check the `.env` file in the app folder
- Or get a new one from https://ai.google.dev/

### Q: Can multiple people use the same Mac with different API keys?
**A**: Yes, each user can have their own copy of the app folder with their own `.env` file.

---

## 📞 Getting Help

If you're stuck:

1. **Check this README** - Most answers are here
2. **Check QUICKSTART.md** - For feature tutorials
3. **Check README.md** - For complete documentation
4. **Check error messages** - They often tell you what's wrong

---

## 🎬 You're Ready!

Congratulations! You now have Script Doctor Pro running on your Mac.

**Next steps**:
1. ✅ Run the app: Double-click `run_app_macos.command`
2. ✅ Upload a screenplay PDF
3. ✅ Run your first AI analysis
4. ✅ Start improving your script!

**Happy screenwriting!** 🎥✨

---

**Version**: 1.0.0 (macOS Edition)  
**Last Updated**: December 2025  
**Support**: See README.md for contact information
