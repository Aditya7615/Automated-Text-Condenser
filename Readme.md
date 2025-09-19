Automated Text Summarization Engine
1. Overview
This project is a Natural Language Processing (NLP) application designed to generate concise, abstractive summaries from text-based content. It provides an intuitive web interface to condense information from web articles and PDF documents, making it an effective tool for rapid information extraction and analysis.

The core of the application leverages a pre-trained T5 (Text-to-Text Transfer Transformer) model to ensure high-quality, human-readable summaries.

2. Key Features
Web Article Summarization: Extracts text content directly from a provided URL and generates a summary.
PDF Document Summarization: Allows users to upload a PDF file and receive a condensed version of its content.
Interactive UI: A clean and user-friendly interface built with Streamlit for seamless interaction.
3. Technology Stack
The project is built using the following core technologies:
Backend: Python 3.9
NLP Model: T5-small (from Hugging Face Transformers)
Web Framework: Streamlit
Data Extraction:
BeautifulSoup4 & Requests (for URL content)
PyPDF2 (for PDF content)
4. System Architecture
The application follows a straightforward data processing workflow:
Input: The user selects an input source (URL or PDF file) via the Streamlit interface.
Text Extraction: Based on the source, the appropriate module scrapes the web page or parses the PDF to extract the raw text.
Summarization: The extracted text is tokenized and fed into the T5 transformer model, which generates the abstractive summary.
Output: The application displays both the original extracted text and the final summary for comparison.
5. Local Installation and Usage
To run this project on your local machine, please follow the steps below.

Prerequisites
Python 3.9 or higher
pip package installer
Setup Instructions
Clone the Repository
Bash
git clone https://github.com/Aditya7615/NLP-Project.git
cd NLP-Project
Create and Activate a Virtual Environment (Recommended)
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies
Install all required packages from the requirements.txt file.
Bash
pip install -r requirements.txt
Launch the Application
Run the Streamlit server.
Bash
streamlit run app.py
The application will be accessible at http://localhost:8501 in your web browser.
6. License
This project is distributed under the MIT License. See the LICENSE file for more details.
