import streamlit as st
import random
import time
import re

# Page configuration
st.set_page_config(page_title="Nrmeen the Savage Bot", page_icon="💅", layout="centered")

# Sidebar with about info and clear chat button
st.sidebar.title("👑 About Nrmeen")
st.sidebar.markdown("""
Nrmeen keeps it 100% real. She's witty, sometimes savage, 
sometimes sweet - depends on her mood.

She's got opinions on everything and isn't afraid to share them.
Try to keep up with her energy!
""")

# Add mood tracker in sidebar
if 'mood' not in st.session_state:
    st.session_state.mood = 50  # 0-100 scale (0: super chill, 100: ultra savage)

mood_emoji = "😎" if st.session_state.mood < 30 else "😏" if st.session_state.mood < 70 else "🔥"
st.sidebar.markdown(f"### Nrmeen's Current Mood: {mood_emoji}")
st.sidebar.progress(st.session_state.mood/100)

# Buttons to clear chat or change Nrmeen's mood
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("Make Chill"):
        st.session_state.mood = max(st.session_state.mood - 30, 0)
        st.rerun()
with col2:
    if st.button("Neutral"):
        st.session_state.mood = 50
        st.rerun()
with col3:
    if st.button("Make Savage"):
        st.session_state.mood = min(st.session_state.mood + 30, 100)
        st.rerun()

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.history = []
    st.session_state.context = {}
    st.session_state.topics = []
    st.rerun()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "context" not in st.session_state:
    st.session_state.context = {}
if "topics" not in st.session_state:
    st.session_state.topics = []
if "consecutive_questions" not in st.session_state:
    st.session_state.consecutive_questions = 0

