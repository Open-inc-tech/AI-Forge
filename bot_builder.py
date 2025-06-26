import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import re

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def generate_bot_module(bot_config):
    """Generate a new bot module based on user configuration"""
    
    # Clean the bot name for file naming
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', bot_config['name'].lower())
    filename = f"{clean_name}_module.py"
    
    # Create the module code
    module_code = f'''import random
import re
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))
from base_module import BaseAIModule

class AIModule(BaseAIModule):
    """{bot_config['name']} - {bot_config['description']}
    
    Created with AI Forge Bot Builder
    Creation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    name = "{bot_config['name']}"
    version = "{bot_config['version']}"
    description = "{bot_config['description']}"
    creation_date = "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def __init__(self):
        super().__init__()
        
        # User-defined personality traits
        self.personality_traits = {bot_config['personality']}
        
        # User-defined response templates
        self.response_templates = {{
            'greeting': {bot_config['greetings']},
            'question': {bot_config['question_responses']},
            'unknown': {bot_config['unknown_responses']},
            'thanks': [
                "You're welcome!",
                "Happy to help!",
                "No problem!",
                "Glad I could assist!"
            ],
            'goodbye': [
                "Goodbye!",
                "See you later!",
                "Take care!",
                "Until next time!"
            ]
        }}
        
        # User-defined knowledge areas
        self.knowledge_areas = {bot_config['knowledge_areas']}
        
        # User-defined custom responses
        self.custom_responses = {bot_config['custom_responses']}
        
        # Advanced bot settings
        self.learning_style = "{bot_config['learning_style']}"
        self.response_style = "{bot_config['response_style']}"
        self.interaction_mode = "{bot_config.get('interaction_mode', 'conversational')}"
        self.memory_retention = "{bot_config.get('memory_retention', 'standard')}"
        self.creativity_level = {bot_config.get('creativity_level', 5)}
        self.verbosity_level = "{bot_config.get('verbosity_level', 'balanced')}"
        self.emoji_usage = {bot_config.get('emoji_usage', True)}
        self.language_preference = "{bot_config.get('language_preference', 'auto')}"
    
    def generate_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate response using user-defined personality and knowledge"""
        
        # First, check for custom responses
        user_lower = user_input.lower().strip()
        for trigger, response in self.custom_responses.items():
            if trigger.lower() in user_lower:
                return response
        
        # Try to find learned response
        learned_response = self.find_similar_response(user_input)
        if learned_response:
            return self.apply_personality_filter(learned_response)
        
        # Clean input
        clean_input = self.clean_input(user_input)
        
        # Detect intent
        intent = self.detect_intent(clean_input)
        
        # Generate response based on intent and personality
        response = self.generate_personalized_response(intent, clean_input, chat_history)
        
        # Learn from interaction
        confidence = 0.8 if intent != 'unknown' else 0.5
        self.learn_from_conversation(user_input, response, confidence=confidence)
        
        return response
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent"""
        text_lower = text.lower()
        
        # Greeting detection
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in text_lower for greeting in greetings):
            return 'greeting'
        
        # Question detection
        if '?' in text or any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            return 'question'
        
        # Thanks detection
        if any(word in text_lower for word in ['thank', 'thanks', 'appreciate']):
            return 'thanks'
        
        # Goodbye detection
        if any(word in text_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return 'goodbye'
        
        return 'unknown'
    
    def generate_personalized_response(self, intent: str, clean_input: str, chat_history: List[Dict]) -> str:
        """Generate response based on user-defined personality"""
        
        if intent == 'greeting':
            response = random.choice(self.response_templates['greeting'])
        elif intent == 'question':
            response = self.handle_question(clean_input, chat_history)
        elif intent == 'thanks':
            response = random.choice(self.response_templates['thanks'])
        elif intent == 'goodbye':
            response = random.choice(self.response_templates['goodbye'])
        else:
            response = random.choice(self.response_templates['unknown'])
        
        return self.apply_personality_filter(response)
    
    def handle_question(self, clean_input: str, chat_history: List[Dict]) -> str:
        """Handle questions based on knowledge areas"""
        
        # Check if question relates to known knowledge areas
        for area, keywords in self.knowledge_areas.items():
            if any(keyword.lower() in clean_input.lower() for keyword in keywords):
                return f"That's a great question about {{area}}! {{random.choice(self.response_templates['question'])}}"
        
        return random.choice(self.response_templates['question'])
    
    def apply_personality_filter(self, response: str) -> str:
        """Apply personality traits and advanced settings to response"""
        
        # Apply response style
        if self.response_style == "formal":
            response = response.replace("can't", "cannot").replace("won't", "will not")
        elif self.response_style == "casual":
            response = response.replace("cannot", "can't").replace("will not", "won't")
        elif self.response_style == "enthusiastic":
            if not response.endswith('!'):
                response += "!"
        
        # Apply verbosity level
        if self.verbosity_level == "concise":
            # Keep responses short
            sentences = response.split('. ')
            if len(sentences) > 2:
                response = '. '.join(sentences[:2]) + '.'
        elif self.verbosity_level == "detailed":
            # Add more context if response is too short
            if len(response.split()) < 5:
                response += " I'm happy to elaborate if you'd like more details!"
        
        # Apply emoji usage setting
        if not self.emoji_usage:
            # Remove emojis
            response = re.sub(r'[^\w\s\.,!?;:-]', '', response)
        
        # Apply creativity level (add variations for higher creativity)
        if self.creativity_level > 7:
            creative_additions = [
                " That's an interesting perspective!",
                " Let me think about that creatively...",
                " Here's a unique way to look at it:",
                " That sparks some creative ideas!"
            ]
            if random.random() < 0.3:  # 30% chance
                response += random.choice(creative_additions)
        
        return response.strip()
    
    def clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        text = text.lower().strip()
        text = re.sub(r'\\s+', ' ', text)
        text = re.sub(r'[^\\w\\s\\?\\!\\.\\,\\-]', '', text)
        return text.strip()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics"""
        base_stats = super().get_stats()
        
        base_stats.update({{
            'creation_date': self.creation_date,
            'personality_traits': len(self.personality_traits),
            'knowledge_areas': len(self.knowledge_areas),
            'custom_responses': len(self.custom_responses),
            'response_style': self.response_style,
            'learning_style': self.learning_style,
            'interaction_mode': self.interaction_mode,
            'memory_retention': self.memory_retention,
            'creativity_level': self.creativity_level,
            'verbosity_level': self.verbosity_level,
            'emoji_usage': self.emoji_usage,
            'language_preference': self.language_preference,
            'module_type': 'User-Created Bot',
            'capabilities': 'Custom Personality, Specialized Knowledge, Adaptive Learning, Advanced Configuration'
        }})
        
        return base_stats
'''
    
    return filename, module_code

