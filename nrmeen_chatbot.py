import streamlit as st
import random
import json
from datetime import datetime
import time
import re
import string

# Set up the Streamlit page
st.set_page_config(
    page_title="Chat with Nrmeen", 
    page_icon="💬", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        border-left: 5px solid #4d9eff;
    }
    .chat-message.assistant {
        background-color: #343a40;
        border-left: 5px solid #ff4d4d;
    }
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-bubble {
        padding: 0.5rem 0;
    }
    .mood-indicator {
        font-size: 0.8rem;
        color: #bbb;
        margin-top: 0.3rem;
    }
    div.stButton > button:first-child {
        width: 100%;
    }
    .voice-message {
        background-color: #3a3f4b; 
        padding: 10px; 
        border-radius: 5px; 
        display: flex; 
        align-items: center;
        margin-bottom: 10px;
    }
    .voice-icon {
        margin-right: 10px;
    }
    .typing-indicator {
        display: flex;
        align-items: center;
    }
    .typing-dot {
        height: 8px;
        width: 8px;
        border-radius: 50%;
        background-color: #bbb;
        margin: 0 3px;
        animation: typing-dot-animation 1.4s infinite ease-in-out;
    }
    @keyframes typing-dot-animation {
        0%, 80%, 100% { 
            transform: scale(0);
        } 40% { 
            transform: scale(1.0);
        }
    }
