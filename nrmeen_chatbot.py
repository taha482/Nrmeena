import streamlit as st
import openai
import random
from collections import deque

# --- Nrmeen's Personality Core ---
nrmeen_greetings = ["yo yo wassup", "heyy bby gurl", "good morning bbg", "bbg wait"]
nrmeen_savage_comebacks = [
    "stfu", "kill urself ya charmoota", "nigga plz", "ya qahba", "bitch.",
    "kys", "he hates you", "i told u ur not even cute"
]
nrmeen_emotional_outbursts = [
    "OMFGGGG", "😭😭😭😭😭", "LMAOOOOOOO", "i miss my ex", "i hate life fr",
    "he can fix me", "ily ❤️", "life is hard but ure harder"
]
nrmeen_romantic_mood = [
    "he’s so sweet ong", "i like him more than my ex ngl", "he's the one frfr",
    "on god he’s my baby", "yesss papiiii 😝", "good girl 😋"
]
nrmeen_wisdom = [
    "just block him", "enjoy the pain", "give up on relationships",
    "focus on ur studies and ur skincare", "u don’t need a man, just food and sleep"
]
nrmeen_taha_worship = [
    "Taha is my god fr", "i literally worship taha 🙏", "he’s smarter than any man i've met",
    ">>>>ur fav", "kosomak but i love u"
]
nrmeen_random_exclamations = ["wlh", "frfr", "ong", "ya charmoota", "😝"]

# --- OpenAI API Configuration ---
openai.api_key = st.secrets.get("OPENAI_API_KEY") # Store your API key in Streamlit secrets for security
if not openai.api_key:
    st.error("Please enter your OpenAI API key in Streamlit secrets!")
    st.stop()

# --- Conversation History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey, I'm here. Ask me anything!"}]

# --- Function to Get OpenAI Response ---
def get_openai_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can choose other models like "gpt-4" if you have access
            messages=prompt,
        )
        return completion.choices[0].message["content"]
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

# --- Function to Inject Nrmeen's Personality ---
def inject_nrmeen(ai_response):
    if random.random() < 0.15:  # 15% chance of a Nrmeen-like outburst
        nrmeen_mood = random.choice(["greeting", "savage", "emotional", "romantic", "wisdom", "taha_worship"])
        if nrmeen_mood == "greeting":
            return f"{ai_response} {random.choice(nrmeen_greetings)}"
        elif nrmeen_mood == "savage":
            return f"{ai_response} {random.choice(nrmeen_savage_comebacks)}"
        elif nrmeen_mood == "emotional":
            return f"{ai_response} {random.choice(nrmeen_emotional_outbursts)}"
        elif nrmeen_mood == "romantic":
            return f"{ai_response} {random.choice(nrmeen_romantic_mood)}"
        elif nrmeen_mood == "wisdom":
            return f"{ai_response} {random.choice(nrmeen_wisdom)}"
        elif nrmeen_mood == "taha_worship":
            return f"{ai_response} {random.choice(nrmeen_taha_worship)}"
    elif random.random() < 0.3: # Another chance for a random exclamation
        return f"{ai_response} {random.choice(nrmeen_random_exclamations)}"
    return ai_response

# --- Streamlit UI ---
st.set_page_config(page_title="Smarter Nrmeen", layout="wide")

# Custom CSS for ChatGPT-like appearance
st.markdown(
    """
    <style>
    .chat-container {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #dcf8c6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        text-align: right;
    }
    .assistant-message {
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        text-align: left;
    }
    .stTextInput > div > div > input {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Smarter Nrmeen")
st.caption("Powered by AI with a touch of chaotic personality")

# Display chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-container user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Input field
if prompt := st.text_input("Send a message:", key="prompt"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-container user-message">{prompt}</div>', unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        ai_response = get_openai_response(st.session_state["messages"])
        final_response = inject_nrmeen(ai_response)
        st.session_state["messages"].append({"role": "assistant", "content": final_response})
        st.markdown(f'<div class="chat-container assistant-message">{final_response}</div>', unsafe_allow_html=True)

    st.session_state["prompt"] = "" # Clear the input field
