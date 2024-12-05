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

def summarize_large_notes(notes_text, lod):
    """Summarize large notes using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant summarizing lecture notes."},
                {"role": "user", "content": f"Summarize these notes: {notes_text}. On a scale of 1 to 10, with 1 being a short and sweet overview and 10 being an intricate, in-depth dive into the material with multiple examples, summarize these notes with a level of detail equaling {lod}"}
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
    
def generate_flashcards(notes_text, previous_flashcards, difficulty):
    """Generate flashcards based on the provided notes."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant which generates five flashcards based on the lecture notes."},
                {"role": "user", "content": f"Create a list of five question-answer pairs based with a difficulty of {difficulty} on the following content:\n\n{notes_text}. Make sure that the questions you ask are appropriate to the difficulty level and are different than the questions contained in {previous_flashcards} if there are any. Format the string as follows: For each question, add a line for the question number (i.e. q1). Then, on the next line, put the question and only the question. The line after that, put the answer and only the answer. Format the string such that there are no extraneous characters, such as triple quotes or 'python' in the string."}
            ]
        )
        flashcard_list = response.choices[0].message.content
        return flashcard_list
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
if "index" not in st.session_state:
    st.session_state["index"] = 0
    st.session_state["show_answer"] = False
if "flashcards" not in st.session_state:
    st.session_state["flashcards"] = {}
if "previous_flashcards" not in st.session_state:
    st.session_state["previous_flashcards"] = {}

# File Upload
st.subheader("📂 Upload Notes")
uploaded_file = st.file_uploader("Upload a PDF or Text file", type=["pdf", "txt"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        st.session_state["notes_text"] = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        st.session_state["notes_text"] = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully!")

tab1, tab2, tab3 = st.tabs(["Summarization", "Question Answering", "Flashcards"])

with tab1:
        # Summarization Section
        st.subheader("📝 Summarization")
        if st.session_state["notes_text"]:
            level_of_detail = st.slider("Select the level of detail for the summary:", 1, 10, 5)
            if st.button("Summarize Notes"):
                st.session_state["summary"] = summarize_large_notes(st.session_state["notes_text"], level_of_detail)
                st.success("Summary generated successfully!")
            if st.session_state["summary"]:  # Persist and render the summary
                st.markdown("### 📋 Summary Output")
                st.markdown(st.session_state["summary"], unsafe_allow_html=True)
        else:
            st.info("Upload a file and click 'Summarize Notes' to generate a summary.")

with tab2:
    # Question Answering Section
    st.subheader("❓ Ask a Question")
    if st.session_state["notes_text"]:
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

with tab3:
    # Flashcards Generation Section
    st.subheader("🧠 Test Yourself with Flashcards")

    if st.session_state['notes_text']:
        # select difficulty level
        difficulty = st.selectbox("Select the difficulty level of the flashcards:", ("Easy", "Medium", "Hard"))
        if st.button("Generate Flashcards"):
            # if flashcards already exist, save them to previous_flashcards
            if st.session_state["flashcards"]:
                st.session_state["previous_flashcards"] = st.session_state["flashcards"]
            # generate new flashcards
            flashcards_string = generate_flashcards(st.session_state["notes_text"], st.session_state['previous_flashcards'], difficulty)
            # process chatgpt output
            flashcards_list = flashcards_string.split('\n')
            flashcard_dict = {}
            ff = [x for x in flashcards_list if x]
            for i in range(0, len(ff), 3):
                flashcard_dict[ff[i]] = (ff[i+1], ff[i+2])
            # save flashcards to session state
            st.session_state["flashcards"] = flashcard_dict
            st.success("Flashcards generated successfully!")
        if st.session_state["flashcards"]:
            # render flashcards
            st.markdown("📇 Your Flashcards:")
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])
            # for key, value in st.session_state["flashcards"].items():
            for tab, (key, value) in zip([tab1, tab2, tab3, tab4, tab5], st.session_state["flashcards"].items()):
                tab.markdown(f"🃏 **{key.upper()}** 🃏")
                tab.markdown(f"**❓ {value[0]}**")
                # Use a checkbox to toggle answer visibility
                checkbox_key = f"show_answer_{key}"
                show_answer = tab.checkbox("Show/Hide Answer", key=checkbox_key)
                if show_answer:
                    tab.markdown(f"**✔️ Answer:** {value[1]}")
    else:
        st.info("Upload a file and click 'Generate Flashcards' to create flashcards.")

# Footer
st.markdown("---")
st.markdown("🔗 Powered by OpenAI and Streamlit | Created for Math Notes Analysis.")
