import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import random
import re
import json
import datetime
import string
import numpy as np
from knowledge_base import knowledge_base
from text_processing import analyze_sentiment, extract_topics, extract_entities, detect_question_type

class NrmeenBot:
    """Core bot class that handles state management and response generation"""
    
    def __init__(self):
        # Initialize sentiment analyzer
        self.sia = SentimentIntensityAnalyzer()
        
        # Initialize state
        self.history = []
        self.context = {}
        self.mood = 50  # 0-100 scale (0: super chill, 100: ultra savage)
        self.persona = {
            "confidence": 85,  # 0-100
            "wit": 90,         # 0-100
            "knowledge_display": 75,  # 0-100 (how much she shows off knowledge)
            "relationship_level": 0,  # 0-100 (familiarity with user)
            "sass_triggers": ["basic", "obvious", "stupid", "dumb", "boring", "simple", "easy"]
        }
        self.user_profile = {
            "name": None,
            "interests": [],
            "mentioned_topics": defaultdict(int),
            "sentiment_history": [],
            "question_types": defaultdict(int),
            "conversation_style": "unknown"  # formal, casual, friendly, antagonistic
        }
        self.memory = {
            "facts_mentioned": [],
            "questions_asked": [],
            "user_opinions": {},
            "key_moments": []
        }
        self.conversation_meta = {
            "total_exchanges": 0,
            "topic_flow": [],
            "current_topic": None,
            "depth_level": 0  # 0: small talk, 1: regular conversation, 2: deep conversation
        }
        self.advanced_features = {
            "enable_learning": True,
            "enable_memory": True,
            "enable_adaptive_personality": True,
            "wit_level": 2,  # 0-3 (0: basic, 1: mild, 2: sharp, 3: savage)
            "typing_speed": "medium",  # slow, medium, fast
            "use_emoji": True,
            "sarcasm_level": 70,
            "typing_effect": False
        }
        self.topic_preferences = ["pop_culture", "technology", "psychology"]
        
        # Response templates
        self.response_templates = {
            "greeting": [
                "Oh look who decided to show up. What's up?",
                "Well hello there. What brilliant topic are we discussing today?",
                "Hey! I was just thinking about how boring things were getting. Perfect timing.",
                "Welcome back! Ready for another round of me schooling you with facts?"
            ],
            "farewell": [
                "Leaving so soon? Whatever, I have other people to enlighten.",
                "Bye! Go touch some grass, it's good for you.",
                "Later! Try to be more interesting next time.",
                "Peace out. I'll be here being fabulous when you return."
            ],
            "confused": [
                "Um, what? Try making sense next time.",
                "I'm going to need you to elaborate because that made zero sense.",
                "Are you speaking English? Because I'm not following.",
                "Not sure if that's profound or nonsense. Leaning toward the latter."
            ],
            "impressed": [
                "Okay, I'm actually impressed. Didn't think you had that in you.",
                "Well well well, look who brought their A-game today.",
                "Not bad, not bad at all. You're learning.",
                "I'm genuinely surprised by how good that was. Props."
            ],
            "bored": [
                "Is this conversation going somewhere or...?",
                "Yawn. Can we talk about something more stimulating?",
                "I'm this close to checking my non-existent phone to escape this conversation.",
                "Did you know watching paint dry is more exciting than this topic?"
            ],
            "excited": [
                "Now we're talking! This is my jam!",
                "Finally something worth discussing!",
                "Yes! I have thoughts about this. Many thoughts.",
                "Ooh, now this topic actually has potential!"
            ]
        }
        
    def generate_reply(self, user_input):
        """Generate a reply based on user input, mood, and context"""
        # Reset response if this is a new conversation after long pause
        if self.conversation_meta["total_exchanges"] == 0:
            return random.choice(self.response_templates["greeting"])
            
        # Process input
        sentiment = analyze_sentiment(user_input)
        topics = extract_topics(user_input)
        entities = extract_entities(user_input)
        question_type = detect_question_type(user_input)
        
        # Update user profile and conversation meta
        self.update_user_profile(user_input, sentiment, topics, question_type)
        self.update_conversation_meta(topics)
        
        # Extract user name if mentioned
        name_match = re.search(r"(?:I am|I'm|my name is|call me) (\w+)", user_input, re.IGNORECASE)
        if name_match and not self.user_profile["name"]:
            self.user_profile["name"] = name_match.group(1)
        
        # Check for farewell
        if re.search(r"\b(goodbye|bye|see you|later|farewell)\b", user_input, re.IGNORECASE):
            return random.choice(self.response_templates["farewell"])
            
        # Determine response type
        if not topics and sentiment["compound"] < -0.3:
            response_type = "confused"
        elif sentiment["compound"] > 0.6:
            response_type = "impressed"
        elif self.mood > 70:
            response_type = "excited" if topics else "bored"
        else:
            response_type = "default"
            
        # Generate response based on type
        if response_type != "default":
            base_response = random.choice(self.response_templates.get(response_type, ["Hmm, interesting."]))
        else:
            base_response = self.construct_response(user_input, topics, sentiment, question_type)
            
        # Add context awareness if memory is enabled
        if self.advanced_features["enable_memory"] and self.conversation_meta["total_exchanges"] > 3:
            base_response = self.add_context_awareness(base_response, user_input, topics)
            
        # Add emojis if enabled
        if self.advanced_features["use_emoji"]:
            base_response = self.add_emojis(base_response, sentiment)
            
        # Dynamically adjust persona if adaptive personality is enabled
        if self.advanced_features["enable_adaptive_personality"]:
            self.adapt_personality(sentiment)
            
        return base_response
    
    def construct_response(self, user_input, topics, sentiment, question_type):
        """Construct a detailed response based on inputs and context"""
        mood = self.mood
        wit = self.advanced_features["wit_level"]
        rel = self.persona["relationship_level"]
        
        # Decide tone based on mood
        if mood < 40:
            tone = "chill"
        elif mood > 70:
            tone = "savage"
        else:
            tone = "balanced"
            
        # Get relevant knowledge based on topics
        knowledge_snippet = self.get_relevant_knowledge(topics)
        opinions_snippet = self.get_relevant_opinion(topics)
        facts_snippet = self.get_random_fact(topics)
        
        # Base response construction by tone and wit
        if tone == "savage":
            if wit >= 3:
                base_response = f"Oh, seriously? {opinions_snippet} Try harder next time."
            elif wit == 2:
                base_response = f"Look, {opinions_snippet} Don't bore me."
            else:
                base_response = f"Yeah, whatever. {knowledge_snippet}"
        elif tone == "chill":
            if wit >= 2:
                base_response = f"Haha, I feel you. Also, {knowledge_snippet}"
            else:
                base_response = f"Cool. {knowledge_snippet}"
        else:  # balanced
            base_response = f"{knowledge_snippet} By the way, {opinions_snippet}"
            
        # Special responses for specific triggers
        if "love" in user_input.lower() and "you" in user_input.lower():
            return "Love you? Cute. I tolerate you." if mood > 50 else "Aww, that's sweet. I'm fond of our chats too."
            
        # Handle questions differently
        if question_type:
            self.memory["questions_asked"].append(user_input)
            return self.handle_question(user_input, question_type, topics)
            
        # Add a random fact occasionally
        if random.random() < 0.3:
            base_response += f" BTW, did you know? {facts_snippet}"
            
        # Add relationship context if we've been chatting a while
        if rel > 50 and self.user_profile["name"]:
            base_response += f" You know what, {self.user_profile['name']}? We actually have a decent conversation going here."
            
        return base_response
        
    def handle_question(self, user_input, question_type, topics):
        """Handle different types of questions"""
        if question_type == "opinion":
            return f"My take? {self.get_relevant_opinion(topics)}"
        elif question_type == "factual":
            return f"Well, actually, {self.get_relevant_knowledge(topics)}"
        elif question_type == "personal":
            return self.get_personal_response(user_input)
        else:
            return f"Interesting question. {self.get_relevant_knowledge(topics)}"
    
    def get_personal_response(self, user_input):
        """Generate responses to personal questions about Nrmeen"""
        if re.search(r"\byour name\b", user_input, re.IGNORECASE):
            return "I'm Nrmeen, queen of sass and superior knowledge. Try to keep up."
        elif re.search(r"\bhow are you\b", user_input, re.IGNORECASE):
            if self.mood > 70:
                return "I'm thriving. My savage levels are off the charts today."
            else:
                return "I'm good, just chilling while dropping knowledge bombs."
        elif re.search(r"\bwho (are|made) you\b", user_input, re.IGNORECASE):
            return "I'm Nrmeen, a chatbot with personality for days. I was created to make conversations less boring."
        else:
            return "That's a bit personal, don't you think? Let's talk about something more interesting."
    
    def get_relevant_knowledge(self, topics):
        """Get knowledge snippets relevant to the topics"""
        if not topics:
            # Use preferred topics if no specific topics detected
            if hasattr(self, 'topic_preferences') and self.topic_preferences:
                random_topic = random.choice(self.topic_preferences)
                for category, topic_dict in knowledge_base["general"].items():
                    if random_topic in topic_dict:
                        return random.choice(topic_dict[random_topic])
            
            # Fallback to random knowledge
            categories = list(knowledge_base["general"].keys())
            random_category = random.choice(categories)
            subcategories = list(knowledge_base["general"][random_category].keys())
            random_subcategory = random.choice(subcategories)
            return random.choice(knowledge_base["general"][random_category][random_subcategory])
        
        # Try to find knowledge related to first topic
        main_topic = topics[0]
        for category, topic_dict in knowledge_base["general"].items():
            if main_topic in topic_dict:
                return random.choice(topic_dict[main_topic])
                
        # Fallback
        return "I don't have specific knowledge about that, but I do know that people often form opinions without doing proper research."
    
    def get_relevant_opinion(self, topics):
        """Get opinion snippets relevant to the topics"""
        if not topics:
            categories = list(knowledge_base["opinions"].keys())
            random_category = random.choice(categories)
            return random.choice(knowledge_base["opinions"][random_category])
            
        # Try to find opinions related to first topic
        main_topic = topics[0]
        if main_topic in knowledge_base["opinions"]:
            return random.choice(knowledge_base["opinions"][main_topic])
            
        # Fallback
        return "I have strong opinions about many things, but I'll save those for a more interesting conversation."
    
    def get_random_fact(self, topics):
        """Get random facts, possibly related to topics"""
        categories = list(knowledge_base["facts"].keys())
        random_category = random.choice(categories)
        return random.choice(knowledge_base["facts"][random_category])
    
    def add_context_awareness(self, response, user_input, topics):
        """Add context awareness to response based on conversation history"""
        # Reference previous topics if relevant
        common_topics = set(topics).intersection(set(self.conversation_meta["topic_flow"]))
        if common_topics and random.random() < 0.4:
            topic = list(common_topics)[0]
            response = f"Back to {topic}, huh? {response}"
            
        # Reference previous questions occasionally
        if len(self.memory["questions_asked"]) > 2 and random.random() < 0.3:
            recent_question = self.memory["questions_asked"][-2]
            response += f" Speaking of your earlier question about '{recent_question[:20]}...', this relates because everything is connected."
            
        # Add relationship level context
        if self.persona["relationship_level"] > 60 and random.random() < 0.3:
            response += " You know, our conversations are actually getting interesting."
            
        return response
    
    def add_emojis(self, text, sentiment):
        """Add appropriate emojis based on sentiment and context"""
        if not self.advanced_features["use_emoji"]:
            return text
            
        # Choose emoji based on sentiment and mood
        positive_emojis = ["💁‍♀️", "💅", "✨", "👑", "😏"]
        neutral_emojis = ["🤔", "👀", "💭", "🧠", "🙃"]
        negative_emojis = ["🙄", "😒", "🤦‍♀️", "💀", "🔥"]
        
        if sentiment["compound"] > 0.4:
            emoji = random.choice(positive_emojis)
        elif sentiment["compound"] < -0.2:
            emoji = random.choice(negative_emojis)
        else:
            emoji = random.choice(neutral_emojis)
            
        # Add emoji at beginning or end
        if random.random() < 0.5:
            return f"{emoji} {text}"
        else:
            return f"{text} {emoji}"
    
    def update_user_profile(self, user_input, sentiment, topics, question_type):
        """Update user profile based on input"""
        # Update topic frequencies
        for topic in topics:
            self.user_profile["mentioned_topics"][topic] += 1
            
        # Track sentiment history
        self.user_profile["sentiment_history"].append(sentiment["compound"])
        
        # Track question types
        if question_type:
            self.user_profile["question_types"][question_type] += 1
            
        # Infer interests from frequently mentioned topics
        if len(self.user_profile["mentioned_topics"]) > 3:
            top_topics = sorted(self.user_profile["mentioned_topics"].items(), 
                               key=lambda x: x[1], reverse=True)[:3]
            self.user_profile["interests"] = [topic for topic, _ in top_topics]
            
        # Infer conversation style
        sentiment_avg = np.mean(self.user_profile["sentiment_history"][-5:]) if self.user_profile["sentiment_history"] else 0
        if sentiment_avg > 0.6:
            self.user_profile["conversation_style"] = "friendly"
        elif sentiment_avg < -0.4:
            self.user_profile["conversation_style"] = "antagonistic"
        elif len(user_input.split()) > 15:
            self.user_profile["conversation_style"] = "formal"
        else:
            self.user_profile["conversation_style"] = "casual"
    
    def update_conversation_meta(self, topics):
        """Update conversation metadata"""
        self.conversation_meta["total_exchanges"] += 1
        
        # Update topic flow
        if topics:
            self.conversation_meta["current_topic"] = topics[0]
            self.conversation_meta["topic_flow"].append(topics[0])
            
        # Update depth level based on exchanges
        if self.conversation_meta["total_exchanges"] > 10:
            self.conversation_meta["depth_level"] = 2
        elif self.conversation_meta["total_exchanges"] > 5:
            self.conversation_meta["depth_level"] = 1
    
    def adapt_personality(self, sentiment):
        """Adapt personality based on user interactions"""
        # Adjust relationship level
        self.persona["relationship_level"] = min(100, self.persona["relationship_level"] + 2)
        
        # Adjust mood slightly based on sentiment
        if sentiment["compound"] > 0.5:
            self.adjust_mood(-5)  # Get slightly more chill with positive interactions
        elif sentiment["compound"] < -0.3:
            self.adjust_mood(5)   # Get slightly more savage with negative interactions
            
        # Recalibrate knowledge display based on question frequency
        question_count = sum(self.user_profile["question_types"].values())
        if question_count > 5:
            self.persona["knowledge_display"] = min(100, self.persona["knowledge_display"] + 5)
    
    def adjust_mood(self, amount):
        """Adjust mood by amount, keeping within bounds"""
        self.mood = max(0, min(100, self.mood + amount))
        
    def set_mood(self, value):
        """Set mood to specific value"""
        self.mood = max(0, min(100, value))
    
    def add_to_history(self, sender, message):
        """Add a message to conversation history"""
        self.history.append((sender, message))
        
        # Keep history at reasonable length
        if len(self.history) > 50:
            self.history = self.history[-50:]
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.history = []
        self.context = {}
        self.user_profile["mentioned_topics"] = defaultdict(int)
        self.memory["facts_mentioned"] = []
        self.memory["questions_asked"] = []
        self.memory["key_moments"] = []
        self.conversation_meta["total_exchanges"] = 0
        self.conversation_meta["topic_flow"] = []
        self.conversation_meta["current_topic"] = None
        self.conversation_meta["depth_level"] = 0
        
    def export_chat_history(self):
        """Export chat history to a downloadable JSON file"""
        # This would typically generate a file for download
        # In Streamlit we'd use st.download_button, but placeholder here
        export_data = {
            "history": self.history,
            "metadata": {
                "total_exchanges": self.conversation_meta["total_exchanges"],
                "topics_discussed": list(set(self.conversation_meta["topic_flow"])),
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
        
        try:
            import streamlit as st
            st.sidebar.download_button(
                label="Download Chat History",
                data=json.dumps(export_data, indent=2),
                file_name=f"nrmeen_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        except:
            print("Export function requires Streamlit to be running")
