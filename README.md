# 🎬 Script Doctor Pro - AI Screenplay Assistant

## Overview

Script Doctor Pro is an advanced AI-powered screenplay analysis and editing tool designed for filmmakers, producers, and screenwriters. It combines creative analysis with marketing insights to help develop commercially viable screenplays.

## ✨ Key Features

### 1. **Dual-View Analysis**
- **Creative Doctor Perspective**: Structure, character development, tension, and "Show vs Tell" analysis
- **Marketing Perspective (Maya)**: Market analysis, USP identification, commercial potential, and box office estimation

### 2. **Scene-by-Scene Editing**
- Interactive script editor with line numbers
- AI-powered brainstorming with multiple rewrite options
- Real-time refinement and diff view
- Undo/Redo functionality

### 3. **Action Plan Generation**
- Strategic editing roadmap based on dual analysis
- Task management with progress tracking
- AI auto-fix for automated scene improvements
- Manual editing with guided instructions

### 4. **Advanced AI Features**
- Show, Don't Tell conversion (dialogue to visual actions)
- Character analysis and development tracking
- Multi-language support (Vietnamese/English)
- Cost tracking for API usage

### 5. **Export & Collaboration**
- Professional screenplay format (.docx export)
- Session state persistence
- Project management (in development)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://ai.google.dev/))

### Quick Start (Windows)

1. **Double-click `run_app.bat`**
   - Automatically creates virtual environment
   - Installs all dependencies
   - Launches the application

### Manual Installation

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

## 📁 Project Structure

```
ScriptDoctor_App/
├── app.py                 # Main Streamlit application
├── ai_engine.py          # AI/Gemini integration & analysis logic
├── script_parser.py      # PDF parsing & scene detection
├── character_engine.py   # Character analysis features
├── export_engine.py      # DOCX export functionality
├── utils.py              # Session management & utilities
├── requirements.txt      # Python dependencies
├── run_app.bat          # Windows launcher script
├── .env                 # Environment variables (API keys)
├── data/                # Session & project data
│   ├── current_session.json
│   └── projects.json
└── README.md            # This file
```

## ⚙️ Configuration

### API Key Setup

