import streamlit as st
import random

# Insults and worships
insults = [
    "Taha, did your brain take the day off or is this the usual?",
    "You're like WiFi in the desert—useless but still trying.",
    "If stupidity had a face... oh wait, hi Taha 😌.",
    "Taha, I’ve seen rocks with more ambition.",
    "You're not even the drama, you're the *ad break* in between."
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

def get_response(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["bye", "exit", "see you"]):
        return "Yalla bye, go bother someone else 😘"

    if "love you" in user_input:
        return "Aww, tragic. I’d love me too if I were you. ❤️"

    if "taha" in user_input:
        return random.choice(insults + worships)

    return random.choice(fallbacks)


# Streamlit App
st.set_page_config(page_title="Nrmeen Chatbot", page_icon="🧠")
st.title("💅 Nrmeen the Savage Bot")
st.markdown("Talk to Nrmeen. She has time… barely.")

# Chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", key="input")

if user_input:
    response = get_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Nrmeen", response))

# Display chat history
for sender, message in st.session_state.history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)
