from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import pytesseract  # Importing Tesseract for OCR
from PIL import Image  # Importing PIL for image handling

import openai
import pandas as pd  # Importing pandas for CSV handling
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

@app.route('/analyze_csv', methods=['GET'])
def analyze_csv():
    # Read the CSV file
    csv_file_path = 'pitchleague_270220241436.csv'
    data = pd.read_csv(csv_file_path)
    
    feedbacks = []  # List to store feedback for each startup

    for index, row in data.iterrows():
        startup_description = row['description']  # Assuming 'description' is a column in the CSV
        if pd.isna(startup_description) or startup_description.strip() == "":
            feedback = "No description provided."
        else:
            feedback = analyze_pitch_gpt(startup_description)

        feedbacks.append({'name': row['name'], 'feedback': feedback})  # Assuming 'name' is a column in the CSV
    
    return render_template('result.html', feedbacks=feedbacks, title="CSV Analysis Feedback")


def analyze_pitch_gpt(description):
    """Uses OpenAI Gemini to analyze pitch and provide feedback.
    
    This function identifies key sections of the pitch, assigns weights, 
    and calculates a score based on clarity, depth, and uniqueness.
    It also provides strengths and weaknesses along with suggestions.
    """ 
    sections = {
        "Problem": {"weight": 0.25, "score": 0},
        "Solution": {"weight": 0.25, "score": 0},
        "Market": {"weight": 0.2, "score": 0},
        "Business Model": {"weight": 0.1, "score": 0},
        "Financials": {"weight": 0.1, "score": 0},
        "Team": {"weight": 0.05, "score": 0},
        "Unique Value Proposition": {"weight": 0.05, "score": 0}
    }

    try:
        # Analyze each section and calculate scores
        # This section uses the OpenAI API to get feedback for each part of the pitch.
        for section in sections.keys():
            section_feedback = client.chat.completions.create(
                model="gemini",
                messages=[
                    {"role": "system", "content": f"You are an expert in startup pitch analysis. Analyze the {section} section."},
                    {"role": "user", "content": f"Analyze this section: {description}"}
                ]
            )
            sections[section]["score"] = evaluate_section(section_feedback.choices[0].message.content)
        
        total_score = sum(sections[section]["score"] * sections[section]["weight"] for section in sections if sections[section]["weight"] > 0)

        strengths = identify_strengths(sections)
        weaknesses = identify_weaknesses(sections)
        
        feedback_summary = f"Total Score: {total_score:.2f}/100\nStrengths: {strengths}\nWeaknesses: {weaknesses}\n"
        
        # Provide personalized feedback
        feedback_summary += "Suggestions for Improvement:\n"
        for section, data in sections.items():
            if data["score"] < 70:
                feedback_summary += f"- Improve the {section} section. Consider adding more details or clarifying your points.\n"

        return feedback_summary

    except Exception as e:
        return f"Error: {e}"

def evaluate_section(feedback):
    """Evaluate the section feedback and return a score based on clarity, depth, and uniqueness.
    
    This function currently returns a placeholder score of 75, but it can be enhanced
    to include more sophisticated scoring logic based on the feedback received.
    """
    return 75  # Example score

def identify_strengths(sections):
    """Identify strengths based on the analyzed sections."""
    return ", ".join([section for section, data in sections.items() if data["score"] > 70])

def identify_weaknesses(sections):
    """Identify weaknesses based on the analyzed sections."""
    return ", ".join([section for section, data in sections.items() if data["score"] <= 70])

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file, using OCR if necessary."""
    text = ""
    # Check if the PDF is scanned or empty
    if not text.strip():
        # Use OCR to extract text from images in the PDF
        text = extract_text_with_ocr(pdf_file)

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"Error extracting text: {e}"

    return text.strip() if text.strip() else "No text extracted from PDF."

def extract_text_with_ocr(pdf_file):
    """Extract text from images in the PDF using OCR."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # Convert PDF page to image
                page_image = page.to_image()
                # Use OCR to extract text from the image
                page_text = pytesseract.image_to_string(page_image.original)
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"Error extracting text with OCR: {e}"
    
    return text.strip() if text.strip() else "No text extracted from images."

if __name__ == '__main__':
    app.run(debug=True)