1. **Get your Gemini API Key** from [Google AI Studio](https://ai.google.dev/)

2. **Option A - In Application:**
   - Open the app
   - Enter API key in sidebar
   - Click "Kiểm tra kết nối" to verify

3. **Option B - Environment File:**
   ```bash
   # Create .env file
   echo GEMINI_API_KEY=your_api_key_here > .env
   ```

## 📖 User Guide

### 1. Import Screenplay

- **Tab 1: Review & Phân tích**
- Upload PDF screenplay file
- System auto-parses scenes with intelligent detection
- Supports multiple scene ID formats (numbered, lettered, AUTO)

### 2. Run Dual Analysis

- Click **"🔍 Phân tích Lại Kịch bản (Dual View)"**
- Wait 20-30 seconds for AI processing
- Review both Creative and Marketing reports
- Check summary table for key insights

### 3. Edit Scenes

- **Tab 2: Brainstorm Sáng tạo**
- Select scene from sidebar navigator
- Edit script in the editor pane
- Add director's notes for AI guidance
- Generate multiple rewrite options
- Preview differences before applying
- Use "Show, Don't Tell" for dialogue improvements

### 4. Create Action Plan

- **Tab 3: Lập Kế hoạch (Action Plan)**
- Input strategic goals (from AI analysis or custom)
- Generate comprehensive task list
- Use AI Auto-Fix for automated improvements
- Track progress with visual indicators
- Mark tasks complete as you work

### 5. Export

- Click **"Tạo file Word (.docx)"** in sidebar
- Professional screenplay format
- Includes all edited scenes
- Ready for production or distribution

## 🎨 UI Features

### Modern Design System
- Dark mode with glassmorphism effects
- System fonts for native feel
- Responsive layout (68/32 split for editor)
- Progress bars with gradient fills
- Color-coded task priorities

### Scene Navigator
- Status indicators (✓ Completed, ✏️ Edited, 📄 Pending)
- Quick jump to any scene
- Real-time editing status

### Task Management
- Priority-based grouping (🔥 High, ⚠️ Medium, 📄 Low)
- Checkbox completion tracking
- Action buttons (👁️ View, ⚡ AI Fix)
- Collapsible task groups

## 💡 Tips & Best Practices

### For Best Results:

1. **Upload clean PDF files** - Use standard screenplay format
2. **Write clear director's notes** - Specific instructions yield better AI results
3. **Review AI suggestions carefully** - AI is a tool, not a replacement for creative judgment
4. **Use the diff view** - Always compare before applying changes
5. **Save frequently** - Changes are auto-saved, but manual saves ensure persistence
6. **Track costs** - Monitor API usage in the sidebar cost tracker

### Common Workflows:

**Quick Polish:**
1. Import script → 2. Run dual analysis → 3. Review suggestions → 4. Export

**Deep Rewrite:**
1. Import → 2. Analyze → 3. Create action plan → 4. AI auto-fix scenes → 5. Manual refinement → 6. Export

**Marketing Focus:**
1. Import → 2. Dual analysis → 3. Focus on Marketing report → 4. Use suggestions in Action Plan → 5. Export

## 🔧 Troubleshooting

### Common Issues:

**App won't start:**
- Ensure Python 3.8+ is installed
- Check if port 8501 is available
- Try deleting `.venv` and running `run_app.bat` again

**API Key errors:**
- Verify key is correct
- Check internet connection
- Ensure key has Gemini API access enabled

**PDF import fails:**
- Ensure PDF is not password-protected
- Try re-exporting PDF with standard fonts
- Check if PDF has selectable text (not scanned images)

**Scene detection issues:**
- Verify screenplay follows standard format
- Scene headers should be in CAPS with INT./EXT.
- Check PDF for formatting artifacts

## 📊 Technical Specifications

### Dependencies:
- **streamlit** - Web application framework
- **pandas** - Data manipulation
- **google-generativeai** - AI/Gemini integration
- **pypdf** - PDF text extraction
- **python-docx** - DOCX export
- **python-dotenv** - Environment configuration

### System Requirements:
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB for application + dependencies
- **Internet**: Required for AI features
- **Browser**: Modern browser (Chrome, Firefox, Edge)

### Performance:
- **PDF Import**: ~2-5 seconds per screenplay
- **Scene Parsing**: Instant (<1 second)
- **Dual Analysis**: 20-40 seconds (depends on script length)
- **Brainstorm**: 10-20 seconds per scene
- **Action Plan**: 15-30 seconds

## 🔐 Privacy & Security

- **Local First**: All script data stored locally on your machine
- **API Security**: API keys stored in local .env file (never shared)
- **No Cloud Storage**: No scripts are uploaded to external servers (except Gemini API for processing)
- **Session Data**: Stored in local `data/` directory

## 📝 License & Credits

**Developed by**: AI Kenny Team
**Version**: 1.0.0
**Last Updated**: December 2025

### Technology Credits:
- Streamlit Community
- Google Gemini AI
- Python Software Foundation

## 🆘 Support

For issues, questions, or feature requests:
- Check this README first
- Review the in-app help tooltips
- Contact: [Your support email/contact]

## 🚀 Future Roadmap

### Planned Features:
- [ ] Multi-project management
- [ ] Collaborative editing
- [ ] Version control integration
- [ ] Custom AI model fine-tuning
- [ ] Mobile app support
- [ ] Real-time collaboration
- [ ] Advanced character relationship mapping
- [ ] Integration with industry-standard software (Final Draft, etc.)

---

**Thank you for using Script Doctor Pro!** 🎬

*Empowering filmmakers with AI-driven screenplay development.*
