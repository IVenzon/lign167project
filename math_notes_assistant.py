import streamlit as st
from openai import OpenAI
import PyPDF2

# Initialize OpenAI client
client = OpenAI(api_key="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")

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def summarize_large_notes(notes_text):
    """Summarize large notes using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant summarizing lecture notes."},
                {"role": "user", "content": f"Summarize these notes: {notes_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def answer_question(notes_text, question):
    """Answer a question using the uploaded notes."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions about lecture notes."},
                {"role": "user", "content": f"Based on these notes: {notes_text}, answer this question: {question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("📚 Math Notes Assistant")
st.write("Upload your notes, summarize, and ask questions interactively.")

# Initialize session state variables
if "notes_text" not in st.session_state:
    st.session_state["notes_text"] = ""
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "answer" not in st.session_state:
    st.session_state["answer"] = ""

# File Upload
uploaded_file = st.file_uploader("Upload a PDF or Text file", type=["pdf", "txt"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        st.session_state["notes_text"] = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        st.session_state["notes_text"] = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully!")

# Summarization Section
st.subheader("📝 Summarization")
if st.session_state["notes_text"]:
    if st.button("Summarize Notes"):
        st.session_state["summary"] = summarize_large_notes(st.session_state["notes_text"])
        st.success("Summary generated successfully!")
    if st.session_state["summary"]:  # Persist and render the summary
        st.markdown("### 📋 Summary Output")
        st.markdown(st.session_state["summary"], unsafe_allow_html=True)
else:
    st.info("Upload a file and click 'Summarize Notes' to generate a summary.")

# Question Answering Section
st.subheader("❓ Ask a Question")
question = st.text_input("Enter your question:")
if st.session_state["notes_text"] and question:
    if st.button("Ask"):
        # Use the summary if available, otherwise use the full notes
        source_text = st.session_state["summary"] if st.session_state["summary"] else st.session_state["notes_text"]
        st.session_state["answer"] = answer_question(source_text, question)
    if st.session_state["answer"]:  # Persist and render the answer
        st.markdown("### 💬 Answer Output")
        st.markdown(st.session_state["answer"], unsafe_allow_html=True)
else:
    st.info("Upload a file and enter a question to get an answer.")

# Footer
st.markdown("---")
st.markdown("🔗 Powered by OpenAI and Streamlit | Created for Math Notes Analysis.")
