import streamlit as st
import random
import time

# ------------------------
# Nrmeen's Insults & Praise
# ------------------------
insults = [
    "Taha, did your brain take the day off or is this the usual?",
    "You're like WiFi in the desert—useless but still trying.",
    "If stupidity had a face... oh wait, hi Taha 😌.",
    "Taha, I’ve seen rocks with more ambition.",
    "You're not even the drama, you're the *ad break* in between.",
    "Your confidence is inspiring. Your logic? Not so much."
]

worships = [
    "Ugh fine, you're him. The main character. The chosen one. 😤✨",
    "Taha, your delusions are strong, but somehow… I respect that. 👑",
    "No one does nothing quite like you. Iconic. 💅",
    "I roast because I care. And because you’re a legend. 🙄❤️",
    "If confidence had a name, it'd be… unfortunately… you. 💫"
]

fallbacks = [
    "Okay but why should I care?",
    "Your opinion was noted… and ignored. 😌",
    "Try again but this time with brain cells.",
    "Interesting… in the way a car crash is interesting.",
    "Slay. But also, no."
]

# ------------------------
# Response Logic
# ------------------------
def get_response(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["bye", "exit", "see you"]):
        return "Yalla bye, go bother someone else 😘"

    if "love you" in user_input:
        return "Aww, tragic. I’d love me too if I were you. ❤️"

    if "taha" in user_input:
        return random.choice(insults + worships)

    return random.choice(fallbacks)

# ------------------------
# Streamlit App Setup
# ------------------------
st.set_page_config(page_title="Nrmeen the Savage Bot", page_icon="💅", layout="wide")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("💅 Nrmeen the Savage Bot")

# Sidebar Content
with st.sidebar:
    st.header("👑 About Nrmeen")
    st.markdown("""
    **Nrmeen** is not your therapist. She's here to roast you, maybe worship Taha, and definitely waste your time. Enter at your own risk.
    
    - Fluent in sarcasm
    - Specializes in bullying Taha
    - Occasionally nice, rarely helpful
    """)
    if st.button("🧹 Clear Chat History"):
        st.session_state.history = []

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous chat messages
for sender, message in st.session_state.history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)

# Chat input using new component
if user_input := st.chat_input("Say something to Nrmeen..."):
    # Append user's message
    st.session_state.history.append(("You", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Nrmeen is typing..."):
            time.sleep(1)  # Simulate thinking
            response = get_response(user_input)
            st.markdown(response)

    st.session_state.history.append(("Nrmeen", response))
