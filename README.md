# 📝 NLP Text Summarization & Q&A

A Streamlit web application that can:
- Summarize long texts into concise summaries.
- Answer user questions based on the provided text or uploaded document.

## 🚀 Features
- **Summarization** using `sshleifer/distilbart-cnn-12-6`.
- **Question Answering** using `deepset/roberta-base-squad2`.
- Supports **.txt** and **.pdf** uploads.
- Splits large documents into chunks for better processing.
- Shows **confidence score** and source text for each answer.

## 📂 Project Structure

├── app.py   # Main application code

├── requirements.txt    # Required Python packages

├── README.md   # Project documentation

└── .gitignore   # Ignored files (optional)


## 🛠 Installation

1. **Clone the repository**
```bash
git clone https://github.com/MohamedMostafa404/nlp_text_summarization_q-a.git
cd nlp_text_summarization_q-a

```
2.Install dependencies

```bash
pip install -r requirements.txt
 ```
3.Run the application

```bash
streamlit run app.py

```

📦 Requirements
Main dependencies:

streamlit

transformers

PyPDF2

torch

Full list in requirements.txt.

---------------------------------------------------------------------------------------------

📄 Example Usage
1.Paste your text or upload a .txt or .pdf file.

2.Click Summarize to get a concise version of the text.

3.Ask a question related to the text to get an answer with a confidence score.

---------------------------------------------------------------------------------------------
👨‍💻 Author

Mohamed Mostafa







