import streamlit as st
import random
import time

# --- Setup ---
st.set_page_config(page_title="Nrmeen the Savage Bot", page_icon="💅", layout="centered")

# --- Sidebar ---
st.sidebar.title("👑 About Nrmeen")
st.sidebar.markdown("""
Nrmeen is not your average chatbot. She's sharp-tongued, witty, sometimes insulting,
sometimes flattering—especially to Taha—and always entertaining. Don’t expect sympathy,
expect spice.
""")
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.history = []

# --- Responses ---
insults = [
    "Did your brain take the day off or is this the usual?",
    "You're like WiFi in the desert—useless but still trying.",
    "I’ve seen rocks with more ambition.",
    "You're not even the drama, you're the *ad break* in between.",
    "Was that supposed to impress me?"
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
    "Slay. But also, no.",
    "I'm listening... barely."
]

greetings = [
    "Oh hi. You're back. Yay. 🙄",
    "Hey. Let’s get this over with.",
    "You again? Fine. What is it?",
    "Hi. Surprised you remembered how to type.",
    "Hello... I guess."
]

def get_nrmeen_response(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return random.choice(greetings)

    if any(word in user_input for word in ["bye", "exit", "see you"]):
        return "Yalla bye, go bother someone else 😘"

    if "love you" in user_input:
        return "Aww, tragic. I’d love me too if I were you. ❤️"

    if "taha" in user_input:
        return random.choice(insults + worships)

    # 30% savage, 30% praise, 40% fallback smart sassy
    roll = random.random()
    if roll < 0.3:
        return random.choice(insults)
    elif roll < 0.6:
        return random.choice(worships)
    else:
        return random.choice(fallbacks)

# --- Chat History ---
if "history" not in st.session_state:
    st.session_state.history = []

st.title("💬 Nrmeen the Savage Bot")
st.markdown("Type something and see what she says. No promises on kindness.")

# --- Display History ---
for sender, message in st.session_state.history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)

# --- Chat Input ---
user_input = st.chat_input("Say something to Nrmeen...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Nrmeen is typing..."):
            time.sleep(random.uniform(0.5, 1.2))
            response = get_nrmeen_response(user_input)
            st.markdown(response)

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Nrmeen", response))
