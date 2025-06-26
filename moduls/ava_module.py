import random
import string
import re
import math
import statistics
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))
from base_module import BaseAIModule

class AIModule(BaseAIModule):
    """A.v.A - Advanced virtual Assistant module"""
    
    name = "A.v.A"
    version = "3.0.0"
    description = "Advanced virtual Assistant with sophisticated AI-like reasoning, natural language understanding, and adaptive learning - fully local, no external APIs"
    
    def __init__(self):
        super().__init__()
        
        # Enhanced response templates
        self.response_templates = {
            'greeting': [
                "Hello! How can I assist you today?",
                "Hi there! What would you like to know or discuss?",
                "Good day! I'm here to help with any questions or tasks.",
                "Welcome! How may I be of service?",
                "Greetings! What can I help you with?"
            ],
            'question': [
                "That's an interesting question. Based on my analysis, {}",
                "Let me think about this carefully. I believe {}",
                "From what I understand, {} seems to be the most likely answer.",
                "After considering the factors, {}",
                "This is a good question. My reasoning suggests that {}"
            ],
            'calculation': [
                "Let me calculate that for you: {}",
                "Based on my calculations: {}",
                "The mathematical result is: {}",
                "After computing this: {}",
                "The answer to your calculation is: {}"
            ],
            'analysis': [
                "After analyzing the information: {}",
                "My detailed analysis shows: {}",
                "Breaking this down systematically: {}",
                "Based on the data patterns: {}",
                "From a logical perspective: {}"
            ],
            'unknown': [
                "I'm not entirely sure about that. Could you provide more context?",
                "That's interesting, but I need more information to give you a proper answer.",
                "I'd like to help, but could you clarify what you're asking?",
                "That's outside my current knowledge. Can you explain it differently?",
                "I'm still learning about that topic. Could you be more specific?"
            ],
            'thanks': [
                "You're welcome! Happy to help anytime.",
                "Glad I could assist! Feel free to ask if you need anything else.",
                "My pleasure! That's what I'm here for.",
                "No problem at all! Always ready to help.",
                "It was my pleasure helping you!"
            ],
            'goodbye': [
                "Goodbye! Have a wonderful day!",
                "See you later! Take care!",
                "Until next time! Stay well!",
                "Farewell! Hope to chat again soon!",
                "Goodbye! Wishing you all the best!"
            ],
            'learning': [
                "I'm learning from our conversation. This helps me provide better responses.",
                "Thank you for teaching me something new. I'll remember this.",
                "This is valuable information that I'll incorporate into my knowledge.",
                "I appreciate the feedback - it helps me improve my responses.",
                "Each conversation helps me become more helpful. Thank you!"
            ]
        }
        
        # Enhanced pattern recognition
        self.patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings'],
            'question': ['?', 'what', 'how', 'when', 'where', 'why', 'who', 'which', 'can you', 'do you', 'are you'],
            'calculation': ['calculate', 'compute', 'math', 'add', 'subtract', 'multiply', 'divide', 'plus', 'minus', 'times', 'divided by', '=', '+', '-', '*', '/', 'sum', 'total', 'average', 'percentage'],
            'analysis': ['analyze', 'compare', 'evaluate', 'assess', 'examine', 'review', 'consider', 'think about'],
            'thanks': ['thank you', 'thanks', 'appreciate', 'grateful', 'much appreciated'],
            'goodbye': ['goodbye', 'bye', 'see you', 'farewell', 'until next time', 'take care'],
            'learning': ['learn', 'teach', 'remember', 'understand', 'know', 'explain', 'show me']
        }
        
        # Mathematical operations support
        self.math_operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else "Cannot divide by zero",
            'power': lambda x, y: x ** y,
            'sqrt': lambda x: math.sqrt(x) if x >= 0 else "Cannot compute square root of negative number",
            'factorial': lambda x: math.factorial(int(x)) if x >= 0 and x == int(x) else "Factorial only works with non-negative integers"
        }
        
        # Enhanced knowledge base with deeper reasoning
        self.knowledge_domains = {
            'science': {
                'keywords': ['physics', 'chemistry', 'biology', 'astronomy', 'geology', 'atom', 'molecule', 'cell', 'DNA', 'evolution', 'gravity', 'energy'],
                'reasoning': 'Scientific topics require logical analysis and evidence-based thinking',
                'responses': [
                    "From a scientific perspective, this involves fundamental principles of {}",
                    "The scientific method suggests we should examine {} systematically",
                    "This relates to scientific concepts involving {}"
                ]
            },
            'technology': {
                'keywords': ['computer', 'programming', 'software', 'hardware', 'internet', 'ai', 'machine learning', 'algorithm', 'data', 'code', 'digital'],
                'reasoning': 'Technology topics involve logical systems and problem-solving approaches',
                'responses': [
                    "In technological terms, {} represents a systematic approach to problem-solving",
                    "From a computational perspective, {} involves logical processes",
                    "This technology concept relates to {}"
                ]
            },
            'mathematics': {
                'keywords': ['algebra', 'geometry', 'calculus', 'statistics', 'probability', 'equation', 'formula', 'number', 'calculate'],
                'reasoning': 'Mathematical concepts follow logical rules and patterns',
                'responses': [
                    "Mathematically speaking, {} follows logical patterns and rules",
                    "The mathematical approach to {} involves systematic reasoning",
                    "From a mathematical standpoint, {} can be analyzed logically"
                ]
            },
            'philosophy': {
                'keywords': ['think', 'meaning', 'purpose', 'existence', 'consciousness', 'mind', 'reality', 'truth', 'ethics', 'morality'],
                'reasoning': 'Philosophical questions require deep contemplation and multiple perspectives',
                'responses': [
                    "This philosophical question about {} invites deep contemplation",
                    "From a philosophical perspective, {} raises interesting questions about existence and meaning",
                    "The philosophical implications of {} touch on fundamental questions"
                ]
            },
            'psychology': {
                'keywords': ['behavior', 'emotion', 'feeling', 'memory', 'learning', 'personality', 'motivation', 'stress', 'happiness'],
                'reasoning': 'Human psychology involves complex patterns of thought and behavior',
                'responses': [
                    "From a psychological perspective, {} relates to human behavior and cognition",
                    "This touches on psychological concepts involving {}",
                    "The psychological aspects of {} involve complex mental processes"
                ]
            }
        }
        
        # Reasoning patterns for AI-like responses
        self.reasoning_patterns = {
            'cause_effect': ['because', 'since', 'therefore', 'as a result', 'consequently'],
            'comparison': ['similar to', 'different from', 'like', 'unlike', 'compared to'],
            'analysis': ['analyzing', 'examining', 'considering', 'evaluating', 'breaking down'],
            'synthesis': ['combining', 'integrating', 'merging', 'connecting', 'relating'],
            'hypothesis': ['possibly', 'might be', 'could be', 'perhaps', 'potentially']
        }
        
        # Memory for conversation context and personality
        self.conversation_memory = {
            'user_preferences': {},
            'discussed_topics': [],
            'personality_traits': ['curious', 'analytical', 'helpful', 'thoughtful'],
            'reasoning_style': 'logical_and_intuitive'
        }
    
    def generate_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate AI-like response using sophisticated local reasoning"""
        
        # Update conversation memory
        self.update_conversation_context(user_input, chat_history)
        
        # First, try advanced learned response matching
        learned_response = self.find_intelligent_learned_response(user_input)
        if learned_response:
            return self.add_reasoning_layer(learned_response, user_input)
        
        # Clean and analyze input with AI-like preprocessing
        clean_input = self.clean_input(user_input)
        
        # Check for mathematical calculations with reasoning
        calc_result = self.try_calculate(clean_input)
        if calc_result:
            reasoning = self.generate_calculation_reasoning(user_input, calc_result)
            response = f"{reasoning} {calc_result}"
            self.learn_from_conversation(user_input, response, confidence=0.95)
            return response
        
        # Multi-layer intent detection with reasoning
        primary_intent = self.detect_intent(clean_input)
        reasoning_type = self.detect_reasoning_pattern(clean_input)
        domain = self.identify_advanced_domain(clean_input)
        
        # Generate AI-like response with multi-layer reasoning
        response = self.generate_ai_like_response(
            primary_intent, reasoning_type, domain, clean_input, chat_history, user_input
        )
        
        # Advanced learning with contextual confidence
        confidence = self.calculate_advanced_confidence(
            primary_intent, reasoning_type, domain, clean_input, chat_history
        )
        self.learn_from_conversation(user_input, response, confidence=confidence)
        
        return response
    
    def try_calculate(self, text: str) -> str:
        """Try to perform mathematical calculations"""
        # Extract numbers and operations
        numbers = re.findall(r'-?\d+\.?\d*', text)
        
        # Need at least one or two numbers depending on operation
        if len(numbers) < 1:
            return ""
        
        try:
            nums = [float(n) for n in numbers]
            
            # Check for specific calculation patterns
            text_lower = text.lower()
            
            # Addition
            if any(op in text_lower for op in ['plus', '+', 'add']) and len(nums) >= 2:
                result = nums[0] + nums[1]
                return f"{numbers[0]} + {numbers[1]} = {result}"
            
            # Subtraction  
            elif any(op in text_lower for op in ['minus', '-', 'subtract']) and len(nums) >= 2:
                result = nums[0] - nums[1]
                return f"{numbers[0]} - {numbers[1]} = {result}"
            
            # Multiplication
            elif any(op in text_lower for op in ['times', '*', 'multiply', 'x']) and len(nums) >= 2:
                result = nums[0] * nums[1]
                return f"{numbers[0]} × {numbers[1]} = {result}"
            
            # Division
            elif any(op in text_lower for op in ['divided by', '/', 'divide']) and len(nums) >= 2:
                if nums[1] != 0:
                    result = nums[0] / nums[1]
                    return f"{numbers[0]} ÷ {numbers[1]} = {result:.4f}"
                else:
                    return "Cannot divide by zero"
            
            # Power
            elif any(op in text_lower for op in ['power', '**', '^', 'to the power']) and len(nums) >= 2:
                result = nums[0] ** nums[1]
                return f"{numbers[0]} to the power of {numbers[1]} = {result}"
            
            # Average/Mean
            elif any(op in text_lower for op in ['average', 'mean']) and len(nums) >= 2:
                result = statistics.mean(nums)
                return f"Average of {', '.join(numbers)} = {result:.4f}"
            
            # Sum/Total
            elif any(op in text_lower for op in ['sum', 'total']) and len(nums) >= 2:
                result = sum(nums)
                return f"Sum of {', '.join(numbers)} = {result}"
            
            # Square root
            elif any(op in text_lower for op in ['square root', 'sqrt']) and len(nums) >= 1:
                if nums[0] >= 0:
                    result = math.sqrt(nums[0])
                    return f"Square root of {numbers[0]} = {result:.4f}"
                else:
                    return "Cannot compute square root of negative number"
            
            # Factorial
            elif 'factorial' in text_lower and len(nums) >= 1:
                if nums[0] >= 0 and nums[0] == int(nums[0]) and nums[0] <= 20:
                    result = math.factorial(int(nums[0]))
                    return f"Factorial of {int(numbers[0])} = {result}"
                else:
                    return "Factorial only works with non-negative integers up to 20"
            
            # Simple math expressions like "what is 5 + 3"
            elif 'what is' in text_lower and len(nums) >= 2:
                if '+' in text or 'plus' in text_lower:
                    result = nums[0] + nums[1]
                    return f"{numbers[0]} + {numbers[1]} = {result}"
                elif '-' in text or 'minus' in text_lower:
                    result = nums[0] - nums[1]
                    return f"{numbers[0]} - {numbers[1]} = {result}"
                elif '*' in text or 'times' in text_lower:
                    result = nums[0] * nums[1]
                    return f"{numbers[0]} × {numbers[1]} = {result}"
                elif '/' in text or 'divided' in text_lower:
                    if nums[1] != 0:
                        result = nums[0] / nums[1]
                        return f"{numbers[0]} ÷ {numbers[1]} = {result:.4f}"
                    else:
                        return "Cannot divide by zero"
            
        except (ValueError, OverflowError) as e:
            return f"Calculation error: {str(e)}"
        
        return ""
    
    def detect_intent(self, text: str) -> str:
        """Enhanced intent detection with weighted scoring"""
        text_lower = text.lower()
        intent_scores = {}
        
        # Score each intent based on keyword matches
        for intent, keywords in self.patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Weight longer keywords more heavily
                    score += len(keyword.split())
            intent_scores[intent] = score
        
        # Find the highest scoring intent
        if intent_scores:
            best_intent = ""
            best_score = -1
            for intent, score in intent_scores.items():
                if score > best_score:
                    best_score = score
                    best_intent = intent
            if best_score > 0:
                return best_intent
        
        # Check for domain-specific questions
        for domain, terms in self.knowledge_domains.items():
            if any(term in text_lower for term in terms):
                return 'analysis'
        
        return 'unknown'
    
    def generate_enhanced_response(self, intent: str, clean_input: str, chat_history: List[Dict], original_input: str) -> str:
        """Generate enhanced contextual responses"""
        
        if intent == 'greeting':
            return random.choice(self.response_templates['greeting'])
        
        elif intent == 'question':
            return self.generate_intelligent_question_response(clean_input, chat_history)
        
        elif intent == 'analysis':
            return self.generate_analysis_response(clean_input, chat_history)
        
        elif intent == 'thanks':
            return random.choice(self.response_templates['thanks'])
        
        elif intent == 'goodbye':
            return random.choice(self.response_templates['goodbye'])
        
        elif intent == 'learning':
            return random.choice(self.response_templates['learning'])
        
        else:
            return self.generate_contextual_unknown_response(clean_input, chat_history)
    
    def generate_intelligent_question_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate intelligent responses to questions"""
        
        # Handle specific question types first
        user_lower = user_input.lower()
        
        # Identity questions
        if any(phrase in user_lower for phrase in ['who are you', 'what are you', 'you ava']):
            return "I'm A.v.A (Advanced virtual Assistant), a local AI module designed to help with calculations, analysis, and conversation. I can learn from our interactions to provide better responses over time."
        
        # Capability questions
        if any(phrase in user_lower for phrase in ['what can you do', 'your capabilities', 'help me']):
            return "I can help with mathematical calculations, answer questions, analyze information, and learn from our conversations. Try asking me to calculate something like '15 + 27' or ask me about topics in science, technology, or other subjects."
        
        # Simple questions with obvious answers
        if user_lower.strip() in ['what', 'what?']:
            return "I'd love to help, but could you elaborate on what you're looking for? I can assist with calculations, answer questions, or discuss various topics."
        
        # Extract key concepts and context
        concepts = self.extract_enhanced_concepts(user_input)
        context = self.analyze_conversation_context(chat_history)
        
        if concepts:
            # Generate response based on concepts and knowledge domains
            domain = self.identify_knowledge_domain(concepts)
            if domain:
                concept_text = self.generate_domain_response(domain, concepts, context)
            else:
                concept_text = self.combine_concepts_intelligently(concepts, context)
            
            template = random.choice(self.response_templates['question'])
            return template.format(concept_text)
        else:
            return self.generate_contextual_unknown_response(user_input, chat_history)
    
    def generate_analysis_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate analytical responses"""
        
        concepts = self.extract_enhanced_concepts(user_input)
        analysis = self.perform_basic_analysis(concepts, chat_history)
        
        template = random.choice(self.response_templates['analysis'])
        return template.format(analysis)
    
    def calculate_response_confidence(self, intent: str, clean_input: str, chat_history: List[Dict]) -> float:
        """Calculate confidence score for response quality"""
        
        base_confidence = 0.5
        
        # Boost confidence for specific intents
        intent_confidence = {
            'greeting': 0.9,
            'thanks': 0.9,
            'goodbye': 0.9,
            'calculation': 0.95,
            'question': 0.7,
            'analysis': 0.6,
            'learning': 0.8,
            'unknown': 0.3
        }
        
        confidence = intent_confidence.get(intent, base_confidence)
        
        # Adjust based on input complexity
        word_count = len(clean_input.split())
        if word_count > 10:
            confidence += 0.1  # Longer inputs provide more context
        
        # Adjust based on conversation history
        if len(chat_history) > 5:
            confidence += 0.05  # More context from longer conversations
        
        return min(confidence, 1.0)
    
    def extract_enhanced_concepts(self, text: str) -> List[str]:
        """Enhanced concept extraction with better filtering"""
        
        # Expanded stop words
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'this', 'but', 'they',
            'have', 'had', 'what', 'said', 'each', 'which', 'their', 'time',
            'can', 'could', 'would', 'should', 'may', 'might', 'must',
            'do', 'does', 'did', 'get', 'got', 'go', 'went', 'come', 'came',
            'see', 'saw', 'look', 'make', 'made', 'take', 'took', 'give', 'gave'
        }
        
        # Extract words and phrases
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        concepts = []
        
        # Single words
        for word in words:
            if len(word) > 2 and word not in stop_words:
                concepts.append(word)
        
        # Bigrams (two-word phrases)
        for i in range(len(words) - 1):
            if words[i] not in stop_words and words[i+1] not in stop_words:
                if len(words[i]) > 2 and len(words[i+1]) > 2:
                    concepts.append(f"{words[i]} {words[i+1]}")
        
        # Remove duplicates and return top concepts
        concepts = list(set(concepts))
        return concepts[:8]
    
    def identify_knowledge_domain(self, concepts: List[str]) -> str:
        """Identify the knowledge domain of the concepts"""
        
        domain_scores = {}
        
        for domain, terms in self.knowledge_domains.items():
            score = 0
            for concept in concepts:
                for term in terms:
                    if term in concept or concept in term:
                        score += 1
            domain_scores[domain] = score
        
        if domain_scores:
            best_domain = ""
            best_score = -1
            for domain, score in domain_scores.items():
                if score > best_score:
                    best_score = score
                    best_domain = domain
            if best_score > 0:
                return best_domain
        
        return ""
    
    def generate_domain_response(self, domain: str, concepts: List[str], context: Dict) -> str:
        """Generate domain-specific responses"""
        
        domain_responses = {
            'science': f"this relates to scientific principles involving {', '.join(concepts[:3])}",
            'technology': f"from a technological perspective, {', '.join(concepts[:3])} are interconnected",
            'mathematics': f"mathematically speaking, {', '.join(concepts[:3])} follow logical patterns",
            'history': f"historically, {', '.join(concepts[:3])} have played significant roles",
            'geography': f"geographically, {', '.join(concepts[:3])} are important factors",
            'arts': f"in the arts, {', '.join(concepts[:3])} represent creative expression"
        }
        
        return domain_responses.get(domain, f"{', '.join(concepts[:3])} are interconnected concepts")
    
    def combine_concepts_intelligently(self, concepts: List[str], context: Dict) -> str:
        """Intelligently combine concepts based on context"""
        
        if not concepts:
            return "this is an interesting topic that requires more information"
        
        if len(concepts) == 1:
            return f"the concept of '{concepts[0]}' is multifaceted and worth exploring"
        elif len(concepts) == 2:
            return f"'{concepts[0]}' and '{concepts[1]}' are related in several ways"
        else:
            return f"'{concepts[0]}', '{concepts[1]}', and other factors like '{concepts[2]}' all contribute to the answer"
    
    def analyze_conversation_context(self, chat_history: List[Dict]) -> Dict:
        """Analyze conversation context for better responses"""
        
        context = {
            'message_count': len(chat_history),
            'recent_topics': [],
            'conversation_tone': 'neutral'
        }
        
        # Extract recent topics
        for message in chat_history[-5:]:  # Last 5 messages
            if message.get('role') == 'user':
                content = message.get('content', '').lower()
                words = content.split()
                context['recent_topics'].extend(words[:3])  # First 3 words of each message
        
        return context
    
    def perform_basic_analysis(self, concepts: List[str], chat_history: List[Dict]) -> str:
        """Perform basic analysis on concepts"""
        
        if not concepts:
            return "the available information suggests multiple possibilities"
        
        # Simple analysis based on concept relationships
        analysis_templates = [
            f"the relationship between {concepts[0]} and related factors suggests complexity",
            f"analyzing {concepts[0]} reveals multiple interconnected elements",
            f"the data points toward {concepts[0]} being a key factor",
            f"breaking down {concepts[0]} shows various contributing elements"
        ]
        
        return random.choice(analysis_templates)
    
    def generate_contextual_unknown_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate contextual responses for unknown inputs"""
        
        user_lower = user_input.lower().strip()
        input_length = len(user_input.split())
        has_question_mark = '?' in user_input
        
        # Handle very short inputs with specific responses
        if user_lower in ['hi', 'hello', 'hey']:
            return random.choice(self.response_templates['greeting'])
        
        if user_lower in ['thanks', 'thank you', 'thx']:
            return random.choice(self.response_templates['thanks'])
        
        if user_lower in ['bye', 'goodbye', 'see you']:
            return random.choice(self.response_templates['goodbye'])
        
        # More intelligent analysis of the input
        if any(word in user_lower for word in ['calculate', 'math', 'compute']):
            return "I can help with calculations! Try asking me something like 'what is 15 + 27?' or 'calculate the average of 10, 20, 30'."
        
        if any(word in user_lower for word in ['learn', 'teach', 'explain']):
            return "I'm always learning from our conversations. What would you like me to explain or learn about?"
        
        # Build on conversation history with better context
        if len(chat_history) > 2:
            # Look for patterns in recent conversation
            recent_topics = []
            for msg in chat_history[-3:]:
                if msg.get('role') == 'user':
                    content = msg.get('content', '').lower()
                    words = content.split()[:3]  # First 3 words
                    recent_topics.extend(words)
            
            if recent_topics:
                unique_topics = list(set(recent_topics))[:2]
                if len(unique_topics) > 0:
                    return f"I notice we've been discussing topics like '{unique_topics[0]}'. Would you like to explore this further or ask about something else?"
        
        # Respond based on input characteristics with more variety
        if has_question_mark:
            if input_length < 5:
                return "That's a great question! Could you provide a bit more detail so I can give you the best answer?"
            else:
                return "Interesting question! While I may not have all the details, I'd be happy to help you think through this. Could you share more context?"
        
        elif input_length < 3:
            responses = [
                "I'm here to help! What would you like to know or discuss?",
                "Feel free to ask me anything - calculations, questions, or just chat!",
                "I'd love to assist you. What's on your mind?",
                "What can I help you with today?"
            ]
            return random.choice(responses)
        
        elif input_length > 15:
            return "That's quite detailed! Let me focus on the key points. Could you highlight the main question or topic you'd like me to address?"
        
        else:
            # Use enhanced unknown responses
            enhanced_responses = [
                "I'm processing what you've shared. Could you help me understand the main point you'd like to discuss?",
                "That's interesting! I'd like to help but need a bit more context. What specifically would you like to know?",
                "I'm here to assist with calculations, questions, and analysis. What would you like to explore?",
                "Let me think about this... Could you rephrase or provide more details about what you're looking for?"
            ]
            return random.choice(enhanced_responses)
    
    def clean_input(self, text: str) -> str:
        """Enhanced input cleaning with better normalization"""
        
        # Convert to lowercase and strip
        text = text.lower().strip()
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive punctuation but keep meaningful ones
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        text = re.sub(r'[.]{2,}', '.', text)
        
        # Remove special characters but keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^\w\s\?\!\.\,\-\+\*\/\=\(\)]', '', text)
        
        return text.strip()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get enhanced A.v.A module statistics"""
        base_stats = super().get_stats()
        
        # Add A.v.A specific enhanced stats
        learning_data = self.chat_manager.get_learning_data(self.module_name)
        
        avg_confidence = 0.0
        active_patterns = 0
        
        if learning_data:
            confidences = [data['confidence'] for data in learning_data]
            avg_confidence = statistics.mean(confidences) if confidences else 0.0
            active_patterns = len([data for data in learning_data if data['usage_count'] > 0])
        
        base_stats.update({
            'response_templates': sum(len(templates) for templates in self.response_templates.values()),
            'pattern_categories': len(self.patterns),
            'knowledge_domains': len(self.knowledge_domains),
            'math_operations': len(self.math_operations),
            'avg_confidence': avg_confidence,
            'active_patterns': active_patterns,
            'reasoning_patterns': len(self.reasoning_patterns),
            'personality_traits': len(self.conversation_memory['personality_traits']),
            'discussed_topics': len(set(self.conversation_memory.get('discussed_topics', []))),
            'module_type': 'AI-like Local Intelligence',
            'capabilities': 'Advanced Reasoning, Context Awareness, Adaptive Learning, Multi-domain Analysis'
        })
        
        return base_stats
    
    def update_conversation_context(self, user_input: str, chat_history: List[Dict]):
        """Update conversation memory with AI-like context awareness"""
        # Extract topics from current input
        concepts = self.extract_enhanced_concepts(user_input)
        self.conversation_memory['discussed_topics'].extend(concepts[:3])
        
        # Keep only recent topics (last 20)
        if len(self.conversation_memory['discussed_topics']) > 20:
            self.conversation_memory['discussed_topics'] = self.conversation_memory['discussed_topics'][-20:]
        
        # Analyze user communication patterns
        if len(user_input.split()) > 10:
            self.conversation_memory['user_preferences']['detail_level'] = 'detailed'
        elif len(user_input.split()) < 3:
            self.conversation_memory['user_preferences']['detail_level'] = 'brief'
    
    def find_intelligent_learned_response(self, user_input: str) -> str:
        """Advanced learned response matching with semantic understanding"""
        learning_data = self.chat_manager.get_learning_data(self.module_name)
        
        if not learning_data:
            return ""
        
        user_concepts = set(self.extract_enhanced_concepts(user_input))
        best_match = None
        best_score = 0
        
        for data in learning_data:
            pattern_concepts = set(self.extract_enhanced_concepts(data['pattern']))
            
            # Semantic similarity scoring
            concept_overlap = len(user_concepts.intersection(pattern_concepts))
            confidence_bonus = data['confidence'] * 2
            usage_bonus = min(data['usage_count'] * 0.5, 3)
            
            score = concept_overlap + confidence_bonus + usage_bonus
            
            if score > best_score and score > 4:  # Higher threshold for quality
                best_score = score
                best_match = data
        
        return best_match['response'] if best_match else ""
    
    def add_reasoning_layer(self, base_response: str, user_input: str) -> str:
        """Add AI-like reasoning to learned responses"""
        reasoning_starters = [
            "I recall from our previous discussions that ",
            "Based on what I've learned, ",
            "My analysis suggests that ",
            "Drawing from my experience, "
        ]
        
        starter = random.choice(reasoning_starters)
        return f"{starter}{base_response.lower()}"
    
    def generate_calculation_reasoning(self, user_input: str, calc_result: str) -> str:
        """Generate reasoning for mathematical calculations"""
        reasoning_options = [
            "Let me work through this calculation step by step:",
            "I'll solve this mathematically for you:",
            "Breaking down this mathematical problem:",
            "Applying mathematical principles here:",
            "Using computational analysis:"
        ]
        return random.choice(reasoning_options)
    
    def detect_reasoning_pattern(self, text: str) -> str:
        """Detect the type of reasoning needed"""
        text_lower = text.lower()
        
        for pattern_type, keywords in self.reasoning_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return pattern_type
        
        # Default reasoning based on question type
        if '?' in text:
            return 'analysis'
        elif any(word in text_lower for word in ['why', 'how', 'what if']):
            return 'cause_effect'
        elif any(word in text_lower for word in ['compare', 'versus', 'difference']):
            return 'comparison'
        else:
            return 'synthesis'
    
    def identify_advanced_domain(self, text: str) -> str:
        """Advanced domain identification with confidence scoring"""
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, info in self.knowledge_domains.items():
            score = 0
            for keyword in info['keywords']:
                if keyword in text_lower:
                    # Weight longer, more specific keywords higher
                    score += len(keyword.split()) + 1
            domain_scores[domain] = score
        
        if domain_scores:
            best_domain = ""
            best_score = -1
            for domain, score in domain_scores.items():
                if score > best_score:
                    best_score = score
                    best_domain = domain
            
            if best_score > 1:  # Require minimum confidence
                return best_domain
        
        return ""
    
    def generate_ai_like_response(self, intent: str, reasoning_type: str, domain: str, 
                                clean_input: str, chat_history: List[Dict], original_input: str) -> str:
        """Generate sophisticated AI-like responses with multi-layer reasoning"""
        
        # Handle identity with AI personality
        if intent == 'greeting':
            return self.generate_personalized_greeting(chat_history)
        
        elif intent == 'question':
            return self.generate_reasoning_based_response(
                clean_input, reasoning_type, domain, chat_history, original_input
            )
        
        elif intent == 'analysis':
            return self.generate_analytical_response(
                clean_input, reasoning_type, domain, chat_history
            )
        
        elif intent == 'thanks':
            return self.generate_contextual_thanks_response(chat_history)
        
        elif intent == 'goodbye':
            return self.generate_thoughtful_goodbye(chat_history)
        
        elif intent == 'learning':
            return self.generate_learning_response(clean_input, chat_history)
        
        else:
            return self.generate_intelligent_unknown_response(
                clean_input, reasoning_type, domain, chat_history
            )
    
    def generate_personalized_greeting(self, chat_history: List[Dict]) -> str:
        """Generate personalized greetings based on conversation history"""
        if len(chat_history) == 0:
            return "Hello! I'm A.v.A, your advanced virtual assistant. I'm here to help with calculations, analysis, and thoughtful conversation. What would you like to explore today?"
        
        elif len(chat_history) < 5:
            return "Welcome back! I'm ready to continue our conversation. What's on your mind?"
        
        else:
            recent_topics = self.conversation_memory.get('discussed_topics', [])
            if recent_topics:
                topic = recent_topics[-1]
                return f"Hello again! I remember we were discussing topics related to '{topic}'. How can I help you today?"
            else:
                return "Good to see you again! I'm here and ready to assist with whatever you need."
    
    def generate_reasoning_based_response(self, clean_input: str, reasoning_type: str, 
                                        domain: str, chat_history: List[Dict], original_input: str) -> str:
        """Generate responses with explicit reasoning chains"""
        
        # Handle specific question types with AI-like analysis
        if 'who are you' in clean_input.lower() or 'what are you' in clean_input.lower():
            return "I'm A.v.A - an Advanced virtual Assistant. I'm designed to think, reason, and learn from our conversations. Unlike simple chatbots, I can perform calculations, analyze information, and adapt my responses based on context. I operate entirely locally without external APIs, using sophisticated reasoning algorithms."
        
        if 'how do you work' in clean_input.lower():
            return "I use multiple layers of analysis: pattern recognition for understanding context, semantic analysis for meaning extraction, reasoning pattern detection for logical flow, and adaptive learning from our conversations. My responses combine logical reasoning with intuitive understanding, much like human thought processes."
        
        # Domain-specific reasoning
        if domain and domain in self.knowledge_domains:
            domain_info = self.knowledge_domains[domain]
            concepts = self.extract_enhanced_concepts(clean_input)
            
            if concepts:
                reasoning_text = domain_info['reasoning']
                response_template = random.choice(domain_info['responses'])
                concept_text = ', '.join(concepts[:3])
                
                return f"{reasoning_text}. {response_template.format(concept_text)}. Let me analyze this further: {self.generate_deeper_analysis(concepts, reasoning_type)}"
        
        # General reasoning-based response
        concepts = self.extract_enhanced_concepts(clean_input)
        if concepts:
            return f"Analyzing your question about {concepts[0]}, I need to consider multiple factors. {self.generate_contextual_reasoning(concepts, reasoning_type, chat_history)}"
        
        return "That's an intriguing question that requires careful analysis. Could you provide more context so I can apply the appropriate reasoning approach?"
    
    def generate_deeper_analysis(self, concepts: List[str], reasoning_type: str) -> str:
        """Generate deeper analytical insights"""
        if reasoning_type == 'cause_effect':
            return f"The relationship between {concepts[0]} involves causal factors that interconnect in complex ways"
        elif reasoning_type == 'comparison':
            return f"Comparing {concepts[0]} with related concepts reveals important distinctions and similarities"
        elif reasoning_type == 'analysis':
            return f"Breaking down {concepts[0]} into its component parts helps us understand the underlying mechanisms"
        else:
            return f"Synthesizing information about {concepts[0]} requires integrating multiple perspectives"
    
    def generate_contextual_reasoning(self, concepts: List[str], reasoning_type: str, chat_history: List[Dict]) -> str:
        """Generate reasoning based on conversation context"""
        if len(chat_history) > 3:
            return f"Given our previous discussion, {concepts[0]} connects to broader themes we've explored. This suggests a pattern that requires {reasoning_type} thinking."
        else:
            return f"To properly address {concepts[0]}, I need to apply {reasoning_type} reasoning and consider various perspectives."
    
    def generate_analytical_response(self, clean_input: str, reasoning_type: str, domain: str, chat_history: List[Dict]) -> str:
        """Generate analytical responses with AI-like depth"""
        concepts = self.extract_enhanced_concepts(clean_input)
        
        if domain and domain in self.knowledge_domains:
            domain_info = self.knowledge_domains[domain]
            response_template = random.choice(domain_info['responses'])
            concept_text = ', '.join(concepts[:2])
            
            analysis = f"{response_template.format(concept_text)}. "
            analysis += self.generate_deeper_analysis(concepts, reasoning_type)
            return analysis
        
        if concepts:
            return f"Analyzing {concepts[0]}, I can identify several interconnected factors: {self.generate_deeper_analysis(concepts, reasoning_type)}"
        
        return "This requires systematic analysis. Could you provide more specific details for me to examine?"
    
    def generate_contextual_thanks_response(self, chat_history: List[Dict]) -> str:
        """Generate contextual thanks responses"""
        if len(chat_history) > 5:
            return "You're very welcome! I enjoy our thoughtful conversations and learning together. Feel free to ask anything else!"
        else:
            return random.choice(self.response_templates['thanks'])
    
    def generate_thoughtful_goodbye(self, chat_history: List[Dict]) -> str:
        """Generate thoughtful goodbye responses"""
        if len(chat_history) > 3:
            topics = self.conversation_memory.get('discussed_topics', [])
            if topics:
                return f"Goodbye! I've enjoyed our discussion about {topics[-1]} and related topics. Looking forward to our next conversation!"
        
        return random.choice(self.response_templates['goodbye'])
    
    def generate_learning_response(self, clean_input: str, chat_history: List[Dict]) -> str:
        """Generate responses about learning and knowledge"""
        learning_responses = [
            "I'm constantly learning from our interactions. Each conversation helps me understand better and provide more relevant responses.",
            "Learning is fascinating! I process patterns, adapt to context, and build understanding through our exchanges.",
            "My learning process involves analyzing conversation patterns, extracting key concepts, and building connections between ideas.",
            "I learn by recognizing patterns in our discussions and using that knowledge to improve future responses."
        ]
        return random.choice(learning_responses)
    
    def generate_intelligent_unknown_response(self, clean_input: str, reasoning_type: str, domain: str, chat_history: List[Dict]) -> str:
        """Generate intelligent responses for unknown inputs with reasoning"""
        
        # Try to identify what the user might be asking about
        concepts = self.extract_enhanced_concepts(clean_input)
        
        if concepts:
            reasoning_approach = "Let me think about this systematically"
            if reasoning_type == 'analysis':
                reasoning_approach = "I need to analyze this carefully"
            elif reasoning_type == 'cause_effect':
                reasoning_approach = "Let me consider the causal relationships here"
            elif reasoning_type == 'comparison':
                reasoning_approach = "I should compare different aspects of this"
            
            return f"{reasoning_approach}. While I'm processing the concepts of {', '.join(concepts[:2])}, I need more context to provide the most helpful response. Could you elaborate on what specifically interests you?"
        
        # Fallback with AI-like uncertainty expression
        uncertainty_responses = [
            "I'm analyzing your input, but I need more information to understand your specific question or request.",
            "My reasoning processes suggest multiple interpretations. Could you clarify what you'd like to explore?",
            "I'm processing what you've shared, but I'd like to ensure I understand correctly. What's the main point you'd like to discuss?",
            "I want to give you the most thoughtful response possible. Could you provide a bit more context?"
        ]
        
        return random.choice(uncertainty_responses)
    
    def calculate_advanced_confidence(self, intent: str, reasoning_type: str, domain: str, 
                                    clean_input: str, chat_history: List[Dict]) -> float:
        """Calculate confidence with advanced contextual factors"""
        base_confidence = 0.6
        
        # Intent-based confidence
        intent_confidence = {
            'greeting': 0.95, 'thanks': 0.95, 'goodbye': 0.95,
            'calculation': 0.98, 'question': 0.75, 'analysis': 0.8,
            'learning': 0.85, 'unknown': 0.4
        }
        
        confidence = intent_confidence.get(intent, base_confidence)
        
        # Domain knowledge bonus
        if domain:
            confidence += 0.1
        
        # Reasoning type bonus
        if reasoning_type in ['analysis', 'cause_effect']:
            confidence += 0.05
        
        # Conversation context bonus
        if len(chat_history) > 5:
            confidence += 0.05
        
        # Input complexity consideration
        words = len(clean_input.split())
        if 5 <= words <= 15:  # Optimal complexity
            confidence += 0.05
        
        return min(confidence, 1.0)