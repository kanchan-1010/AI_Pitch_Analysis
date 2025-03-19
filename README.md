# AI Pitch Analysis

## Overview
AI Pitch Analysis is a Flask web application that allows users to upload a PDF pitch deck, extracts text from it, and analyzes the pitch using OpenAI's API.

## Features
- Upload a pitch deck in PDF format.
- AI-powered feedback on the pitch.
- User-friendly interface with Bootstrap styling.

## Requirements
- Python 3.x
- Flask
- OpenAI API
- pdfplumber
- dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kanchan-1010/AI_Pitch_Analysis.git
   cd AI_Pitch_Analysis
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage
1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Upload your pitch deck PDF and click "Analyze Pitch" to receive feedback.

## License
This project is licensed under the MIT License.
