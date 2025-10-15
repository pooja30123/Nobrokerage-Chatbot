# NoBrokerage Property Search Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered property search chatbot for NoBrokerage.com that understands natural language queries (e.g., "3BHK flat in Pune under ₹1.2 Cr"), extracts filters, searches local CSV data, and responds with data-grounded summaries and relevant property cards.

![NoBrokerage Chatbot](image.jpg)

## 🔧 Overview

This intelligent chatbot transforms property search from a filter-based experience to a conversational one. Instead of selecting multiple filters, users can simply type queries like natural language and get instant, relevant property recommendations.

The system parses natural language to extract key filters, searches through real property data, and generates AI-powered summaries - all without any hallucination or external data sources.

## ✨ Features

- **Natural Language Search**: Understands queries like "3BHK flat in Pune under ₹1.2 Cr"
- **Smart Filter Extraction**: Automatically identifies BHK, budget, location, and status
- **AI-Powered Summaries**: Provides concise, data-grounded property summaries
- **Property Cards**: Displays detailed property information with full address
- **Graceful Error Handling**: Provides helpful guidance for invalid queries
- **Zero Brokerage Philosophy**: Aligned with NoBrokerage.com's mission

## 🚀 Demo

**Live Demo**: [https://pooja30123-nobrokerage-chatbot-streamlit-app-uxn5rs.streamlit.app/](https://pooja30123-nobrokerage-chatbot-streamlit-app-uxn5rs.streamlit.app/)

## 🏗️ Architecture
```
User Query → Query Parser → Filter Extraction → Data Search → Summary Generation → Response
```

**Components:**
- **Frontend**: Streamlit chat interface
- **Backend**: Python-based NLP and search engine
- **Database**: Local CSV files (no external APIs)
- **AI**: Google Gemini for natural language summarization
- **Search**: Rule-based filtering with pandas DataFrames

## 📥 Setup & Installation

### 1. Prerequisites
- Python 3.8+
- Git
- Google Gemini API Key

### 2. Installation
```bash
Clone the repository
git clone https://github.com/pooja30123/Nobrokerage-Chatbot.git
cd Nobrokerage-Chatbot

Create virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
```bash
Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 4. Data Preparation
The application expects the following CSV files in the root directory:
- `project.csv` - Project information
- `ProjectAddress.csv` - Address details  
- `ProjectConfiguration.csv` - Property configurations
- `ProjectConfigurationVariant.csv` - Price and area variants

### 5. Run the Application
```bash
streamlit run app.py
```

## 🎯 Usage Examples

Ask questions like:
```
"2BHK under 1 crore"
"1BHK in Chembur"
"3BHK ready to move"
"Flat near Lodha Xperia Mall"
"Properties with 4 bathrooms"
"Flats in Borivali"
```

The chatbot will extract filters, search properties, and provide a summary with matching property cards.

## 📊 Query Understanding

The system can parse:
- **BHK Types**: 1BHK, 2BHK, 3BHK, RK, etc.
- **Budget**: "under ₹1.2 Cr", "below 50 lakh", "within 2 crore"
- **Locations**: Cities (Mumbai, Pune) and localities (Borivali, Chembur)
- **Status**: "ready to move", "under construction"
- **Other Filters**: Bathrooms, project names, landmarks

## 📦 Project Structure
```
Nobrokerage-chatbot/
├── project.csv # Project information
├── ProjectAddress.csv # Address details
├── ProjectConfiguration.csv # Property configurations
├── ProjectConfigurationVariant.csv # Price and area variants
├── app.py # Streamlit frontend
├── backend/
│ ├── data_processor.py # Data loading and processing
│ ├── query_parser.py # Natural language parsing
│ ├── search_engine.py # Property search functionality
│ └── summarizer.py # AI summary generation
├── requirements.txt # Dependencies
├── .env.example # Environment variables template
├── .gitignore # Git ignore rules
└── README.md # This file
```

## 📋 Dependencies

- streamlit==1.24.0
- pandas==2.0.3
- google-generativeai==0.3.1
- python-dotenv==1.0.0

Install with:
```bash
pip install -r requirements.txt
```

## 🛡️ Environment Variables

Create a `.env` file with:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## 🌐 Deployment

To deploy on Streamlit Community Cloud:
1. Push your code to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Sign in with GitHub
4. Create a new app
5. Select your repository
6. Set the main file path: `app.py`
7. Deploy!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Support

For issues and feature requests, please open an issue on GitHub.

## 🎯 Why This Implementation Stands Out

1. **Advanced NLP**: Goes beyond simple keyword matching with comprehensive rule-based parsing
2. **Data Integrity**: All responses are grounded in actual CSV data - no hallucination
3. **User Experience**: Conversational interface with helpful guidance for invalid queries
4. **Transparency**: Shows full property addresses for verification
5. **Production Ready**: Clean code, proper error handling, and professional UI

This solution transforms property search from a tedious filter-based process to an intuitive conversation, helping users find their dream homes faster and more naturally.

