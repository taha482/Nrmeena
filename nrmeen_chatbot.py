import streamlit as st
import random
import time

st.set_page_config(page_title="Nrmeen the Savage Bot", page_icon="💅", layout="centered")

st.sidebar.title("👑 About Nrmeen")
st.sidebar.markdown("""
Nrmeen is sharp, witty, sometimes savage, sometimes chill.
She’s got mood swings but always keeps it real.
Try her out and see if you can keep up.
""")

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.history = []

# Response categories with more natural replies
greetings = [
    "Hey, you again? What’s up?",
    "Yo, nice to see you. What’s the vibe?",
    "Hey there! Ready for some savage talk or chill chat?",
    "Hello! Let’s keep this interesting.",
]

how_are_you = [
    "I'm good, just roasting people like usual. You?",
    "Living the savage life, what about you?",
    "Better now that you showed up. What's good?",
    "I'm fine, but I only care if you're entertaining.",
]

confused = [
    "Wait, what did you say?",
    "I’m not sure I got that. Try again?",
    "That sounds like gibberish to me.",
]

farewells = [
    "Alright, peace out! Don’t miss me too much.",
    "Bye bye, don’t get yourself into trouble.",
    "Catch you later, if you’re lucky.",
]

love_replies = [
    "Aww, I’d love me too if I were you.",
    "Flattery will get you nowhere... except maybe a compliment.",
]

taha_related = [
    "Taha? Yeah, legend status confirmed.",
    "You talk about Taha like he’s the king, huh?",
    "Taha’s out here breaking hearts and taking names.",
    "If only Taha knew how much I roast him behind his back.",
]

fallback_savage = [
    "Interesting... if you’re into nonsense.",
    "You really said that? Bold move.",
    "Try harder next time.",
    "Meh, not impressed.",
    "Keep talking, I’m just warming up.",
]

fallback_chill = [
    "Hmm, okay.",
    "Alright, got it.",
    "Cool story, bro.",
    "I see what you did there.",
    "That’s something.",
]

def get_response(user_input):
    user_input = user_input.lower()

    # Greetings
    if any(greet in user_input for greet in ["hi", "hello", "hey", "yo"]):
        return random.choice(greetings)

    # How are you
    if any(phrase in user_input for phrase in ["how are you", "how ya", "how's it going", "how do you do"]):
        return random.choice(how_are_you)

    # Bye / exit
    if any(word in user_input for word in ["bye", "exit", "see you", "later"]):
        return random.choice(farewells)

    # Love you
    if "love you" in user_input:
        return random.choice(love_replies)

    # Talk about Taha
    if "taha" in user_input:
        return random.choice(taha_related)

    # Question detection
    if user_input.endswith("?"):
        # 50% chance to be savage, 50% chill answer
        if random.random() < 0.5:
            return random.choice(fallback_savage)
        else:
            return random.choice(fallback_chill)

    # Otherwise fallback, mix savage and chill
    return random.choice(fallback_savage + fallback_chill)


if "history" not in st.session_state:
    st.session_state.history = []

st.title("💬 Nrmeen the Savage Bot")
st.markdown("Talk to Nrmeen. She might be savage, but sometimes she’s chill.")

for sender, message in st.session_state.history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)

user_input = st.chat_input("Say something to Nrmeen...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Nrmeen is thinking..."):
            time.sleep(random.uniform(0.6, 1.2))
            response = get_response(user_input)
            st.markdown(response)

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Nrmeen", response))
