# AI Pitch Analysis

## Overview
AI Pitch Analysis is a Flask web application designed to assist entrepreneurs and startups in refining their pitch decks. Users can upload a PDF pitch deck, which the application processes to extract text and analyze the content using OpenAI's API. The goal is to provide actionable feedback that can help improve the quality and effectiveness of the pitch.

## Features
- **Upload a pitch deck in PDF format**: Users can easily upload their pitch decks for analysis.
- **AI-powered feedback on the pitch**: The application leverages OpenAI's API to provide insights and suggestions based on the content of the pitch.
- **User-friendly interface with Bootstrap styling**: The application is designed to be intuitive and easy to navigate, ensuring a smooth user experience.

## Requirements
- **Python 3.x**: Ensure you have Python installed on your system.
- **Flask**: A lightweight WSGI web application framework.
- **OpenAI API**: Access to OpenAI's API for generating feedback.
- **pdfplumber**: A library for extracting text from PDF files.
- **dotenv**: A module to load environment variables from a `.env` file.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kanchan-1010/AI_Pitch_Analysis.git
   cd AI_Pitch_Analysis
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables in a `.env` file**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

   Make sure to replace `your_openai_api_key` with your actual OpenAI API key.

## Usage and CSV Analysis
1. **Run the application** and analyze a pitch deck:
   ```bash
   python app.py
   ```

2. **Open your web browser and go to** `http://127.0.0.1:5000`.

3. **Upload your pitch deck PDF** and click "Analyze Pitch" to receive feedback. The application will process the document and provide insights based on the content.

4. **To analyze a CSV file**:
   - Ensure your CSV file is formatted correctly with columns for `name` and `description`.
   - Navigate to the application and follow the prompts to upload your CSV file for analysis.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as long as you include the original license in any copies of the software.