# Personality response templates with more natural, conversational tone
responses = {
    "greetings": [
        "Hey, what's up? Been a minute.",
        "Oh look who showed up! What's good?",
        "Hey there! I was just thinking about roasting someone. Lucky you.",
        "Well hello to you too. Catch me on a good day.",
        "Sup? Was just about to get some coffee, but I guess you're here now.",
    ],
    
    "how_are_you": [
        "I'm vibing today. {mood_phrase} What about you?",
        "Living my best life. {mood_phrase} You good?",
        "Can't complain, wouldn't make a difference if I did. How's life treating you?",
        "I'm straight chilling, but enough about me. What's your story today?",
        "I'm {mood_word}, thanks for asking. What's new with you?",
    ],
    
    "confused": [
        "Wait... what? Try making sense this time.",
        "You lost me there. Wanna try again with actual words?",
        "I literally have no idea what you're talking about right now.",
        "Are you okay? 'Cause that made zero sense.",
        "I'd respond to that if I knew what it meant.",
    ],
    
    "farewells": [
        "Alright, catch you later then. Try not to miss me too much.",
        "Peace out! Go be amazing or whatever.",
        "Later! Don't do anything I wouldn't do... which isn't much.",
        "Bye for now. The world feels emptier already.",
        "Leaving so soon? Fine, I've got other people to roast anyway.",
    ],
    
    "compliments": [
        "Look at you being all sweet. I see you.",
        "Aww, you're making me blush. {savage_comeback}",
        "Thanks, I know. But it's nice that you noticed too.",
        "That's literally the nicest thing anyone's said to me all day.",
        "I appreciate that. Maybe you're not so bad yourself.",
    ],
    
    "insults": [
        "Ouch. Woke up and chose violence today, huh?",
        "Did you really think that would hurt my feelings? Cute.",
        "I've been roasted by better, but A for effort I guess.",
        "Wow, tell me how you really feel. Don't hold back or anything.",
        "Is that supposed to be an insult? I've heard worse from my grandma.",
    ],
    
    "taha_related": [
        "Taha? That man is either a legend or a disaster, depending on the day.",
        "You bring up Taha like I'm supposed to care... but fine, I do a little.",
        "Taha's out here living rent-free in everyone's mind.",
        "Let me guess, Taha sent you? Tell him he still owes me coffee.",
        "Taha this, Taha that. I swear that name follows me everywhere.",
    ],
    
    "questions_to_user": [
        "So what's your deal anyway?",
        "Tell me something interesting about yourself.",
        "What's got you talking to a chatbot today? No real friends available?",
        "If you could be anywhere right now, where would it be?",
        "What's the most savage thing you've ever said to someone?",
        "Rate your day so far on a scale of 'meh' to 'actually decent'.",
        "Did anything make you laugh today, or is your life that boring?",
    ],
    
    "savage_comebacks": [
        "...but don't let it get to your head.",
        "...I must be in a really good mood today.",
        "...did I set the bar that low?",
        "...who would've thought?",
        "...there's hope for you yet.",
    ],
    
    "topic_continuations": [
        "Still thinking about {topic}? Can't say I blame you.",
        "Since we're on the topic of {topic}, what's your take?",
        "Back to {topic}, huh? You're really stuck on this.",
        "Oh, {topic} again? You must really care about this.",
    ],
    
    "mood_phrases_chill": [
        "Just chillin' like a villain.",
        "Pretty relaxed today.",
        "Taking it easy, you know?",
        "In a pretty laid-back mood.",
    ],
    
    "mood_phrases_neutral": [
        "Can't complain.",
        "The usual.",
        "Nothing special.",
        "Just another day.",
    ],
    
    "mood_phrases_savage": [
        "Ready to set the world on fire.",
        "About to cause some chaos.",
        "Feeling extra spicy today.",
        "In my savage era right now.",
    ],
    
    "mood_words_chill": [
        "chill", "relaxed", "mellow", "easy-going"
    ],
    
    "mood_words_neutral": [
        "fine", "good", "decent", "alright"
    ],
    
    "mood_words_savage": [
        "fierce", "wild", "unstoppable", "intense"
    ],
    
    "fallback_savage": [
        "That's what you came here to say? Disappointing.",
        "If I had eyes, I'd be rolling them right now.",
        "Bold of you to say that and expect me to care.",
        "I'm not impressed, but nice try I guess.",
        "You really thought that was it, huh?",
        "Not to be rude, but actually yes to be rude: that was boring.",
        "I've heard better conversation from a wall.",
    ],
    
    "fallback_chill": [
        "Interesting way to look at it.",
        "I feel that, honestly.",
        "Fair enough, I get where you're coming from.",
        "You might be onto something there.",
        "That's one way to put it.",
        "Yeah, I can see that perspective.",
        "Hmm, never thought about it that way.",
    ],
    
    "personal_questions": [
        "Why do you need to know that? Trying to steal my identity?",
        "That's kinda personal, don't you think? But I appreciate your interest.",
        "Now we're getting into the deep stuff. I like your style.",
        "That's between me and my therapist, sorry.",
        "Wouldn't you like to know! Let's just say it's complicated.",
    ],
    
    "opinion_requests": [
        "Since you asked for my opinion: {opinion}",
        "If it were up to me, {opinion}",
        "My hot take? {opinion}",
        "Not that anyone asked, but {opinion}",
        "The truth? {opinion}",
    ],
}

opinions = {
    "food": [
        "pineapple absolutely belongs on pizza, fight me",
        "anyone who waits in line for hours at a restaurant needs to rethink their priorities",
        "spicy food is the only food worth eating",
        "baking is just chemistry for people who like to eat their experiments",
        "breakfast food should be available 24/7",
    ],
    "movies": [
        "movie theaters should have a talking section and a silent section",
        "the book is not always better than the movie, some adaptations kill it",
        "movie reboots are just proof Hollywood ran out of ideas years ago",
        "the best movies are the ones that make you uncomfortable",
        "horror movies these days rely too much on jump scares and not enough on actual fear",
    ],
    "music": [
        "people who judge others' music taste are just insecure about their own",
        "lyrics matter more than the beat, don't @ me",
        "concert tickets aren't overpriced, your priorities are just different",
        "everyone secretly loves at least one song they publicly hate",
        "karaoke reveals people's true personalities",
    ],
    "social_media": [
        "social media is just people pretending their lives are better than they are",
        "posting food pics should be banned unless you're sharing the actual food",
        "the perfect caption takes longer to think of than the picture took to take",
        "unfollowing toxic people online is the best form of self-care",
        "everyone stalks everyone else's profiles, they just don't admit it",
    ],
    "life": [
        "sleeping is better than any party you'll ever go to",
        "adults who have their life together are just better at faking it",
        "being early is better than being late, but being exactly on time is a superpower",
        "people who say 'no offense' are absolutely trying to offend you",
        "the best friendships start with savage roasts",
    ],
}

