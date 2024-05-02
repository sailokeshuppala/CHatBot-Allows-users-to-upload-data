import streamlit as st
import pandas as pd
import PyPDF2
import google.generativeai as genai
import re
import string

# Function to preprocess text data
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to preprocess CSV data
def preprocess_csv(csv_file):
    df = pd.read_csv(csv_file)
    # Concatenate text columns into a single string
    text = ' '.join(df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1))
    # Preprocess text
    text = preprocess_text(text)
    return text

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    # Preprocess text
    text = preprocess_text(text)
    return text

# Main function
def main():
    st.title("Data-Based Question Answering Chatbot")

    # Data upload options
    data_type = st.radio("Upload Data Type:", ("PDF", "CSV"))

    if data_type == "PDF":
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
    else:  # CSV
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file:
            text = preprocess_csv(uploaded_file)

    if uploaded_file:
        # User input for question
        question = st.text_input("Enter your question: ")

        if st.button("Ask"):
            # Combine context and question
            context = text + "\n\n" + question

            # Retrieve API key from file
            with open(".gemini_api.txt", "r") as file:
                api_key = file.read()

            # Configure gemini
            genai.configure(api_key=api_key)

            # Use gemini for question answering
            response = genai.GenerativeModel(model_name="gemini-1.5-pro-latest").generate_content(context)

            # Extract answer from response
            answer = response.text.strip()

            # Display answer
            st.write("Answer:")
            st.write(answer)


if __name__ == "__main__":
    main()
