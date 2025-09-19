QuickSum: Automated Text Summarizer
An NLP-powered web app to quickly summarize articles and documents from URLs or PDF files using the T5 transformer model.

![QuickSum Demo GIF]
(Consider adding a screenshot or a GIF of your application in action here)

✨ Features
URL Summarization: Provide a link to any article, and the app will extract the text and generate a concise summary.
PDF Summarization: Upload a PDF document directly from your computer to get a summary of its content.
Simple Web Interface: Built with Streamlit for a clean, interactive, and easy-to-use experience.
🛠️ Technologies Used
This project leverages a modern stack of NLP and web app technologies:
Backend: Python
NLP Model: Google's T5 (Text-to-Text Transfer Transformer) via Hugging Face Transformers
Web Framework: Streamlit
Web Scraping: BeautifulSoup4, Requests
PDF Processing: PyPDF2
🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Python 3.9 or higher
pip package manager
Installation & Setup
Clone the repository:
Bash
git clone https://github.com/Aditya7615/NLP-Project.git
cd NLP-Project
Create a virtual environment (recommended):
Bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:
The requirements.txt file contains all the necessary packages.
Bash
pip install -r requirements.txt
Run the Streamlit application:
Bash
streamlit run app.py
Your browser should automatically open to the web application's local address (usually http://localhost:8501).

💻 How to Use
Once the application is running:
Choose an option: Select either "Summarize from URL" or "Summarize from PDF" from the sidebar.
For URL: Paste the full URL of the article you want to summarize into the text box and click "Summarize".
For PDF: Click the "Browse files" button, select a PDF from your computer, and the summary will be generated automatically.
View the original and summarized text side-by-side.
📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.