def show_bot_builder():
    """Show the bot builder interface"""
    
    st.header("🛠️ AI Forge - Bot Builder")
    st.markdown("*Create your own custom AI bot with personality and knowledge*")
    
    # Enhanced header styling
    st.markdown("""
    <div style='background: linear-gradient(90deg, #ff6b6b, #4ecdc4); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
        <h4 style='color: white; margin: 0;'>🌟 AI Forge Bot Builder</h4>
        <p style='color: white; margin: 0; opacity: 0.9;'>Build powerful AI personalities with advanced customization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state - reset if needed to fix any corruption
    if 'bot_config' not in st.session_state or st.session_state.bot_config.get('specialty_area') == '':
        st.session_state.bot_config = {
            'name': '',
            'version': '1.0.0',
            'description': '',
            'personality': [],
            'greetings': [],
            'question_responses': [],
            'unknown_responses': [],
            'knowledge_areas': {},
            'custom_responses': {},
            'learning_style': 'adaptive',
            'response_style': 'friendly',
            'interaction_mode': 'conversational',
            'memory_retention': 'standard',
            'creativity_level': 5,
            'verbosity_level': 'balanced',
            'emoji_usage': True,
            'language_preference': 'auto',
            'specialty_area': 'General Knowledge',
            'conversation_starters': [],
            'mood_responses': {},
            'time_awareness': False,
            'user_preferences_learning': True
        }
    
    # Quick help section
    with st.expander("❓ How to Use the Bot Builder"):
        st.markdown("""
        ### 📋 Step-by-Step Guide:
        
        1. **📝 Basic Info**: Set your bot's name, description, and avatar
        2. **🎭 Personality**: Choose personality traits and communication style
        3. **💬 Responses**: Create custom response templates for different situations
        4. **🧠 Knowledge**: Define what your bot knows about and relevant keywords
        5. **⚙️ Custom Rules**: Add specific trigger-response pairs
        6. **🔧 Advanced Settings**: Fine-tune behavior, creativity, and interaction style
        7. **🎯 Specialization**: Set specialty areas and advanced features
        8. **🔍 Review & Build**: Preview your configuration and generate the bot
        
        ### 💡 Tips for Better Bots:
        - Add varied response templates to make conversations more natural
        - Use personality traits that match your bot's purpose
        - Create knowledge areas with relevant keywords for better responses
        - Test different creativity levels to find the right balance
        - Use custom rules for frequently asked questions
        """)
    
    # Progress indicator
    config = st.session_state.bot_config
    completed_sections = 0
    total_sections = 7
    
    if config['name'] and config['description']:
        completed_sections += 1
    if config['personality']:
        completed_sections += 1
    if config['greetings'] and config['question_responses'] and config['unknown_responses']:
        completed_sections += 1
    if config['knowledge_areas']:
        completed_sections += 1  
    if config['custom_responses']:
        completed_sections += 1
    # Advanced settings always considered complete (have defaults)
    completed_sections += 1
    # Specialization always considered complete (have defaults)
    completed_sections += 1
    
    progress = completed_sections / total_sections
    st.progress(progress)
    st.write(f"**Configuration Progress**: {completed_sections}/{total_sections} sections completed")
    
    # Configuration tabs with enhanced options
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📝 Basic Info", "🎭 Personality", "💬 Responses", 
        "🧠 Knowledge", "⚙️ Custom Rules", "🔧 Advanced Settings", 
        "🎯 Specialization", "🔍 Review & Build"
    ])
    
    with tab1:
        st.subheader("Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.bot_config['name'] = st.text_input(
                "Bot Name *",
                value=st.session_state.bot_config['name'],
                placeholder="e.g., StudyBot, MathHelper, GameMaster"
            )
            
            st.session_state.bot_config['version'] = st.text_input(
                "Version",
                value=st.session_state.bot_config['version'],
                placeholder="1.0.0"
            )
        
        with col2:
            st.session_state.bot_config['description'] = st.text_area(
                "Description *",
                value=st.session_state.bot_config['description'],
                placeholder="Describe what your bot does and its purpose...",
                height=100
            )
        
        # Bot icon/avatar selection
        st.subheader("🎨 Bot Avatar")
        avatar_options = ["🤖", "🦾", "🧠", "⚡", "🌟", "🔥", "💎", "🚀", "🎯", "🛡️", "👑", "🦄"]
        st.session_state.bot_config['avatar'] = st.selectbox(
            "Choose an avatar for your bot:",
            avatar_options,
            index=avatar_options.index(st.session_state.bot_config.get('avatar', '🤖'))
        )
        
        # Bot category
        category_options = ["General Assistant", "Educational", "Creative", "Technical", "Entertainment", "Specialized"]
        current_category = st.session_state.bot_config.get('category', 'General Assistant')
        try:
            category_index = category_options.index(current_category)
        except ValueError:
            category_index = 0
        
        st.session_state.bot_config['category'] = st.selectbox(
            "Bot Category:",
            category_options,
            index=category_index
        )
        
        if st.session_state.bot_config['name'] and st.session_state.bot_config['description']:
            st.success("✅ Basic information complete!")
        else:
            st.warning("⚠️ Please fill in the required fields (marked with *)")
    
    with tab2:
        st.subheader("Personality & Style")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personality Traits**")
            personality_options = [
                "helpful", "curious", "analytical", "creative", "patient", 
                "enthusiastic", "professional", "humorous", "empathetic", "logical"
            ]
            
            selected_traits = st.multiselect(
                "Select personality traits:",
                personality_options,
                default=st.session_state.bot_config['personality']
            )
            st.session_state.bot_config['personality'] = selected_traits
            
            response_styles = ["friendly", "formal", "casual", "enthusiastic", "professional"]
            current_style = st.session_state.bot_config.get('response_style', 'friendly')
            try:
                style_index = response_styles.index(current_style)
            except ValueError:
                style_index = 0
            
            st.session_state.bot_config['response_style'] = st.selectbox(
                "Response Style:",
                response_styles,
                index=style_index
            )
        
        with col2:
            st.write("**Learning Style**")
            learning_styles = ["adaptive", "conservative", "aggressive", "balanced"]
            current_learning = st.session_state.bot_config.get('learning_style', 'adaptive')
            try:
                learning_index = learning_styles.index(current_learning)
            except ValueError:
                learning_index = 0
            
            st.session_state.bot_config['learning_style'] = st.selectbox(
                "How should your bot learn?",
                learning_styles,
                index=learning_index
            )
            
            st.info("""
            **Learning Styles:**
            - **Adaptive**: Learns quickly from user feedback
            - **Conservative**: Learns slowly but with high confidence
            - **Aggressive**: Learns rapidly from all interactions
            - **Balanced**: Moderate learning pace with good accuracy
            """)
        
        if selected_traits:
            st.success(f"✅ Personality configured: {', '.join(selected_traits)}")
    
    with tab3:
        st.subheader("Response Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Greeting Messages**")
            greetings_text = st.text_area(
                "Enter greeting messages (one per line):",
                value='\n'.join(st.session_state.bot_config['greetings']),
                placeholder="Hello! How can I help you today?\nHi there! What would you like to know?\nGreetings! I'm here to assist you.",
                height=120
            )
            if greetings_text.strip():
                st.session_state.bot_config['greetings'] = [line.strip() for line in greetings_text.split('\n') if line.strip()]
            
            st.write("**Question Responses**")
            questions_text = st.text_area(
                "Enter question response templates:",
                value='\n'.join(st.session_state.bot_config['question_responses']),
                placeholder="That's an interesting question!\nLet me help you with that.\nI can assist you with this topic.",
                height=120
            )
            if questions_text.strip():
                st.session_state.bot_config['question_responses'] = [line.strip() for line in questions_text.split('\n') if line.strip()]
        
        with col2:
            st.write("**Unknown Input Responses**")
            unknown_text = st.text_area(
                "Enter responses for unknown inputs:",
                value='\n'.join(st.session_state.bot_config['unknown_responses']),
                placeholder="I'm not sure about that. Could you clarify?\nThat's interesting! Can you tell me more?\nI'd like to help, but I need more information.",
                height=120
            )
            if unknown_text.strip():
                st.session_state.bot_config['unknown_responses'] = [line.strip() for line in unknown_text.split('\n') if line.strip()]
            
            st.info("💡 **Tip**: Create varied responses to make your bot more natural")
        
        if (st.session_state.bot_config['greetings'] and 
            st.session_state.bot_config['question_responses'] and 
            st.session_state.bot_config['unknown_responses']):
            st.success("✅ Response templates configured!")
    
    with tab4:
        st.subheader("Knowledge Areas")
        st.markdown("Define what your bot knows about and relevant keywords")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_area = st.text_input("Knowledge Area:", key="knowledge_area_input")
            new_keywords = st.text_input("Keywords (comma-separated):", key="keywords_input")
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("Add Knowledge Area", use_container_width=True):
                if new_area and new_keywords:
                    keywords_list = [kw.strip() for kw in new_keywords.split(',') if kw.strip()]
                    st.session_state.bot_config['knowledge_areas'][new_area] = keywords_list
                    st.success(f"Added knowledge area: {new_area}")
                    st.rerun()
        
        # Display current knowledge areas
        if st.session_state.bot_config['knowledge_areas']:
            st.write("**Current Knowledge Areas**")
            for area, keywords in st.session_state.bot_config['knowledge_areas'].items():
                col_area, col_keywords, col_remove = st.columns([2, 4, 1])
                with col_area:
                    st.write(f"**{area}**")
                with col_keywords:
                    st.write(f"Keywords: {', '.join(keywords)}")
                with col_remove:
                    if st.button("🗑️", key=f"remove_{area}"):
                        del st.session_state.bot_config['knowledge_areas'][area]
                        st.rerun()
        
        if st.session_state.bot_config['knowledge_areas']:
            st.success("✅ Knowledge areas configured!")
    
    with tab5:
        st.subheader("Custom Response Rules")
        st.markdown("Create specific trigger-response pairs for your bot")
        
        col1, col2 = st.columns([2, 2])
        
        with col1:
            trigger_input = st.text_input("Trigger phrase:", key="trigger_input")
        
        with col2:
            response_input = st.text_input("Response:", key="response_input")
        
        col3, col4 = st.columns([1, 3])
        with col3:
            if st.button("Add Rule", use_container_width=True):
                if trigger_input and response_input:
                    st.session_state.bot_config['custom_responses'][trigger_input] = response_input
                    st.success(f"Added rule: {trigger_input} → {response_input}")
                    st.rerun()
        
        # Display current custom rules
        if st.session_state.bot_config['custom_responses']:
            st.write("**Current Custom Rules**")
            for trigger, response in st.session_state.bot_config['custom_responses'].items():
                col_trigger, col_response, col_remove = st.columns([2, 4, 1])
                with col_trigger:
                    st.write(f"**{trigger}**")
                with col_response:
                    st.write(response)
                with col_remove:
                    if st.button("🗑️", key=f"remove_rule_{trigger}"):
                        del st.session_state.bot_config['custom_responses'][trigger]
                        st.rerun()
        
        st.info("💡 **Example**: Trigger: 'how old are you' → Response: 'I was created recently and I'm always learning!'")
    
    with tab6:
        st.subheader("Advanced Bot Configuration")
        st.markdown("Fine-tune your bot's behavior and capabilities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Interaction Settings**")
            interaction_modes = ["conversational", "professional", "educational", "creative", "analytical"]
            current_mode = st.session_state.bot_config.get('interaction_mode', 'conversational')
            try:
                mode_index = interaction_modes.index(current_mode)
            except ValueError:
                mode_index = 0
            
            st.session_state.bot_config['interaction_mode'] = st.selectbox(
                "Interaction Mode:",
                interaction_modes,
                index=mode_index
            )
            
            memory_options = ["minimal", "standard", "enhanced", "comprehensive"]
            current_memory = st.session_state.bot_config.get('memory_retention', 'standard')
            try:
                memory_index = memory_options.index(current_memory)
            except ValueError:
                memory_index = 1  # Default to 'standard'
            
            st.session_state.bot_config['memory_retention'] = st.selectbox(
                "Memory Retention:",
                memory_options,
                index=memory_index
            )
            
            verbosity_options = ["concise", "balanced", "detailed", "comprehensive"]
            current_verbosity = st.session_state.bot_config.get('verbosity_level', 'balanced')
            try:
                verbosity_index = verbosity_options.index(current_verbosity)
            except ValueError:
                verbosity_index = 1  # Default to 'balanced'
            
            st.session_state.bot_config['verbosity_level'] = st.selectbox(
                "Response Length:",
                verbosity_options,
                index=verbosity_index
            )
        
        with col2:
            st.write("**Personality Adjustments**")
            st.session_state.bot_config['creativity_level'] = st.slider(
                "Creativity Level (1-10):",
                min_value=1,
                max_value=10,
                value=st.session_state.bot_config['creativity_level'],
                help="Higher values make responses more creative and varied"
            )
            
            st.session_state.bot_config['emoji_usage'] = st.checkbox(
                "Use Emojis in Responses",
                value=st.session_state.bot_config['emoji_usage']
            )
            
            st.session_state.bot_config['time_awareness'] = st.checkbox(
                "Time-Aware Responses",
                value=st.session_state.bot_config['time_awareness'],
                help="Bot will adjust responses based on time of day"
            )
            
            st.session_state.bot_config['user_preferences_learning'] = st.checkbox(
                "Learn User Preferences",
                value=st.session_state.bot_config['user_preferences_learning'],
                help="Bot will remember user preferences over time"
            )
        
        # Language and Communication
        st.write("**Language & Communication**")
        col3, col4 = st.columns(2)
        
        with col3:
            language_options = ["auto", "english", "czech", "spanish", "french", "german", "italian", "portuguese"]
            current_language = st.session_state.bot_config.get('language_preference', 'auto')
            try:
                language_index = language_options.index(current_language)
            except ValueError:
                language_index = 0  # Default to 'auto'
            
            st.session_state.bot_config['language_preference'] = st.selectbox(
                "Primary Language:",
                language_options,
                index=language_index
            )
        
        with col4:
            communication_styles = st.multiselect(
                "Communication Styles:",
                ["friendly", "formal", "humorous", "supportive", "direct", "patient", "encouraging"],
                default=st.session_state.bot_config.get('communication_styles', ['friendly'])
            )
            st.session_state.bot_config['communication_styles'] = communication_styles
        
        st.success("⚙️ Advanced settings configured!")
    
    with tab7:
        st.subheader("Bot Specialization & Advanced Features")
        st.markdown("Configure specialized capabilities for your bot")
        
        # Specialty Area
        st.write("**Specialty Area**")
        specialty_options = [
            "General Knowledge", "Mathematics", "Science", "Technology", "History", 
            "Literature", "Arts", "Music", "Sports", "Gaming", "Cooking", "Travel",
            "Health & Fitness", "Business", "Psychology", "Philosophy", "Languages"
        ]
        current_specialty = st.session_state.bot_config.get('specialty_area', 'General Knowledge')
        try:
            specialty_index = specialty_options.index(current_specialty)
        except ValueError:
            specialty_index = 0  # Default to first option if current value not found
        
        st.session_state.bot_config['specialty_area'] = st.selectbox(
            "Choose your bot's main specialty:",
            specialty_options,
            index=specialty_index
        )
        
        # Conversation Starters
        st.write("**Conversation Starters**")
        starters_text = st.text_area(
            "Add conversation starters (one per line):",
            value='\n'.join(st.session_state.bot_config.get('conversation_starters', [])),
            placeholder="What would you like to learn today?\nI'm here to help with any questions!\nLet's explore something interesting together!",
            height=100
        )
        if starters_text.strip():
            st.session_state.bot_config['conversation_starters'] = [line.strip() for line in starters_text.split('\n') if line.strip()]
        
        # Mood-based responses
        st.write("**Mood-Based Responses**")
        col1, col2 = st.columns(2)
        
        mood_options = ["happy", "sad", "excited", "confused", "frustrated", "curious"]
        
        for i, mood in enumerate(mood_options):
            with col1 if i % 2 == 0 else col2:
                mood_response = st.text_input(
                    f"Response when user seems {mood}:",
                    value=st.session_state.bot_config.get('mood_responses', {}).get(mood, ''),
                    placeholder=f"How to respond when user is {mood}..."
                )
                if mood_response:
                    if 'mood_responses' not in st.session_state.bot_config:
                        st.session_state.bot_config['mood_responses'] = {}
                    st.session_state.bot_config['mood_responses'][mood] = mood_response
        
        # Special capabilities
        st.write("**Special Capabilities**")
        capabilities = st.multiselect(
            "Enable special features:",
            [
                "Mathematical calculations", "Text analysis", "Creative writing", 
                "Problem solving", "Brainstorming", "Study assistance", 
                "Code explanation", "Language translation help", "Storytelling"
            ],
            default=st.session_state.bot_config.get('special_capabilities', [])
        )
        st.session_state.bot_config['special_capabilities'] = capabilities
        
        if st.session_state.bot_config.get('specialty_area') != 'General Knowledge':
            st.success(f"🎯 Bot specialized in: {st.session_state.bot_config['specialty_area']}")
    
    with tab8:
        st.subheader("Review & Build Your Bot")
        
        config = st.session_state.bot_config
        
        # Enhanced Configuration Display
        st.markdown("### 🤖 Your Bot Preview")
        
        # Bot preview card
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                st.markdown(f"## {config.get('avatar', '🤖')}")
                st.write(f"**{config['name']}**")
                st.write(f"v{config['version']}")
            
            with col2:
                st.write("**Basic Information**")
                st.write(f"📝 **Description**: {config['description']}")
                st.write(f"🏷️ **Category**: {config.get('category', 'General Assistant')}")
                st.write(f"🎯 **Specialty**: {config.get('specialty_area', 'General Knowledge')}")
                st.write(f"🎭 **Personality**: {', '.join(config['personality']) if config['personality'] else 'None set'}")
            
            with col3:
                st.write("**Advanced Settings**")
                st.write(f"🔧 **Interaction Mode**: {config.get('interaction_mode', 'conversational')}")
                st.write(f"🧠 **Memory**: {config.get('memory_retention', 'standard')}")
                st.write(f"💬 **Response Style**: {config['response_style']}")
                st.write(f"🎨 **Creativity Level**: {config.get('creativity_level', 5)}/10")
                st.write(f"🌐 **Language**: {config.get('language_preference', 'auto')}")
        
        st.markdown("### 📊 Configuration Summary")
        
        # Configuration metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Greetings", len(config.get('greetings', [])))
            st.metric("Question Templates", len(config.get('question_responses', [])))
        
        with col2:
            st.metric("Unknown Responses", len(config.get('unknown_responses', [])))
            st.metric("Knowledge Areas", len(config.get('knowledge_areas', {})))
        
        with col3:
            st.metric("Custom Rules", len(config.get('custom_responses', {})))
            st.metric("Conversation Starters", len(config.get('conversation_starters', [])))
        
        with col4:
            st.metric("Mood Responses", len(config.get('mood_responses', {})))
            st.metric("Special Capabilities", len(config.get('special_capabilities', [])))
        
        # Detailed configuration view
        with st.expander("🔍 Detailed Configuration Review"):
            st.json({
                "Basic Info": {
                    "name": config['name'],
                    "version": config['version'],
                    "description": config['description'],
                    "avatar": config.get('avatar', '🤖'),
                    "category": config.get('category', 'General Assistant')
                },
                "Personality": {
                    "traits": config['personality'],
                    "response_style": config['response_style'],
                    "learning_style": config['learning_style'],
                    "communication_styles": config.get('communication_styles', [])
                },
                "Advanced Settings": {
                    "interaction_mode": config.get('interaction_mode', 'conversational'),
                    "memory_retention": config.get('memory_retention', 'standard'),
                    "creativity_level": config.get('creativity_level', 5),
                    "verbosity_level": config.get('verbosity_level', 'balanced'),
                    "emoji_usage": config.get('emoji_usage', True),
                    "time_awareness": config.get('time_awareness', False)
                },
                "Specialization": {
                    "specialty_area": config.get('specialty_area', 'General Knowledge'),
                    "special_capabilities": config.get('special_capabilities', [])
                }
            })
        
        # Validation
        is_valid = (
            config['name'] and 
            config['description'] and 
            config['greetings'] and 
            config['question_responses'] and 
            config['unknown_responses']
        )
        
        if is_valid:
            st.success("✅ Configuration is complete and ready to build!")
            
            if st.button("🚀 Build My Bot", type="primary", use_container_width=True):
                try:
                    # Generate the bot module
                    filename, module_code = generate_bot_module(config)
                    
                    # Save to moduls directory
                    moduls_dir = Path("moduls")
                    moduls_dir.mkdir(exist_ok=True)
                    
                    module_path = moduls_dir / filename
                    
                    with open(module_path, 'w', encoding='utf-8') as f:
                        f.write(module_code)
                    
                    # Success display with enhanced styling
                    st.balloons()
                    st.success(f"🎉 Bot '{config['name']}' has been created successfully!")
                    
                    # Enhanced success information
                    success_col1, success_col2 = st.columns(2)
                    with success_col1:
                        st.info(f"📁 **Module saved as**: `{filename}`")
                        st.info(f"🤖 **Bot Name**: {config['name']}")
                        st.info(f"⚡ **Version**: {config['version']}")
                    
                    with success_col2:
                        st.info(f"🎯 **Specialty**: {config.get('specialty_area', 'General Knowledge')}")
                        st.info(f"🎭 **Personality Traits**: {len(config['personality'])}")
                        st.info(f"🧠 **Knowledge Areas**: {len(config.get('knowledge_areas', {}))}")
                    
                    st.markdown("---")
                    st.markdown("### 🚀 Next Steps")
                    st.markdown("1. Go back to the main Chat-PC page")
                    st.markdown("2. Click 'Refresh Modules' to load your new bot")
                    st.markdown("3. Select your bot from the dropdown and start chatting!")
                    
                    # Action buttons
                    button_col1, button_col2, button_col3 = st.columns(3)
                    
                    with button_col1:
                        # Option to download the module
                        st.download_button(
                            label="📥 Download Bot Module",
                            data=module_code,
                            file_name=filename,
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with button_col2:
                        # Reset configuration for new bot
                        if st.button("🆕 Create Another Bot", use_container_width=True):
                            st.session_state.bot_config = {
                                'name': '',
                                'version': '1.0.0',
                                'description': '',
                                'personality': [],
                                'greetings': [],
                                'question_responses': [],
                                'unknown_responses': [],
                                'knowledge_areas': {},
                                'custom_responses': {},
                                'learning_style': 'adaptive',
                                'response_style': 'friendly',
                                'interaction_mode': 'conversational',
                                'memory_retention': 'standard',
                                'creativity_level': 5,
                                'verbosity_level': 'balanced',
                                'emoji_usage': True,
                                'language_preference': 'auto',
                                'specialty_area': 'General Knowledge',
                                'conversation_starters': [],
                                'mood_responses': {},
                                'time_awareness': False,
                                'user_preferences_learning': True
                            }
                            st.rerun()
                    
                    with button_col3:
                        # Quick test button
                        if st.button("🧪 Test Bot Responses", use_container_width=True):
                            st.markdown("### 🧪 Quick Response Test")
                            test_inputs = ["Hello!", "What can you help me with?", "Thank you!", "Goodbye!"]
                            for test_input in test_inputs:
                                st.write(f"**User**: {test_input}")
                                # Simple response simulation based on config
                                if "hello" in test_input.lower():
                                    response = config['greetings'][0] if config['greetings'] else "Hello there!"
                                elif "help" in test_input.lower():
                                    response = config['question_responses'][0] if config['question_responses'] else "I'm here to help!"
                                elif "thank" in test_input.lower():
                                    response = "You're welcome!"
                                else:
                                    response = config['unknown_responses'][0] if config['unknown_responses'] else "I'm not sure about that."
                                st.write(f"**{config['name']}**: {response}")
                                st.write("---")
                    
                except Exception as e:
                    st.error(f"❌ Error creating bot: {str(e)}")
        
        else:
            st.warning("⚠️ Please complete all required configuration steps before building your bot.")
            missing_items = []
            if not config['name']: missing_items.append("Bot Name")
            if not config['description']: missing_items.append("Description") 
            if not config['greetings']: missing_items.append("Greeting Messages")
            if not config['question_responses']: missing_items.append("Question Response Templates")
            if not config['unknown_responses']: missing_items.append("Unknown Input Responses")
            
            st.write("**Missing required items:**")
            for item in missing_items:
                st.write(f"- {item}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Bot Builder - Chat-PC",
        page_icon="🤖",
        layout="wide"
    )
    show_bot_builder()