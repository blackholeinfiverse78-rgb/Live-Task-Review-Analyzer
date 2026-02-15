# 🛡️ Live Task Review Agent

> **Deterministic Engineering Task Analysis System**

A comprehensive AI-powered task review system that analyzes engineering submissions using multiple data sources including GitHub repositories, PDF documentation, and various AI models. Features a modern web interface with real-time analysis, PDF upload, and text-to-speech capabilities.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/blackholeinfiverse78-rgb/Live-Task-Review-Analyzer)

---

## ✨ Features

### 🎯 Core Functionality
- **Task Submission & Review** - Submit engineering tasks for comprehensive analysis
- **Multi-Source Analysis** - Combines GitHub repo analysis, PDF processing, and AI insights
- **Deterministic Scoring** - Objective evaluation based on technical quality, clarity, and discipline signals
- **Next Task Generation** - AI-powered recommendations for follow-up tasks

### 🎨 Frontend
- **Modern UI** - Beautiful glassmorphism design with dark/light themes
- **PDF Upload** - Analyze project documentation directly
- **Text-to-Speech** - Hear analysis results in multiple languages
- **Demo Scenarios** - Pre-loaded examples to test the system
- **Real-time Analysis** - Live progress and instant results

### 🔧 Backend Services
- **GitHub Analysis** - Repository metrics, languages, commit history
- **PDF Processing** - Extract and analyze documentation
- **TTS Service** - VaaniTTS integration for audio output
- **YouTube API** - Video search integration
- **Financial Data** - Alpha Vantage API integration
- **AI Models** - Support for OpenAI, Gemini, Groq, and Ollama

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/blackholeinfiverse78-rgb/Live-Task-Review-Analyzer.git
   cd Live-Task-Review-Analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the backend:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
   ```

5. **Open the frontend:**
   ```bash
   # Open frontend/index.html in your browser
   # Or use:
   start frontend/index.html
   ```

---

## 🌐 Deploy to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/blackholeinfiverse78-rgb/Live-Task-Review-Analyzer)

### Manual Deployment

1. **Push to GitHub** (already done if you cloned this repo)

2. **Import to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository

3. **Add Environment Variables:**
   ```
   GITHUB_TOKEN=your_github_token_here
   GEMINI_API_KEY=your_key_here (optional)
   GROQ_API_KEY=your_key_here (optional)
   OPENAI_API_KEY=your_key_here (optional)
   ```

4. **Deploy!**
   - Vercel auto-detects configuration
   - Your app will be live in ~3 minutes

📖 **Detailed Guide:** See [`docs/VERCEL_DEPLOYMENT.md`](docs/VERCEL_DEPLOYMENT.md)

---

## 📁 Project Structure

```
Live-Task-Review-Agent/
├── api/
│   └── index.py              # Vercel serverless entry point
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API routes
│   │   ├── task.py         # Task submission & review
│   │   ├── orchestrator.py # Task orchestration
│   │   └── tts.py          # Text-to-speech
│   └── services/            # Backend services
│       ├── repo_analyzer.py    # GitHub analysis
│       ├── pdf_processor.py    # PDF processing
│       └── tts_integration.py  # TTS service
├── frontend/
│   └── index.html           # Web interface
├── tests/                   # Test files
├── docs/                    # Documentation
├── VaaniTTS_Standalone/     # TTS service
├── vercel.json             # Vercel configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🔑 Environment Variables

### Required
- `GITHUB_TOKEN` - GitHub Personal Access Token for repository analysis

### Optional (for full features)
- `GEMINI_API_KEY` - Google Gemini API key
- `GROQ_API_KEY` - Groq API key
- `OPENAI_API_KEY` - OpenAI API key
- `YOUTUBE_API_KEY` - YouTube Data API key
- `ALPHA_VANTAGE_API_KEY` - Alpha Vantage API key
- `AGENTOPS_API_KEY` - AgentOps API key

