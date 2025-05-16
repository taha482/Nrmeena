# nrmeen_chatbot.py

import random

# Memory of the chat
chat_history = []

# Pre-made insults and worship lines
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

def nrmeen_response(user_input):
    user_input = user_input.lower()

    if user_input in ["bye", "goodbye", "see you", "exit"]:
        return "Yalla bye, go bother someone else 😘"

    if "love you" in user_input:
        return "Aww, tragic. I’d love me too if I were you. ❤️"

    if "taha" in user_input:
        # Mix of insults and worships when Taha is mentioned
        if random.random() < 0.5:
            return random.choice(insults)
        else:
            return random.choice(worships)

    # General fallback responses
    replies = [
        "Okay but why should I care?",
        "Your opinion was noted… and ignored. 😌",
        "Try again but this time with brain cells.",
        "Interesting… in the way a car crash is interesting.",
        "Slay. But also, no."
    ]

    return random.choice(replies)

def chat():
    print("Nrmeen is here. Make it quick, I have better things to do.\n")
    while True:
        user_input = input("You: ")
        chat_history.append(f"You: {user_input}")

        response = nrmeen_response(user_input)
        chat_history.append(f"Nrmeen: {response}")

        print("Nrmeen:", response)

        if "bye" in user_input.lower():
            break

if __name__ == "__main__":
    chat()
