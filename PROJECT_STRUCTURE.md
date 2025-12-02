# 📁 Project Structure - Script Doctor Pro

**Cấu trúc project sau khi cleanup**

---

## 🎯 Core Application Files (Bắt buộc)

```
app.py                      # Main Streamlit application
ai_engine.py               # AI/Gemini integration
script_parser.py           # PDF parsing & scene detection
character_engine.py        # Character analysis
export_engine.py           # DOCX export
utils.py                   # Utilities & session management
requirements.txt           # Python dependencies
```

---

## 📚 Documentation Files

### Main Documentation
```
README.md                  # Full documentation (English)
README_MACOS.md           # macOS user guide (Vietnamese)
README_GITHUB.md          # GitHub repository README
QUICKSTART.md             # Quick start guide
CHANGELOG.md              # Version history
LICENSE                   # License file
```

### Deployment Documentation
```
KET_LUAN_DEPLOY.md        # ⭐ Tóm tắt deployment (Vietnamese)
QUICK_DEPLOY.md           # ⭐ Quick deploy guide (20 min)
DEPLOYMENT_INDEX.md       # Documentation index
DEPLOYMENT_SUMMARY.md     # Comprehensive analysis
DEPLOYMENT_STREAMLIT_CLOUD.md  # Streamlit Cloud guide
DEPLOYMENT_ALTERNATIVES.md     # Alternative platforms
DEPLOYMENT_CHECKLIST.md   # Full checklist
GITHUB_SETUP.md           # GitHub setup guide
```

---

## 🔧 Configuration Files

```
.gitignore                # Git ignore rules
.env                      # Environment variables (empty, for local dev)
```

### Streamlit Config
```
.streamlit/
  ├── config.toml.example      # Config template
  └── secrets.toml.example     # Secrets template
```

### CI/CD
```
.github/
  └── workflows/
      └── streamlit-deploy.yml  # GitHub Actions workflow
```

---

## 🖥️ Platform-Specific Launchers

### Windows
```
run_app.bat               # Windows launcher
```

### macOS
```
run_app_macos.command     # macOS double-click launcher
install_macos.sh          # macOS installation script
fix_permissions_macos.sh  # macOS permissions fixer
```

### Linux/Unix
```
run_app.sh                # Linux/Unix launcher
```

---

## 📂 Data Directory

```
data/
  └── .gitkeep            # Keep directory in Git
  
# Actual data files are gitignored:
# - current_session.json
# - projects.json
```

---

## 🚫 Ignored Directories (Not in Git)

```
__pycache__/              # Python cache
.venv/                    # Virtual environment
.vscode/                  # VS Code settings
.idea/                    # PyCharm settings
```

---

## 📊 File Count Summary

**Total Files:** 29 files
- Core Python: 6 files
- Documentation: 13 files
- Configuration: 5 files
- Launchers: 4 files
- Other: 1 file (LICENSE)

**Total Directories:** 3 tracked directories
- `.streamlit/` - Streamlit config
- `.github/` - CI/CD workflows
- `data/` - Application data

---

## 🗑️ Files Removed (Cleanup)

Đã xóa các file không cần thiết:
- ❌ `DEPLOYMENT.md` (replaced by new docs)
- ❌ `PACKAGE_SUMMARY.md` (not needed)
- ❌ `MACOS_PACKAGE_SUMMARY.md` (not needed)
- ❌ `MACOS_INSTALLATION_INSTRUCTIONS.txt` (info in README_MACOS.md)
- ❌ `t.html` (reference file, no longer needed)
- ❌ `t_readable.html` (reference file, no longer needed)
- ❌ `script_export.docx` (generated output, not source)

---

## 📦 What to Commit to GitHub

### ✅ Include:
- All core Python files
- All documentation files
- Configuration examples (`.example` files)
- Launchers (`.bat`, `.sh`, `.command`)
- `.gitignore`
- `LICENSE`
- `data/.gitkeep`

### ❌ Exclude (via .gitignore):
- `.env` (contains secrets)
- `.streamlit/secrets.toml` (contains API keys)
- `data/*.json` (session data)
- `__pycache__/` (Python cache)
- `.venv/` (virtual environment)
- `*.docx`, `*.pdf` (generated files)

---

## 🎯 Recommended Reading Order

### For Deployment:
1. `KET_LUAN_DEPLOY.md` - Quick summary
2. `QUICK_DEPLOY.md` - Step-by-step guide
3. `DEPLOYMENT_INDEX.md` - Full documentation index

### For Development:
1. `README.md` - Full documentation
2. `QUICKSTART.md` - Quick start
3. `CHANGELOG.md` - Version history

### For Users:
1. `README_MACOS.md` - macOS users (Vietnamese)
2. `README.md` - All users (English)
3. `QUICKSTART.md` - Quick start

---

## 🔍 File Size Estimate

```
Core Application:  ~100 KB
Documentation:     ~150 KB
Configuration:     ~10 KB
Total (tracked):   ~260 KB
```

**Very lightweight!** Perfect for GitHub and deployment.

---

## 📝 Notes

- Project is clean and ready for GitHub
- All sensitive files are gitignored
- Documentation is comprehensive
- Multiple platform support (Windows, macOS, Linux)
- Ready for Streamlit Cloud deployment

---

**Last Updated:** December 2, 2025