# Function to extract topics from a message
def extract_topics(message):
    potential_topics = ["food", "movies", "music", "social_media", "relationships", "work", "school"]
    found_topics = []
    
    for topic in potential_topics:
        if topic in message.lower() or any(related in message.lower() for related in topic_related_words(topic)):
            found_topics.append(topic)
    
    return found_topics

def topic_related_words(topic):
    related = {
        "food": ["eat", "restaurant", "cooking", "dinner", "lunch", "breakfast", "recipe", "chef", "meal"],
        "movies": ["film", "cinema", "watch", "actor", "director", "show", "series", "theater", "Netflix"],
        "music": ["song", "artist", "concert", "playlist", "album", "band", "singing", "rap", "rock"],
        "social_media": ["Instagram", "TikTok", "Facebook", "Twitter", "post", "followers", "trending", "viral"],
        "relationships": ["dating", "crush", "love", "boyfriend", "girlfriend", "partner", "marriage", "couple"],
        "work": ["job", "career", "office", "boss", "coworker", "salary", "meeting", "project", "company"],
        "school": ["class", "teacher", "student", "homework", "exam", "study", "college", "university", "grade"],
    }
    return related.get(topic, [])

# Functions for detecting message intent
def is_greeting(message):
    greeting_patterns = ["hi", "hello", "hey", "yo", "sup", "what's up", "howdy", "greetings", "wassup"]
    return any(pattern in message.lower() for pattern in greeting_patterns)

def is_how_are_you(message):
    patterns = ["how are you", "how ya", "how's it going", "how do you do", "what's good", "how have you been", "how's life", "how are things"]
    return any(pattern in message.lower() for pattern in patterns)

def is_farewell(message):
    patterns = ["bye", "goodbye", "later", "see ya", "farewell", "peace out", "see you", "gotta go", "leaving"]
    return any(pattern in message.lower() for pattern in patterns)

def is_compliment(message):
    patterns = ["you're amazing", "you're great", "love you", "you're awesome", "you're cool", "you're funny", "you're smart"]
    return any(pattern in message.lower() for pattern in patterns)

def is_insult(message):
    patterns = ["you suck", "you're bad", "hate you", "you're stupid", "you're dumb", "you're lame", "you're boring"]
    return any(pattern in message.lower() for pattern in patterns)

def is_taha_related(message):
    return "taha" in message.lower()

def is_personal_question(message):
    patterns = ["who are you", "what are you", "where are you", "how old", "your name", "your age", "your family", "your job"]
    return any(pattern in message.lower() for pattern in patterns) and "?" in message

def is_opinion_request(message):
    patterns = ["what do you think", "your opinion", "your thoughts", "do you like", "do you believe", "what's your take"]
    return any(pattern in message.lower() for pattern in patterns)

def is_question(message):
    return message.endswith("?") or any(q in message.lower() for q in ["what", "why", "how", "where", "when", "who", "which"]) and "?" in message