### How to Get API Keys
- **GitHub Token:** [github.com/settings/tokens](https://github.com/settings/tokens)
- **Gemini:** [ai.google.dev](https://ai.google.dev)
- **Groq:** [console.groq.com](https://console.groq.com)
- **OpenAI:** [platform.openai.com](https://platform.openai.com)

---

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Task Review
```bash
POST /api/v1/task/review
Content-Type: multipart/form-data

{
  "title": "Task title",
  "description": "Detailed description",
  "github_url": "https://github.com/user/repo",
  "pdf_file": <file>,
  "submitted_by": "Your name"
}
```

### Text-to-Speech
```bash
POST /api/v1/tts/speak
Content-Type: application/json

{
  "text": "Text to speak",
  "language": "en",
  "mode": "stream"
}
```

### API Documentation
- **Interactive Docs:** `http://localhost:3000/docs`
- **OpenAPI Schema:** `http://localhost:3000/openapi.json`

---

## 🎯 Usage Examples

### Submit a Task via UI

1. Open `frontend/index.html` in your browser
2. Select a demo scenario or enter your own task
3. Optionally upload a PDF document
4. Click "Analyze Submission"
5. View detailed results and recommendations

### Submit a Task via API

```python
import requests

url = "http://localhost:3000/api/v1/task/review"
data = {
    "title": "Build REST API",
    "description": "Create a RESTful API with authentication",
    "github_url": "https://github.com/user/repo",
    "submitted_by": "Developer"
}

response = requests.post(url, data=data)
print(response.json())
```

### Use Text-to-Speech

```python
import requests

url = "http://localhost:3000/api/v1/tts/speak"
data = {
    "text": "Hello, this is a test",
    "language": "en",
    "mode": "stream"
}

response = requests.post(url, json=data)
with open("output.wav", "wb") as f:
    f.write(response.content)
```

---

## 🧪 Testing

### Run System Tests
```bash
cd tests
python system_test.py
```

### Run API Tests
```bash
pytest tests/
```

### Test Individual Components
```bash
# Test Gemini integration
python tests/test_gemini.py

# Test Groq integration
python tests/test_groq.py

# Test API endpoints
python tests/test_api_live.py
```

---

## 📖 Documentation

Comprehensive guides are available in the [`docs/`](docs/) directory:

### Deployment
- [`DEPLOY_NOW.md`](docs/DEPLOY_NOW.md) - Quick deployment guide
- [`VERCEL_DEPLOYMENT.md`](docs/VERCEL_DEPLOYMENT.md) - Detailed Vercel guide
- [`GIT_PUSH_GUIDE.md`](docs/GIT_PUSH_GUIDE.md) - Git authentication guide

### Features
- [`UI_NEW_FEATURES.md`](docs/UI_NEW_FEATURES.md) - Frontend features guide
- [`TTS_TROUBLESHOOTING.md`](docs/TTS_TROUBLESHOOTING.md) - TTS setup guide
- [`FRONTEND_GUIDE.md`](docs/FRONTEND_GUIDE.md) - Frontend documentation

### Status & Reports
- [`DEPLOYMENT_READY.md`](docs/DEPLOYMENT_READY.md) - Deployment checklist
- [`FINAL_STATUS_REPORT.md`](docs/FINAL_STATUS_REPORT.md) - System status
- [`SYSTEM_READY.md`](docs/SYSTEM_READY.md) - Setup verification

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI
- **Runtime:** Python 3.9+
- **Server:** Uvicorn
- **AI Models:** OpenAI, Gemini, Groq
- **PDF Processing:** pdfplumber
- **TTS:** gTTS, pyttsx3

### Frontend
- **Core:** HTML5, CSS3, JavaScript (ES6+)
- **Styling:** Vanilla CSS with glassmorphism
- **API Calls:** Fetch API
- **Storage:** LocalStorage

### Deployment
- **Platform:** Vercel (Serverless)
- **CI/CD:** GitHub Actions (optional)
- **Hosting:** Vercel Edge Network

---

## 🎨 UI Features

### Theme Toggle
- Light mode with gradient backgrounds
- Dark mode with sleek purple/blue theme
- Persistent theme preference

### PDF Upload
- Drag-and-drop file input
- File size and name display
- Integrated with backend analysis

### Text-to-Speech
- Multi-language support (English, Hindi, Spanish, French, German)
- Audio player with controls
- Real-time speech generation

### Demo Scenarios
- **Good Submission** - High-quality example
- **Partial Submission** - Medium-quality example
- **Poor Submission** - Low-quality example
- **Live Editor** - Create your own

---

## 🔧 Configuration

### Backend Configuration
Edit `app/main.py` to customize:
- CORS settings
- API routes
- Middleware
- Error handling

### Frontend Configuration
Edit `frontend/index.html` to customize:
- Backend URL (auto-detected)
- Theme colors
- Demo scenarios
- UI text

### Vercel Configuration
Edit `vercel.json` to customize:
- Build settings
- Routes
- Environment variables
- Serverless functions

---

## 🚨 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
netstat -ano | findstr :3000
```

### Frontend Shows "Backend Offline"
1. Ensure backend is running on port 3000
2. Check `http://localhost:3000/health`
3. Hard refresh browser (Ctrl+Shift+R)

### TTS Not Working
- TTS may have limitations on serverless platforms
- For local: Ensure audio drivers are installed
- For production: Consider cloud TTS services

### PDF Upload Fails
- Check file size (max 4.5MB on Vercel free tier)
- Ensure PDF is not corrupted
- Verify `pdfplumber` is installed

📖 **More Help:** See [`docs/TTS_TROUBLESHOOTING.md`](docs/TTS_TROUBLESHOOTING.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **Vercel** - Deployment platform
- **VaaniTTS** - Text-to-speech service
- **pdfplumber** - PDF processing
- **OpenAI, Gemini, Groq** - AI models

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/blackholeinfiverse78-rgb/Live-Task-Review-Analyzer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/blackholeinfiverse78-rgb/Live-Task-Review-Analyzer/discussions)
- **Documentation:** [`docs/`](docs/) directory

---

## 🎯 Roadmap

- [ ] Add more AI model integrations
- [ ] Implement user authentication
- [ ] Add database for task history
- [ ] Create mobile app
- [ ] Add real-time collaboration
- [ ] Implement webhooks for CI/CD integration

---

## 📊 Status

**Version:** 2.0.0
**Status:** ✅ Production Ready
**Last Updated:** 2026-02-15

---

<div align="center">

**Made with ❤️ by [blackholeinfiverse78-rgb](https://github.com/blackholeinfiverse78-rgb)**

⭐ Star this repo if you find it helpful!

</div>
