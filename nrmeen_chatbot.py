import streamlit as st
import random
from collections import deque
import re
import datetime
import math

class SmartChatbot:
    def __init__(self):
        # Core personality traits (toned down but keeping character)
        self.greetings = ["Hey there!", "Hi friend!", "Hello! How are you?", "What's up?", "Good to see you!"]
        self.wisdom = [
            "Sometimes walking away is the best solution.",
            "Focus on what builds you up, not what tears you down.",
            "Self-care isn't selfish, it's necessary.",
            "The right people won't make you question your worth.",
            "Your peace of mind is worth more than pleasing others."
        ]
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        self.random_facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "Octopuses have three hearts, nine brains, and blue blood.",
            "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis but only 225 Earth days to orbit the Sun.",
            "The world's oldest known living tree is over 5,000 years old.",
            "Bananas are berries, but strawberries aren't."
        ]
        
        # Memory for conversation context
        self.context = deque(maxlen=10)
        self.current_mood = "neutral"
        self.conversation_topics = set()
        self.user_facts = {}
        
    def detect_intent(self, user_input):
        lowered = user_input.lower()
        
        # Intent detection
        if re.search(r'\b(hi|hello|hey|greetings|sup|wassup)\b', lowered):
            return "greeting"
        elif re.search(r'\b(how are you|how.+doing|what.+up)\b', lowered):
            return "personal_inquiry"
        elif re.search(r'\b(joke|funny|make me laugh|tell me something funny)\b', lowered):
            return "joke_request"
        elif re.search(r'\b(advice|help me|what should i|suggestion)\b', lowered):
            return "advice_request"
        elif re.search(r'\b(fact|tell me something|interesting|did you know)\b', lowered):
            return "fact_request"
        elif re.search(r'\b(time|date|day|today|current time)\b', lowered):
            return "time_request"
        elif re.search(r'\b(math|calculate|compute|solve|what is \d+[\+\-\*\/]\d+)\b', lowered):
            return "math_request"
        elif re.search(r'\b(my name is|i am|i\'m|call me)\b', lowered):
            return "personal_info"
        else:
            return "conversation"
    
    def extract_personal_info(self, user_input):
        lowered = user_input.lower()
        
        # Name extraction
        name_match = re.search(r'my name is (\w+)|call me (\w+)|i am (\w+)|i\'m (\w+)', lowered)
        if name_match:
            # Find the first non-None group
            name = next((group for group in name_match.groups() if group is not None), None)
            if name and name not in ["am", "just", "so", "very", "a", "an", "the"]:
                self.user_facts["name"] = name.capitalize()
        
        # Age extraction
        age_match = re.search(r'i am (\d+)|i\'m (\d+)|(\d+) years old', lowered)
        if age_match:
            age = next((group for group in age_match.groups() if group is not None), None)
            if age:
                self.user_facts["age"] = age
        
        # Location extraction
        location_match = re.search(r'i live in (\w+)|i\'m from (\w+)|i am from (\w+)', lowered)
        if location_match:
            location = next((group for group in location_match.groups() if group is not None), None)
            if location:
                self.user_facts["location"] = location.capitalize()
    
    def solve_math(self, user_input):
        # Simple calculator functionality
        math_match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', user_input)
        if math_match:
            try:
                num1 = float(math_match.group(1))
                operator = math_match.group(2)
                num2 = float(math_match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "I can't divide by zero! That's not mathematically possible."
                    result = num1 / num2
                
                # Format result to avoid trailing zeros
                if result == int(result):
                    return f"The answer is {int(result)}."
                else:
                    return f"The answer is {result}."
            except:
                return "I had trouble with that calculation. Could you please format it clearly like '2 + 2'?"
        
        # Check for square root request
        sqrt_match = re.search(r'square root of (\d+)', user_input.lower())
        if sqrt_match:
            try:
                num = float(sqrt_match.group(1))
                result = math.sqrt(num)
                
                if result == int(result):
                    return f"The square root of {int(num)} is {int(result)}."
                else:
                    return f"The square root of {int(num)} is approximately {result:.4f}."
            except:
                return "I had trouble calculating that square root."
        
        return "I couldn't identify a math problem to solve. Try formatting it like '2 + 2' or 'square root of 16'."
    
    def get_time_info(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        return f"It's currently {time_str} on {date_str}."
    
    def personalize_response(self, response):
        if "name" in self.user_facts:
            return f"{response.rstrip('.').rstrip('!')} {self.user_facts['name']}!"
        return response
    
    def generate_response(self, user_input):
        intent = self.detect_intent(user_input)
        self.extract_personal_info(user_input)
        
        # Track conversation topics for better context
        words = set(re.findall(r'\b\w{4,}\b', user_input.lower()))
        self.conversation_topics.update(words)
        
        # Store the conversation
        self.context.append(f"You: {user_input}")
        
        # Generate response based on intent
        if intent == "greeting":
            response = self.personalize_response(random.choice(self.greetings))
        elif intent == "personal_inquiry":
            moods = ["pretty good", "doing well", "great", "fantastic", "not too bad"]
            response = f"I'm {random.choice(moods)} today! How about you?"
        elif intent == "joke_request":
            response = random.choice(self.jokes)
        elif intent == "advice_request":
            response = random.choice(self.wisdom)
        elif intent == "fact_request":
            response = random.choice(self.random_facts)
        elif intent == "time_request":
            response = self.get_time_info()
        elif intent == "math_request":
            response = self.solve_math(user_input)
        elif intent == "personal_info":
            if "name" in self.user_facts:
                response = f"Nice to meet you, {self.user_facts['name']}! I'll remember that."
            else:
                response = "It's great to learn more about you!"
        else:
            # Default conversation mode
            if len(self.context) <= 2:  # First few exchanges
                response = "Tell me more! I'm here to chat about whatever's on your mind."
            else:
                # Reference previous topics occasionally
                if self.conversation_topics and random.random() < 0.3:
                    topic = random.choice(list(self.conversation_topics))
                    response = f"Speaking of {topic}, what are your thoughts on that?"
                else:
                    response = random.choice([
                        "That's an interesting perspective!",
                        "I see what you mean.",
                        "Tell me more about that!",
                        "What else is on your mind?",
                        "I find that fascinating.",
                        random.choice(self.wisdom)
                    ])
        
        # Add some randomized personality elements but more subtle
        if random.random() < 0.2 and intent not in ["time_request", "math_request"]:
            emojis = ["😊", "💭", "✨", "👍", "💯"]
            response += f" {random.choice(emojis)}"
            
        self.context.append(f"Chatbot: {response}")
        return response

# --- Streamlit UI with Modern Design ---
def main():
    st.set_page_config(page_title="Smart Chatbot", page_icon="💬", layout="wide")

    # Custom CSS for a modern chat interface
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .main {
            background-color: #ffffff;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            max-width: 1000px;
            margin: 0 auto;
        }
        .chat-message {
            padding: 15px 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            position: relative;
            width: fit-content;
            max-width: 80%;
        }
        .user-message {
            background-color: #e6f7ff;
            border: 1px solid #bae7ff;
            margin-left: auto;
            text-align: right;
            border-top-right-radius: 0;
        }
        .bot-message {
            background-color: #f6f6f6;
            border: 1px solid #e6e6e6;
            margin-right: auto;
            text-align: left;
            border-top-left-radius: 0;
        }
        .chat-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f0f0f0;
        }
        .chat-container {
            height: 60vh;
            overflow-y: auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #f0f0f0;
        }
        .input-area {
            display: flex;
            align-items: center;
        }
        .message-timestamp {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 5px;
        }
        .stButton button {
            border-radius: 20px;
            padding: 0 25px;
            background-color: #1890ff;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SmartChatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # App header
    st.markdown("<div class='chat-header'><h1>💬 Smart Chatbot</h1><p>Your friendly AI chat companion</p></div>", unsafe_allow_html=True)

    # Chat display area
    st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"""
                <div class='chat-message user-message'>
                    {message['content']}
                    <div class='message-timestamp'>{message['time']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='chat-message bot-message'>
                    {message['content']}
                    <div class='message-timestamp'>{message['time']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # User input area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Type your message...", key="user_input", label_visibility="collapsed")
    
    with col2:
        send_button = st.button("Send")

    # Process input
    if send_button and user_input:
        # Get current time
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        
        # Add user message to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'time': current_time
        })
        
        # Generate response
        response = st.session_state.chatbot.generate_response(user_input)
        
        # Add bot response to chat history
        st.session_state.messages.append({
            'role': 'bot',
            'content': response,
            'time': current_time
        })
        
        # Clear input box
        st.session_state.user_input = ""
        
        # Auto-scroll to bottom (requires JavaScript)
        st.markdown("""
            <script>
                function scrollToBottom() {
                    var chatContainer = document.getElementById('chat-container');
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
                window.onload = scrollToBottom;
            </script>
            """, unsafe_allow_html=True)
        
        # Force refresh for immediate display of new messages
        st.experimental_rerun()

    # Add helpful hints
    with st.expander("💡 Chat Features"):
        st.markdown("""
        **Try asking me:**
        - "Tell me a joke!"
        - "Give me some advice"
        - "Share an interesting fact"
        - "What time is it?"
        - Simple math like "Calculate 25 + 37"
        - "My name is [your name]" so I can remember you!
        """)

if __name__ == "__main__":
    main()