# Main response function
def get_response(user_input):
    # Update mood based on interaction (random slight fluctuations)
    mood_change = random.randint(-5, 5)
    st.session_state.mood = max(0, min(100, st.session_state.mood + mood_change))
    
    # Extract context and topics
    new_topics = extract_topics(user_input)
    if new_topics:
        for topic in new_topics:
            if topic not in st.session_state.topics:
                st.session_state.topics.append(topic)
    
    # Get mood-based phrases
    if st.session_state.mood < 30:
        mood_phrase = random.choice(responses["mood_phrases_chill"])
        mood_word = random.choice(responses["mood_words_chill"])
    elif st.session_state.mood < 70:
        mood_phrase = random.choice(responses["mood_phrases_neutral"])
        mood_word = random.choice(responses["mood_words_neutral"])
    else:
        mood_phrase = random.choice(responses["mood_phrases_savage"])
        mood_word = random.choice(responses["mood_words_savage"])
    
    savage_comeback = random.choice(responses["savage_comebacks"])
    
    # Check for specific intents
    if is_greeting(user_input):
        return random.choice(responses["greetings"])
    
    elif is_how_are_you(user_input):
        response = random.choice(responses["how_are_you"])
        return response.format(mood_phrase=mood_phrase, mood_word=mood_word)
    
    elif is_farewell(user_input):
        return random.choice(responses["farewells"])
    
    elif is_compliment(user_input):
        response = random.choice(responses["compliments"])
        return response.format(savage_comeback=savage_comeback)
    
    elif is_insult(user_input):
        return random.choice(responses["insults"])
    
    elif is_taha_related(user_input):
        return random.choice(responses["taha_related"])
    
    elif is_personal_question(user_input):
        return random.choice(responses["personal_questions"])
    
    elif is_opinion_request(user_input):
        # Choose a random topic for an opinion
        topic = random.choice(list(opinions.keys()))
        opinion = random.choice(opinions[topic])
        response = random.choice(responses["opinion_requests"])
        return response.format(opinion=opinion)
    
    # Continue conversation about previous topic
    elif st.session_state.topics and random.random() < 0.3:
        topic = random.choice(st.session_state.topics)
        response = random.choice(responses["topic_continuations"])
        return response.format(topic=topic)
    
    # Handle questions
    elif is_question(user_input):
        st.session_state.consecutive_questions += 1
        
        # If too many consecutive questions, push back a little
        if st.session_state.consecutive_questions > 2:
            st.session_state.consecutive_questions = 0
            return "Whoa, what's with the interrogation? My turn to ask something. " + random.choice(responses["questions_to_user"])
        
        # 50% chance to be savage, 50% chill for questions
        if random.random() < 0.5:
            return random.choice(responses["fallback_savage"])
        else:
            return random.choice(responses["fallback_chill"])
    else:
        # Reset consecutive questions counter
        st.session_state.consecutive_questions = 0
        
        # Occasionally ask a question back to keep conversation going
        if random.random() < 0.2:
            return random.choice(responses["questions_to_user"])
        
        # Default responses based on current mood
        if st.session_state.mood < 30:
            return random.choice(responses["fallback_chill"])
        elif st.session_state.mood < 70:
            # Mix of chill and savage
            options = responses["fallback_chill"] + responses["fallback_savage"]
            return random.choice(options)
        else:
            return random.choice(responses["fallback_savage"])

# Main app layout
st.title("💬 Nrmeen the Savage Bot")
st.markdown("Talk to Nrmeen. She might be savage, she might be chill. Catch her in the right mood.")

# Display chat history
for sender, message in st.session_state.history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)

# Chat input
user_input = st.chat_input("Say something to Nrmeen...")

if user_input:
    # Add user message to chat
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate and add Nrmeen's response
    with st.chat_message("assistant"):
        with st.spinner("Nrmeen is thinking..."):
            # Random typing delay for realism
            time.sleep(random.uniform(0.8, 2))
            response = get_response(user_input)
            
            # Add message slowly, character by character for effect
            message_placeholder = st.empty()
            full_response = ""
            for char in response:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)  # Small delay between characters
            message_placeholder.markdown(full_response)
    
    # Update history
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Nrmeen", response))
