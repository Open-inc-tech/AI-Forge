from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add core to path for imports
sys.path.append(str(Path(__file__).parent.parent / "core"))
from chat_manager import ChatManager

class BaseAIModule(ABC):
    """Base class for all AI modules"""
    
    name = "Base Module"
    version = "1.0.0"
    description = "Base AI module class"
    
    def __init__(self):
        self.chat_manager = ChatManager()
        self.module_name = self.__class__.name
        
        # Initialize database for this module
        self.chat_manager.init_module_database(self.module_name)
    
    @abstractmethod
    def generate_response(self, user_input: str, chat_history: List[Dict]) -> str:
        """Generate a response to user input"""
        pass
    
    def learn_from_conversation(self, user_input: str, ai_response: str, confidence: float = 1.0):
        """Learn from a conversation"""
        # Extract patterns from user input for learning
        patterns = self.extract_patterns(user_input)
        
        for pattern in patterns:
            self.chat_manager.save_learning_data(
                self.module_name, 
                pattern, 
                ai_response, 
                confidence
            )
    
    def extract_patterns(self, text: str) -> List[str]:
        """Extract learning patterns from text"""
        patterns = []
        
        # Convert to lowercase for pattern matching
        text_lower = text.lower().strip()
        
        # Add the full text as a pattern
        patterns.append(text_lower)
        
        # Extract key words (simple approach)
        words = text_lower.split()
        if len(words) > 1:
            # Add combinations of words
            for i in range(len(words)):
                for j in range(i + 1, min(i + 4, len(words) + 1)):  # Max 3-word combinations
                    pattern = " ".join(words[i:j])
                    if len(pattern) > 2:  # Only meaningful patterns
                        patterns.append(pattern)
        
        return patterns
    
    def find_similar_response(self, user_input: str) -> str:
        """Find a similar response from learning data"""
        learning_data = self.chat_manager.get_learning_data(self.module_name)
        
        if not learning_data:
            return None
        
        user_input_lower = user_input.lower().strip()
        best_match = None
        best_score = 0
        
        for data in learning_data:
            pattern = data['pattern']
            confidence = data['confidence']
            usage_count = data['usage_count']
            
            # Simple similarity scoring
            score = 0
            
            # Exact match
            if pattern == user_input_lower:
                score = 10 * confidence
            # Contains pattern
            elif pattern in user_input_lower:
                score = 5 * confidence
            # Pattern contains input
            elif user_input_lower in pattern:
                score = 3 * confidence
            # Word overlap
            else:
                pattern_words = set(pattern.split())
                input_words = set(user_input_lower.split())
                overlap = len(pattern_words.intersection(input_words))
                if overlap > 0:
                    score = overlap * confidence
            
            # Boost score based on usage
            score *= (1 + usage_count * 0.1)
            
            if score > best_score:
                best_score = score
                best_match = data
        
        # Return response if score is high enough
        if best_match and best_score > 2:
            return best_match['response']
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get module statistics"""
        return self.chat_manager.get_module_stats(self.module_name)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        return self.chat_manager.get_conversations(self.module_name, limit)
