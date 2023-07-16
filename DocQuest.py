# download each lib using pip first
# import lib
import streamlit as st
from streamlit_lottie import st_lottie
import PyPDF2
import io
import openai
import docx2txt
import pyperclip

# Title
st.title("DocQuest")
# key here
openai.api_key = st.sidebar.text_input("Enter your OpenAi Api key", type="password")

#sidebar info paragraph
# Add a hyperlink with target website
st.sidebar.markdown("# Copyright©2023 All rights reserved | Made by [Umar Nadeem](https://umar-cs.netlify.app/)")

st.sidebar.write("Welcome, this app allows you to upload a document and ask questions or queries from our deployed model. It leverages the power of LLM processing to understand the context of the document and provide relevant answers to your questions.")

st.sidebar.write("To use the app, follow these steps:")
st.sidebar.write("1. Enter your Api Key and upload your document.")
st.sidebar.write("2. Once the document is uploaded, you can enter your questions or queries in the input box provided.")
st.sidebar.write("3. Click on the 'Enter' button to submit your query to the model.")
st.sidebar.write("4. The model will process your question and provide the most relevant answer from the document.")
st.sidebar.write("5. You can ask multiple questions and explore the document by repeating the above steps.")

st.sidebar.write("Please note that the performance of the model may vary based on the complexity of the document and the nature of the questions. Feel free to experiment with different documents and queries to get the best results.")

st.sidebar.write("I hope you find this app useful and enjoy exploring your documents with my question answering model!")


def extract_text_from_pdf(file):
    # bytes io obj from file uploaded
    pdf_file = io.BytesIO(file.read())
    # pdf reader obj
    reader = PyPDF2.PdfReader(pdf_file)
    # empty string to store extracted text data
    txt = ""
    # loop to extract text from page to page till last word from doc
    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        try:
            txt += page.extract_text()
        except UnicodeDecodeError:
            # Try different encodings if UTF-8 fails
            encodings = ['utf-8', 'latin-1']
            for encoding in encodings:
                try:
                    txt += page.extract_text(encoding=encoding)
                    break
                except UnicodeDecodeError:
                    pass
    # ret extracted txt
    return txt


# Defining a fun to extract txt from word file
def extract_text_from_docx(file):
    # byte IO obj
    docx_file = io.BytesIO(file.read())
    # Extracting txt
    txt = docx2txt.process(docx_file)
    # ret txt
    return txt


# Defining a fun to extract txt from txt file
def extract_text_from_txt(file):
    # reading file as txt
    txt = file.read().decode('utf-8')
    # ret txt
    return txt


# Defining a function to extract text from a file based on its type
def extract_text_from_file(file):
    # Checking the type of the uploaded file
    if file.type == "application/pdf":
        # Extracting text from the PDF file
        txt = extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        txt = extract_text_from_docx(file)
    elif file.type == "text/plain":
        txt = extract_text_from_txt(file)
    # Extracting text from the Text file
    else:
        st.error("Unsupported file type!")
        txt = None
    # Returning the extracted text
    return txt


# defining fun to get gen questions for gpt-3 using txt
def gen_question(txt):
    # select first 4096 char from txt as prompt for Api
    prompt = txt[:4096]
    # generating question
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=30)
    # ret question
    return response.choices[0].text.strip()


# defining fun to get response from gpt-3 using txt
def gen_response(txt, question):
    # select first 4096 char from txt as prompt for Api along question
    prompt = txt[:4096] + '\n Question:' + question + '\n Answer:'
    # generating response
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.6, max_tokens=2000)
    # ret response
    return response.choices[0].text.strip()


def main():
    # Setting the title of the app
    st.title("Ask Questions From Your Uploaded Documents")
    
    #Animation
# CSS styles to hide details and set margins to zero
    styles = """
    <style>
    details {
     display: none;
    }

    .stLottie {
     margin: 0;
    }
    </style>
    """

# Render the CSS styles
    st.markdown(styles, unsafe_allow_html=True)

# Lottie animation
    st_lottie("https://lottie.host/f29860a6-469b-424a-9bb6-8cd55af735a3/F3dCJ28GS4.json",height=200,width=None,speed=1.5)
    
    # Creating a file uploader for PDF, Word, and Text files
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    # Checking if a file has been uploaded
    if uploaded_file is not None:
        # Extracting text from the uploaded file
        txt = extract_text_from_file(uploaded_file)

        # Checking if text was extracted successfully
        if txt is not None:
            # Generating a question from the extracted text using GPT-3
            
           # question = gen_question(txt)

            # Displaying the generated question
            
            #st.write("Question: " + question )

            # Creating a text input for the user to ask a question
            user_question = st.text_input("Ask a question about the document")

            # Checking if the user has asked a question
            if user_question:
                # Generating an answer to the user's question using GPT-3
                answer = gen_response(txt, user_question)

                # Displaying the generated answer
                st.write("Answer: " + answer)

                # Creating a button to copy the answer text to clipboard
                if st.button("Copy Answer Text"):
                    pyperclip.copy(answer)
                    st.success("Answer text copied to clipboard!")


# calling Main fun
if __name__ == "__main__":
    main()
