import streamlit as st
import random
from collections import deque

# Personality Core – Phrase Bank
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

# Keywords for sentiment analysis (simplified)
positive_keywords = ["sweet", "like", "love", "good", "happy", "adore"]
negative_keywords = ["stfu", "kill", "hate", "sad", "cry", "miss", "bad", "angry"]

# Memory for conversation context
context = deque(maxlen=6)

# Mood detection based on user input (simplified sentiment)
def detect_mood(user_input):
    lowered = user_input.lower()
    if "taha" in lowered:
        return "taha_worship"
    elif any(word in lowered for word in positive_keywords):
        return "soft"
    elif any(word in lowered for word in negative_keywords):
        return "savage"
    elif any(word in lowered for word in ["omg", "miss", "hate", "life", "ily"]):
        return "emotional"
    elif any(word in lowered for word in ["hi", "hello", "wassup"]):
        return "greeting"
    else:
        # Default to a random mood if no strong indicators
        moods = ["savage", "soft", "emotional", "romantic", "wisdom"]
        return random.choice(moods)

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

    # Contextual cue boosts (can be made more sophisticated)
    if "taha" in lowered and current_mood != "taha_worship":
        response = random.choice(taha_worship)
    elif any(w in lowered for w in ["sad", "cry", "miss"]) and current_mood != "emotional":
        response += " 😭"
    elif any(w in lowered for w in ["hi", "hello", "wassup"]) and current_mood != "greeting":
        response = random.choice(greetings)

    # Add randomness
    if random.random() < 0.3:
        response += " " + random.choice(["wlh", "frfr", "ong", "ya charmoota", "😝"])

    context.append(f"Nrmeen: {response}")
    return response

# Streamlit UI
st.set_page_config(page_title="Nrmeen the Savage Bot", layout="centered")
theme = st.selectbox("Choose your vibe:", ["light", "dark"])

if theme == "dark":
    st.markdown("""
        <style>
            body { background-color: #1e1e1e; color: #fff; }
            .stTextInput > div > div > input { color: #000; }
        </style>
    """, unsafe_allow_html=True)

st.title(":sparkles: Nrmeen the Savage Bot")
st.write("_Made with chaos, heartbreak, and Taha worship_")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Talk to Nrmeen:", key="input")

if user_input:
    current_mood = detect_mood(user_input)
    reply = generate_response(user_input, current_mood)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Nrmeen", reply))

st.markdown("### 💬 Chat History")
for speaker, message in st.session_state.chat_history[-6:]:
    if speaker == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Nrmeen:** {message}")

st.markdown("---")
st.caption("This bot is powered by pure chaos, coded tantrums, and Taha's ego.")