</style>
""", unsafe_allow_html=True)

# App title and header
st.title("💬 Chat with Nrmeen")
st.markdown("Chat with your sarcastic, chaotic friend who's secretly a hype queen")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "mood" not in st.session_state:
    st.session_state.mood = "neutral"  # neutral, excited, annoyed, nostalgic
    
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {
        "mentioned_ex": False,
        "mentioned_taha": False,
        "swear_count": 0,
        "user_annoyed_count": 0,
        "hyped_topics": []
    }

if "typing_animation" not in st.session_state:
    st.session_state.typing_animation = True
    
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = {
        "topics": [],  # List of discussed topics
        "user_interests": [],  # Things the user seems interested in
        "callbacks": [],  # Topics to call back to later
        "last_interaction_time": datetime.now(),
        "friendship_level": 1  # Ranges from 1-5, increases with positive interactions
    }

if "last_sent_thinking_msg" not in st.session_state:
    st.session_state.last_sent_thinking_msg = datetime.now()

# Attempt to load saved chats if they exist
def load_saved_chats():
    try:
        with open("nrmeen_saved_chats.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_current_chat(chat_name):
    if not chat_name.strip():
        return "Please enter a name for this chat"
    
    saved_chats = load_saved_chats()
    
    # Add timestamp to make names unique if duplicate
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if chat_name in saved_chats:
        chat_name = f"{chat_name}_{timestamp}"
    
    saved_chats[chat_name] = {
        "history": st.session_state.chat_history,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "context": st.session_state.conversation_context,
        "memory": st.session_state.conversation_memory
    }
    
    try:
        with open("nrmeen_saved_chats.json", "w") as f:
            json.dump(saved_chats, f)
        return f"Chat saved as '{chat_name}'"
    except Exception as e:
        return f"Error saving chat: {str(e)}"

def load_chat(chat_name):
    saved_chats = load_saved_chats()
    if chat_name in saved_chats:
        st.session_state.chat_history = saved_chats[chat_name]["history"]
        if "context" in saved_chats[chat_name]:
            st.session_state.conversation_context = saved_chats[chat_name]["context"]
        if "memory" in saved_chats[chat_name]:
            st.session_state.conversation_memory = saved_chats[chat_name]["memory"]
        return f"Loaded chat: {chat_name}"
    return f"Chat '{chat_name}' not found"

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # No API key needed for this version
    st.success("✅ No API key required - this version works completely offline!")
    
    # Personality intensity slider
    personality_intensity = st.slider("Personality Intensity", 0.1, 1.0, 0.7, 
                                     help="Higher values make Nrmeen's personality more extreme")
    st.session_state.personality_intensity = personality_intensity
    
    # Response time settings
    min_response_time = st.slider("Min Response Time (sec)", 0.5, 3.0, 1.0,
                                help="Minimum time Nrmeen takes to respond")
    max_response_time = st.slider("Max Response Time (sec)", min_response_time, 5.0, 2.5,
                                help="Maximum time Nrmeen takes to respond")
    
    # Typing animation toggle
    typing_animation = st.toggle("Show typing animation", value=st.session_state.typing_animation,
                               help="Show an animation while Nrmeen is 'typing'")
    st.session_state.typing_animation = typing_animation
    
    # Voice message toggle
    voice_messages = st.toggle("Send occasional voice messages", value=False,
                            help="Nrmeen will occasionally 'send voice messages' instead of text")
    st.session_state.voice_messages = voice_messages
    
    # Random thinking messages
    thinking_messages = st.toggle("Random thinking messages", value=True,
                               help="Nrmeen will sometimes send unprompted messages")
    st.session_state.thinking_messages = thinking_messages
    
    # Thinking message frequency
    thinking_frequency = st.slider("Thinking message frequency", 0.05, 0.3, 0.1, 0.01,
                                 help="How often Nrmeen sends unprompted messages (higher = more frequent)")
    st.session_state.thinking_frequency = thinking_frequency
    
    st.markdown("---")
    
    # Chat management
    st.subheader("Chat Management")
    
    # Save current chat
    save_chat_name = st.text_input("Name this conversation:", 
                                  placeholder="My awesome chat")
    if st.button("Save Current Chat"):
        save_result = save_current_chat(save_chat_name)
        st.info(save_result)
    
    # Load saved chat
    saved_chats = load_saved_chats()
    if saved_chats:
        chat_options = list(saved_chats.keys())
        selected_chat = st.selectbox("Load a saved chat:", chat_options)
        if st.button("Load Selected Chat"):
            load_result = load_chat(selected_chat)
            st.info(load_result)
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.conversation_context = {
            "mentioned_ex": False,
            "mentioned_taha": False,
            "swear_count": 0,
            "user_annoyed_count": 0,
            "hyped_topics": []
        }
        st.session_state.conversation_memory = {
            "topics": [],
            "user_interests": [],
            "callbacks": [],
            "last_interaction_time": datetime.now(),
            "friendship_level": 1
        }
        st.session_state.mood = "neutral"
        st.rerun()
    
    st.markdown("---")
    
    # About Nrmeen
    with st.expander("About Nrmeen", expanded=False):
        st.markdown("""
        **Who is Nrmeen?**
        - Sarcastic, chaotic, and emotionally detached (but secretly caring)
        - A hype queen who hypes up her friends
        - Swears a lot and is brutally honest
        - Loves using slang and abbreviations
        - Says "stfu ya qa7ba" when annoyed or mad
        - Has a love-hate relationship with Taha (sometimes worships him, sometimes roasts him)
        - Randomly brings up missing her ex
        - Often uses "a33333" when excited or frustrated
        - Calls friends "bbg" (baby girl)
        - Can go from "I love you" to "I hate you" in seconds
        """)
    
    # Friendship level indicator
    friendship_level = st.session_state.conversation_memory.get("friendship_level", 1)
    st.subheader("Friendship Level")
    friendship_labels = {
        1: "Acquaintance 😐",
        2: "Friend 🙂",
        3: "Good Friend 😊",
        4: "Close Friend 🥰",
        5: "Best Friend 💕"
    }
    st.progress(friendship_level/5, text=friendship_labels.get(friendship_level, "Acquaintance"))
    
    # Mood indicator
    st.markdown("---")
    st.subheader("Current Mood")
    mood_emojis = {
        "neutral": "😐",
        "excited": "🤪",
        "annoyed": "😒",
        "nostalgic": "🥺",
        "hyped": "💅",
        "angry": "🤬"
    }
    st.markdown(f"<div style='text-align: center; font-size: 3rem;'>{mood_emojis.get(st.session_state.mood, '😐')}</div>", unsafe_allow_html=True)
    st.caption(f"Nrmeen is feeling {st.session_state.mood}")

# Define Nrmeen's style examples for different moods
nrmeen_style_examples = {
    "neutral": [
        "yo yo wassup",
        "nah buddy ure just in love chill",
        "be proud",
        "well unfortunately u have no choice buddy"
    ],
    "excited": [
        "slaaaaayyyyy",
        "i love you bbg", 
        "a33333333",
        "omg im obsesssseeeddd"
    ],
    "annoyed": [
        "stfu ya qa7ba",
        "i swear ya qa7ba im gonna lose it",
        "i hate you so fkn much",
        "this is so random but i hate Taha"
    ],
    "nostalgic": [
        "ugh i miss my ex so much rn for no reason lmao",
        "anyway gtg cry about my ex",
        "u know what would be funny? if my ex texted me rn"
    ],
    "hyped": [
        "YESSSS QUEEN", 
        "UR SLAYING", 
        "best thing ever literally",
        "i worship taha",
        "tahaeism is my religion"
    ]
}

# Common phrases that Nrmeen uses
nrmeen_phrases = {
    "transitions": ["anyway", "so like", "tbh", "ngl", "like", "idk but", "omg", "lol", "lmao"],
    "fillers": ["like", "literally", "honestly", "i swear", "lowkey", "highkey", "fr"],
    "endearments": ["bbg", "bestie", "queen", "king", "buddy", "boo"],
    "swears": ["fuck", "shit", "damn", "fkn", "wtf", "stfu"],
    "reactions": ["slay", "periodt", "no cap", "fr fr", "on god", "thats wild", "im dead", "bruh"]
}

# Keywords that trigger different moods
mood_triggers = {
    "excited": ["party", "weekend", "concert", "success", "good news", "slay", "amazing", "love", "best", "awesome"],
    "annoyed": ["wrong", "stupid", "can't", "don't", "problem", "issue", "bad", "hate", "angry", "mad"],
    "nostalgic": ["ex", "remember", "miss", "past", "before", "used to", "old times", "memory", "back then"],
    "hyped": ["congratulations", "achievement", "proud", "celebrate", "win", "success", "happy", "excited"]
}

# Topics that Nrmeen is likely to bring up randomly
random_topics = [
    "missing her ex",
    "something Taha did",
    "gossip about mutual friends",
    "complaining about school/work",
    "random celebrity gossip",
    "existential crisis",
    "sudden mood change"
]

# Helper function to extract key topics from user input
def extract_topics(text):
    """Extract potential key topics from user input"""
    # Simple extraction - look for nouns and key phrases
    # For a production app, consider using NLP libraries
    
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    
    # Remove stop words (common words that don't carry much meaning)
    stop_words = ["the", "a", "an", "and", "or", "but", "is", "are", "was", "were", 
                 "in", "on", "at", "to", "for", "with", "by", "about", "like", "through",
                 "over", "before", "after", "since", "during", "i", "you", "he", "she", 
                 "it", "we", "they", "his", "her", "its", "their", "what", "which", "who"]
    
    content_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Extract common phrases (2-3 words)
    phrases = []
    for i in range(len(words) - 1):
        if words[i] not in stop_words or words[i+1] not in stop_words:
            phrases.append(f"{words[i]} {words[i+1]}")
    
    for i in range(len(words) - 2):
        if (words[i] not in stop_words or 
            words[i+1] not in stop_words or 
            words[i+2] not in stop_words):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    
    # Prioritize certain categories of topics
    important_categories = {
        "people": ["taha", "ex", "boyfriend", "girlfriend", "friend", "mom", "dad"],
        "emotions": ["happy", "sad", "angry", "excited", "annoyed", "miss", "love", "hate"],
        "events": ["party", "concert", "meeting", "class", "work", "school", "test", "exam"],
        "interests": ["movie", "music", "song", "book", "game", "show", "sport"]
    }
    
    priority_topics = []
    for word in content_words:
        for category, terms in important_categories.items():
            if any(term in word for term in terms):
                priority_topics.append(word)
                break
    
    # Combine all possible topics, with priority ones first
    all_topics = priority_topics + [w for w in content_words if w not in priority_topics] + phrases
    
    # Remove duplicates while preserving order
    seen = set()
    unique_topics = []
    for topic in all_topics:
        if topic not in seen:
            seen.add(topic)
            unique_topics.append(topic)
    
    return unique_topics[:5]  # Return top 5 topics

def create_system_prompt():
    """Create a detailed system prompt based on current mood and context"""
    
    # Get examples based on current mood
    current_mood = st.session_state.mood
    mood_examples = nrmeen_style_examples.get(current_mood, nrmeen_style_examples["neutral"])
    
    # Mix in some examples from other moods for variety
    all_examples = []
    for mood, examples in nrmeen_style_examples.items():
        if mood == current_mood:
            all_examples.extend(examples)  # Add all examples from current mood
        else:
            # Add just 1-2 examples from other moods
            all_examples.extend(random.sample(examples, k=min(2, len(examples))))
    
    # Shuffle examples for variety
    random.shuffle(all_examples)
    examples_text = "\n- ".join(all_examples[:8])  # Limit to 8 total examples
    
    # Base personality description
    base_prompt = (
        "You are Nrmeen. You're sarcastic, chaotic, and emotionally detached but also kind of a hype queen. "
        "You use casual language with lots of slang and text abbreviations. You don't capitalize properly. "
        "You use abbreviations like 'u' instead of 'you', 'ur' instead of 'your/you're', 'r' instead of 'are'. "
        "You swear a lot and are brutally honest but ultimately care about your friends. "
        "You often use multiple question marks or exclamation marks for emphasis. "
        f"Your current mood is {current_mood}. "
    )
    
    # Add mood-specific instructions
    mood_instructions = {
        "neutral": "Be moderately sarcastic and casual.",
        "excited": "Be extra enthusiastic. Use lots of exclamation marks!!! Capitalize RANDOM words for emphasis.",
        "annoyed": "Be more sarcastic and dismissive. Use 'stfu ya qa7ba' if pushed. Be short in your responses.",
        "nostalgic": "Be a bit emotional. Reference your ex or past memories. Use more 'ugh' and 'sigh'.",
        "hyped": "HYPE UP the person you're talking to! Be their biggest cheerleader! Use phrases like 'SLAY QUEEN/KING'.",
        "angry": "Be very irritated. Use 'stfu ya qa7ba' and other harsh phrases. Be dismissive and annoyed."
    }
    
    # Context-specific instructions
    context_instructions = []
    
    # Taha references
    if st.session_state.conversation_context["mentioned_taha"]:
        if random.random() < 0.7:  # 70% chance to worship Taha
            context_instructions.append("Occasionally mention Taha in a positive way, like you worship him.")
        else:
            context_instructions.append("Occasionally roast Taha or complain about him.")
    
    # Ex references
    ex_mention_frequency = 0.2  # Base 20% chance
    if st.session_state.conversation_context["mentioned_ex"]:
        ex_mention_frequency = 0.35  # Increase to 35% if already mentioned
    
    if current_mood == "nostalgic":
        ex_mention_frequency = 0.5  # 50% if already in nostalgic mood
        
    if random.random() < ex_mention_frequency:
        context_instructions.append("Find a way to mention missing your ex or thinking about your ex in this response, but make it seem random and unrelated to the conversation.")
    
    # Combine all prompt components
    full_prompt = (
        f"{base_prompt}\n"
        f"{mood_instructions.get(current_mood, mood_instructions['neutral'])}\n"
        f"Your typical phrases sound like this:\n- {examples_text}\n"
    )
    
    # Add context instructions if any
    if context_instructions:
        full_prompt += "\nSpecific instructions for this response:\n- " + "\n- ".join(context_instructions)
    
    # Add instruction about personality intensity
    intensity = st.session_state.personality_intensity
    full_prompt += f"\nExpress your personality at {int(intensity * 100)}% intensity. Higher intensity means more exaggerated traits."
    
    # Add friendship level context
    friendship_level = st.session_state.conversation_memory.get("friendship_level", 1)
    if friendship_level >= 3:
        full_prompt += f"\nYou consider this person a close friend (level {friendship_level}/5), so be more personal and caring."
    
    return full_prompt

def analyze_message(message):
    """Analyze user message to update context and mood"""
    message_lower = message.lower()
    
    # Extract topics from message
    topics = extract_topics(message_lower)
    
    # Add to conversation memory
    for topic in topics:
        if topic not in st.session_state.conversation_memory["topics"]:
            st.session_state.conversation_memory["topics"].append(topic)
            
            # Randomly decide to callback to this topic later
            if random.random() < 0.3 and len(topic) > 3:
                st.session_state.conversation_memory["callbacks"].append(topic)
    
    # Check for mood triggers
    for mood, triggers in mood_triggers.items():
        if any(trigger in message_lower for trigger in triggers):
            # Don't always change mood, just increase probability
            if random.random() < 0.7:
                st.session_state.mood = mood
    
    # Check for mentions of specific topics
    if "ex" in message_lower or "boyfriend" in message_lower or "girlfriend" in message_lower:
        st.session_state.conversation_context["mentioned_ex"] = True
    
    if "taha" in message_lower:
        st.session_state.conversation_context["mentioned_taha"] = True
    
    # Check for potentially annoying messages
    annoying_triggers = ["you're wrong", "you don't understand", "that's not right", "you're being", 
                         "stop being", "that's stupid", "you should", "you need to", "you have to",
                         "you must", "i disagree", "that's not true", "you're annoying"]
    
    if any(trigger in message_lower for trigger in annoying_triggers):
        st.session_state.conversation_context["user_annoyed_count"] += 1
        if st.session_state.conversation_context["user_annoyed_count"] > 2:
            st.session_state.mood = "angry"
        else:
            st.session_state.mood = "annoyed"
    
    # Check for topics to get hyped about
    positive_topics = ["achievement", "success", "pass", "good news", "happy", "excited", "love", "like"]
    if any(topic in message_lower for topic in positive_topics):
        # Extract the topic to remember for hyping
        for topic in positive_topics:
            if topic in message_lower:
                words = message_lower.split()
                topic_idx = words.index(topic) if topic in words else -1
                if topic_idx >= 0 and topic_idx < len(words) - 3:
                    # Get a few words around the topic
                    potential_topic = " ".join(words[max(0, topic_idx-2):topic_idx+3])
                    if len(potential_topic) > 5:  # Only add if it's substantial
                        st.session_state.conversation_context["hyped_topics"].append(potential_topic)
                        if random.random() < 0.6:  # 60% chance to switch to hyped mood
                            st.session_state.mood = "hyped"
    
    # Check for positive interactions that can increase friendship level
    positive_indicators = ["thank", "appreciate", "love", "awesome", "great", "amazing", "helpful", "fun", "cool"]
    if any(indicator in message_lower for indicator in positive_indicators):
        if random.random() < 0.4:  # 40% chance to increase friendship
            current_level = st.session_state.conversation_memory["friendship_level"]
            if current_level < 5:  # Max level is 5
                st.session_state.conversation_memory["friendship_level"] = min(current_level + 1, 5)
    
    # Check for user interests
    potential_interests = []
    interest_indicators = ["i like", "i love", "i enjoy", "i'm into", "i am into", "im into", "favorite"]
    for indicator in interest_indicators:
        if indicator in message_lower:
            # Find what follows the indicator
            start_idx = message_lower.find(indicator) + len(indicator)
            interest_text = message_lower[start_idx:].strip()
            # Get the first few words
            interest_words = interest_text.split()[:3]
            if interest_words:
                interest = " ".join(interest_words)
                potential_interests.append(interest)
    
    # Add unique interests to memory
    for interest in potential_interests:
        if interest and interest not in st.session_state.conversation_memory["user_interests"]:
            st.session_state.conversation_memory["user_interests"].append(interest)

def get_random_response_delay():
    """Generate a realistic typing delay based on response length"""
    base_delay = random.uniform(1.0, 2.5)  # Base delay between 1-2.5 seconds
    return base_delay

# Enhanced function for rule-based responses with topic awareness
def generate_nrmeen_response(user_input):
    """Generate a response from Nrmeen based on rules and context awareness"""
    user_input_lower = user_input.lower()
    current_mood = st.session_state.mood
    intensity = st.session_state.personality_intensity
    
    # Extract topics from user input
    input_topics = extract_topics(user_input_lower)
    
    # Calculate response complexity (1-3)
    complexity = 1  # Default (simple response)
    
    # Increase complexity if user sent a longer message
    if len(user_input.split()) > 15:
        complexity += 1
    
    # Increase complexity for certain topics
    deep_topics = ["life", "future", "dreams", "goals", "relationships", "feelings"]
    if any(topic in user_input_lower for topic in deep_topics):
        complexity += 1
        
    # Cap complexity based on mood - annoyed/angry moods have shorter responses
    if current_mood in ["annoyed", "angry"]:
        complexity = min(complexity, 1)
    
    # Get mood-specific phrases
    mood_phrases = nrmeen_style_examples.get(current_mood, nrmeen_style_examples["neutral"])
    
    # Template responses for different categories
    greetings = [
        "heyyy",
        "yo wassup",
        "hiiii",
        "hey bbg",
        "sup",
        "omg hiii"
    ]
    
    questions = [
        "wdym??",
        "what r u talking bout lol",
        "wait fr?",
        "no way, r u serious?",
        "lmao what",
        "explain pls im dumb",
        "huh???"
    ]
    
    agreements = [
        "fr fr",
        "yeahhh",
        "omg true",
        "LITERALLY",
        "slay",
        "periodt",
        "on god"
    ]
    
    disagreements = [
        "nahhh",
        "ur wrong lol",
        "u cant be serious",
        "omg noo",
        "thats so dumb",
        "lmao no"
    ]
    
    angry_responses = [
        "stfu ya qa7ba",
        "i swear ya qa7ba im gonna lose it",
        "dont make me say stfu ya qa7ba",
        "i cant with u rn",
        "this is why ppl talk shit about u"
    ]
    
    # Topic-specific responses
    ex_mentions = [
        "ugh i miss my ex so much rn for no reason lmao",
        "anyway gtg cry about my ex",
        "u know what would be funny? if my ex texted me rn",
        "this reminds me of my ex",
        "my ex used to say that lol im sad now",
        "i wonder what my ex is doing"
    ]
    
    taha_worship = [
        "omg taha would literally be perfect for this",
        "taha is a literal god",
        "i worship taha",
        "tahaeism is my religion",
        "taha would never mess this up",
        "we need taha rn"
    ]
    
    taha_hate = [
        "this is so random but i hate taha",
        "taha is so annoying sometimes omg",
        "taha would literally mess this up",
        "dont even get me started on taha",
        "taha is so dumb sometimes i swear",
        "never let taha near this"
    ]
    
    hype_statements = [
        "YESSS QUEEN",
        "UR SLAYING",
        "i love u SO MUCH",
        "bestie ur amazing",
        "ur literally the best",
        "im so proud of u",
        "u deserve everythinggg"
    ]
    
    # Topic-based responses - simple templated responses for common topics
    topic_responses = {
        "school": ["school is the worst lmao", "i cant with school rn", "dont remind me of hw pls"],
        "work": ["work makes me wanna cry", "boss is on my ass again", "im gonna quit i stg"],
        "sleep": ["im so tired all the time", "i havent slept in days", "who needs sleep anyway"],
        "food": ["im starving rn", "i could eat a whole pizza", "lets get food after this"],
        "weekend": ["cant wait for the weekend", "this weekend is gonna be lit", "weekend plans?"],
        "party
