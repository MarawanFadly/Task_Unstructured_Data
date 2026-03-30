from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Explain the importance of fast language models",
    model="openai/gpt-oss-20b",
)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #D8D45D;
</style>
""", unsafe_allow_html=True)
st.title("🧠 Data Extraction Chatbot")

## Texts

st.markdown(
    "<h3>Paste any messy or unstructured text (receipts, notes or transcriptions), and get a clean Python dictionary:</h3>",
    unsafe_allow_html=True
)

st.markdown("""
- Returns only structured data
- Automatically detects fields (date, items, total,etc.)
- Handles missing or uncertain values 
- Normalizes numbers and formats output
""")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
st.markdown(
    "<h5>Enter your text below 👇",
    unsafe_allow_html=True
)

st.markdown("""
Paste your Unstructured text here:
""")
prompt = st.text_area("Ask something...")

if st.button("Apply"):
    st.write("Apply")


if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response from model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Groq model
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    
    # ---- Parsing logic ----
def parse_text_to_dict(text):
    """
    Example parser: extracts key-value pairs from messy text.
    You can customize this based on your text format.
    """
    data_dict = {}
    lines = text.split("\n")
    
    for line in lines:
        # remove extra spaces
        line = line.strip()
        if not line:
            continue

        # try to split key:value format
        if ":" in line:
            key, value = line.split(":", 1)
            data_dict[key.strip()] = value.strip()
        else:
            # fallback: store lines as numbered keys
            data_dict[f"line_{len(data_dict)+1}"] = line

    return data_dict

# ---- Generate dictionary ----
if prompt:
    parsed_dict = parse_text_to_dict(prompt)
    st.markdown("# Dictionary:")
    st.write(parsed_dict)
