import streamlit as st
import random
from collections import deque

# --- Nrmeen Chmkara's Personality Core ---
greetings = ["yo yo wassup", "heyy bby gurl", "good morning bbg", "bbg wait"]
savage_comebacks = [
    "stfu", "kill urself ya charmoota", "nigga plz", "ya qahba", "bitch.",
    "kys taha", "he hates you", "i told u ur not even cute"
]
emotional_outbursts = [
    "OMFGGGG", "😭😭😭😭😭", "LMAOOOOOOO", "i miss my ex", "i hate life fr",
    "he can fix me", "taha ily ❤️", "life is hard but ure harder"
]
romantic_mood = [
    "he’s so sweet ong", "i like him more than my ex ngl", "he's the one frfr",
    "on god he’s my baby", "yesss papiiii 😝", "good girl 😋"
]
wisdom = [
    "just block him", "enjoy the pain", "give up on relationships",
    "focus on ur studies and ur skincare", "u don’t need a man, just food and sleep"
]
taha_worship = [
    "Taha is my god fr", "i literally worship taha 🙏", "he’s smarter than any man i've met",
    "Taha>>>>ur fav", "kosomak taha but i love u"
]

# Memory for conversation context
context = deque(maxlen=6)

# Mood detection
def detect_mood(user_input, previous_mood=None):
    lowered = user_input.lower()

    if "taha" in lowered:
        return "taha_worship"
    elif any(word in lowered for word in ["sweet", "like", "love", "good", "happy", "adore"]):
        return "soft"
    elif any(word in lowered for word in ["stfu", "kill", "hate", "sad", "cry", "miss", "bad", "angry"]):
        return "savage"
    elif any(word in lowered for word in ["omg", "miss", "hate", "life", "ily"]):
        return "emotional"
    elif any(word in lowered for word in ["hi", "hello", "wassup"]):
        return "greeting"
    elif previous_mood:
        if random.random() < 0.7:
            return previous_mood
        else:
            moods = ["savage", "soft", "emotional", "romantic", "wisdom", "taha_worship"]
            if previous_mood in moods:
                moods.remove(previous_mood)
            return random.choice(moods)
    else:
        moods = ["savage", "soft", "emotional", "romantic", "wisdom", "taha_worship"]
        return random.choice(moods)

# Response generation
def generate_response(user_input, current_mood):
    lowered = user_input.lower()
    context.append(f"You: {user_input}")
    response = ""

    if current_mood == "savage":
        response = random.choice(savage_comebacks)
    elif current_mood == "soft":
        response = random.choice(romantic_mood + greetings)
    elif current_mood == "emotional":
        response = random.choice(emotional_outbursts + wisdom)
    elif current_mood == "romantic":
        response = random.choice(romantic_mood + taha_worship)
    elif current_mood == "wisdom":
        response = random.choice(wisdom)
    elif current_mood == "taha_worship":
        response = random.choice(taha_worship)
    elif current_mood == "greeting":
        response = random.choice(greetings)
    else:
        response = random.choice(greetings + savage_comebacks + emotional_outbursts + romantic_mood + wisdom + taha_worship)

    if "taha" in lowered and current_mood != "taha_worship":
        response = random.choice(taha_worship)
    elif any(w in lowered for w in ["sad", "cry", "miss"]) and current_mood != "emotional":
        response += " 😭"
    elif any(w in lowered for w in ["hi", "hello", "wassup"]) and current_mood != "greeting":
        response = random.choice(greetings)

    if random.random() < 0.3:
        response += " " + random.choice(["wlh", "frfr", "ong", "ya charmoota", "😝"])

    context.append(f"Nrmeen Chmkara: {response}")
    return response

# --- Streamlit UI (ChatGPT-like Design) ---
st.set_page_config(page_title="Nrmeen Chmkara", layout="wide")

# Custom CSS for ChatGPT-like appearance
st.markdown(
    """
    <style>
    body {
        background-color: #343541;
        color: #d1d5db;
        font-family: sans-serif;
    }
    .stApp {
        max-width: 960px;
        margin: 0 auto;
        padding-top: 20px;
    }
    .chat-container {
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 8px;
        overflow-wrap: break-word;
    }
    .user-message {
        background-color: #444654;
        text-align: right;
    }
    .assistant-message {
        background-color: #434a54;
        text-align: left;
    }
    .stTextInput > div > div > input {
        background-color: #40414f !important;
        color: #d1d5db !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-top: 20px !important;
        margin-bottom: 30px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #8e8ea0 !important;
    }
    .stButton {
        display: none !important; /* Hide the default button */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Nrmeen Chmkara")
st.caption("Powered by chaotic code and Taha's influence")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_mood" not in st.session_state:
    st.session_state.current_mood = None

# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f'<div class="chat-container user-message">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container assistant-message">{message}</div>', unsafe_allow_html=True)

# Input field at the bottom
prompt = st.text_input("Send a message:", key="prompt", placeholder="Send a message")

if prompt:
    current_mood = detect_mood(prompt, st.session_state.current_mood)
    reply = generate_response(prompt, current_mood)
    st.session_state.chat_history.append(("You", prompt))
    st.session_state.chat_history.append(("Nrmeen Chmkara", reply))
    st.session_state.current_mood = current_mood
    st.session_state["prompt"] = "" # Clear the input
