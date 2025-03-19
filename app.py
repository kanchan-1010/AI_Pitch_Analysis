from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import openai
load_dotenv()

import pdfplumber

app = Flask(__name__)

# Set OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"OpenAI API Key: {OPENAI_API_KEY}")  # Debugging line to check the API key
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'pdf_file' not in request.files:
        return redirect(request.url)
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return redirect(request.url)
    
    pitch_text = extract_text_from_pdf(pdf_file)
    feedback = analyze_pitch_gpt(pitch_text)
    return render_template('result.html', feedback=feedback)

def analyze_pitch_gpt(description):
    """Uses OpenAI Gemini to analyze pitch and provide feedback."""
    try:
        response = client.chat.completions.create(
            model="gemini",
            messages=[
                {"role": "system", "content": "You are an expert in startup pitch analysis."},
                {"role": "user", "content": f"Analyze this startup pitch: {description}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text if text.strip() else "No text extracted from PDF."
    except Exception as e:
        return f"Error extracting text: {e}"

if __name__ == '__main__':
    app.run(debug=True)
