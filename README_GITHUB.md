# 🎬 Script Doctor Pro

AI-powered screenplay analysis and editing tool for filmmakers and screenwriters.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## ✨ Features

- **Dual-View Analysis**: Creative + Marketing perspectives
- **Scene-by-Scene Editing**: AI-powered brainstorming with multiple rewrite options
- **Action Plan Generation**: Strategic editing roadmap
- **Show, Don't Tell**: Convert dialogue to visual actions
- **Export to DOCX**: Professional screenplay format

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/script-doctor-pro.git
cd script-doctor-pro

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo GEMINI_API_KEY=your_key_here > .env

# Run app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Add your `GEMINI_API_KEY` in Secrets
6. Deploy!

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key ([Get it here](https://ai.google.dev/))

## 🔧 Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash
- **PDF Parsing**: PyPDF
- **Export**: python-docx

## 📖 Documentation

- [Full Documentation](README.md)
- [Deployment Guide](DEPLOYMENT_STREAMLIT_CLOUD.md)
- [GitHub Setup](GITHUB_SETUP.md)

## 🔒 Security

- Never commit `.env` or API keys
- Use Streamlit Secrets for production
- See [Security Best Practices](GITHUB_SETUP.md#-checklist-bảo-mật)

## 📄 License

See [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Made with ❤️ by AI Kenny Team**
