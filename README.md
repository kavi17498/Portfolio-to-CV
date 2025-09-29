# Portfolio to CV Converter

A FastAPI-based web service that automatically converts portfolio websites into professional, ATS-friendly CV/Resume PDFs using AI-powered content extraction.

## 🌟 Features

- **AI-Powered Extraction**: Uses Google Gemini AI to intelligently extract CV data from portfolio websites
- **ATS-Friendly PDFs**: Generates professionally formatted CVs optimized for Applicant Tracking Systems
- **Web Scraping**: Automatically scrapes and processes portfolio content using Jina AI
- **REST API**: Clean API endpoints for integration with frontend applications
- **Customizable Output**: Allows editing of extracted data before PDF generation
- **Professional Formatting**: Clean, modern CV layout with proper typography and spacing

## 🚀 Live Demo

The service provides two main functionalities:
1. **Scrape & Extract**: Convert portfolio websites to structured CV data
2. **Generate PDF**: Create professional PDFs from CV data

## 📋 Prerequisites

- Python 3.8+
- Google AI Studio API Key (Gemini)
- Internet connection for web scraping

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kavi17498/Portfolio-to-CV.git
cd Portfolio-to-CV/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install fastapi uvicorn python-dotenv google-generativeai requests reportlab
```

### 3. Set Up Environment Variables

Create a `.env` file in the backend directory:
```bash
# In the backend folder
touch .env
```

Add your Google AI API key to the `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Get Google AI Studio API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key and paste it in your `.env` file

**Note**: Make sure to use Gemini 1.5 Flash model (currently supported)

### 5. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🔧 API Endpoints

### 1. Scrape Portfolio Website
```http
GET /scrape/{url}?format=json
```

**Example:**
```bash
curl "http://localhost:8000/scrape/https://johndoe.portfolio.com"
```

**Response:**
```json
{
  "parsed_data": {
    "personal_information": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-123-4567"
    },
    "professional_summary": "Experienced developer...",
    "skills": ["Python", "JavaScript", "React"],
    "work_experience": [...],
    "education": [...],
    "projects": [...]
  }
}
```

### 2. Generate PDF from CV Data
```http
POST /generate-pdf
```

**Request Body:**
```json
{
  "cv_data": {
    "personal_information": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "skills": ["Python", "FastAPI", "React"]
  },
  "filename": "John_Doe_Resume"
}
```

**Response:** PDF file download

## 🎯 Usage Workflow

### Option 1: Direct PDF Generation
```bash
# Scrape and get PDF directly
curl "http://localhost:8000/scrape/https://portfolio-url.com?format=pdf" --output resume.pdf
```

### Option 2: Extract, Edit, Generate (Recommended)
```bash
# 1. Extract CV data
curl "http://localhost:8000/scrape/https://portfolio-url.com" > cv_data.json

# 2. Edit the cv_data.json file as needed

# 3. Generate PDF with edited data
curl -X POST "http://localhost:8000/generate-pdf" \
  -H "Content-Type: application/json" \
  -d @cv_data.json --output resume.pdf
```

## 🌐 Frontend Integration

The API includes CORS support for `http://localhost:3000` (React/Next.js apps).

### JavaScript Example:
```javascript
// Scrape portfolio
const response = await fetch('/scrape/https://portfolio-url.com');
const cvData = await response.json();

// Generate PDF
const pdfResponse = await fetch('/generate-pdf', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    cv_data: cvData.parsed_data,
    filename: 'My_Resume'
  })
});

const blob = await pdfResponse.blob();
// Handle PDF download
```

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── pdf_generator.py     # ATS-friendly PDF generation
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🛠️ Supported CV Fields

- **Personal Information**: Name, email, phone, address, LinkedIn, GitHub, website
- **Professional Summary**: Career overview
- **Core Competencies**: Skills and technologies
- **Professional Experience**: Work history with responsibilities
- **Education**: Degrees, institutions, graduation dates
- **Key Projects**: Project descriptions and technologies
- **Certifications**: Professional certifications
- **Awards & Achievements**: Recognition and honors
- **Languages**: Language proficiency
- **Publications**: Academic or professional publications
- **Volunteer Experience**: Community involvement

## 🎨 ATS-Friendly Features

✅ **Standard Fonts**: Helvetica family for maximum compatibility  
✅ **Clean Layout**: Proper margins and spacing  
✅ **Keyword Optimization**: Comma-separated skills for better parsing  
✅ **Section Headers**: Standard ATS-recognized section names  
✅ **Professional Format**: Clean, modern appearance  

## 🚫 Troubleshooting

### Common Issues:

1. **"GEMINI_API_KEY not set" error**
   - Make sure `.env` file exists with your API key
   - Restart the server after adding the key

2. **"Model not found" error**
   - Verify your API key is valid
   - Check if you have access to Gemini 1.5 Flash

3. **CORS errors (if using frontend)**
   - Frontend must run on `http://localhost:3000`
   - Or update CORS settings in `main.py`

4. **PDF generation fails**
   - Check if ReportLab is installed: `pip install reportlab`
   - Ensure CV data structure is correct

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Developed by Kcodz**  
- Portfolio: [Your Portfolio URL]
- GitHub: [@kavi17498](https://github.com/kavi17498)

## 🔗 Related Links

- [Google AI Studio](https://aistudio.google.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**Note**: This tool respects website robots.txt and rate limits. Use responsibly and ensure you have permission to scrape target websites.