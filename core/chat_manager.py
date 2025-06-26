import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ChatManager:
    """Manages chat conversations and learning data"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def get_module_db_path(self, module_name: str) -> Path:
        """Get database path for a specific module"""
        return self.data_dir / f"{module_name}_chat.db"
    
    def init_module_database(self, module_name: str):
        """Initialize database for a module"""
        db_path = self.get_module_db_path(module_name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                context TEXT
            )
        ''')
        
        # Create learning data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                response TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create module stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS module_stats (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, module_name: str, user_input: str, ai_response: str, context: List[Dict] = None):
        """Save a conversation to the module's database"""
        self.init_module_database(module_name)
        
        db_path = self.get_module_db_path(module_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        context_json = json.dumps(context) if context else None
        
        cursor.execute('''
            INSERT INTO conversations (user_input, ai_response, context)
            VALUES (?, ?, ?)
        ''', (user_input, ai_response, context_json))
        
        # Update conversation count
        cursor.execute('''
            INSERT OR REPLACE INTO module_stats (key, value, updated_at)
            VALUES ('total_conversations', 
                    COALESCE((SELECT CAST(value AS INTEGER) FROM module_stats WHERE key = 'total_conversations'), 0) + 1,
                    CURRENT_TIMESTAMP)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_conversations(self, module_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent conversations for a module"""
        db_path = self.get_module_db_path(module_name)
        
        if not db_path.exists():
            return []
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_input, ai_response, timestamp, context
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        conversations = []
        for row in cursor.fetchall():
            context = json.loads(row[3]) if row[3] else None
            conversations.append({
                'user_input': row[0],
                'ai_response': row[1],
                'timestamp': row[2],
                'context': context
            })
        
        conn.close()
        return conversations
    
    def save_learning_data(self, module_name: str, pattern: str, response: str, confidence: float = 1.0):
        """Save learning data for a module"""
        self.init_module_database(module_name)
        
        db_path = self.get_module_db_path(module_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if pattern already exists
        cursor.execute('SELECT id, usage_count FROM learning_data WHERE pattern = ?', (pattern,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing pattern
            cursor.execute('''
                UPDATE learning_data 
                SET response = ?, confidence = ?, usage_count = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (response, confidence, existing[1] + 1, existing[0]))
        else:
            # Insert new pattern
            cursor.execute('''
                INSERT INTO learning_data (pattern, response, confidence)
                VALUES (?, ?, ?)
            ''', (pattern, response, confidence))
        
        # Update learned responses count
        cursor.execute('''
            INSERT OR REPLACE INTO module_stats (key, value, updated_at)
            VALUES ('learned_responses', 
                    (SELECT COUNT(*) FROM learning_data),
                    CURRENT_TIMESTAMP)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_learning_data(self, module_name: str) -> List[Dict[str, Any]]:
        """Get learning data for a module"""
        db_path = self.get_module_db_path(module_name)
        
        if not db_path.exists():
            return []
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pattern, response, confidence, usage_count, last_used
            FROM learning_data
            ORDER BY confidence DESC, usage_count DESC
        ''')
        
        learning_data = []
        for row in cursor.fetchall():
            learning_data.append({
                'pattern': row[0],
                'response': row[1],
                'confidence': row[2],
                'usage_count': row[3],
                'last_used': row[4]
            })
        
        conn.close()
        return learning_data
    
    def get_module_stats(self, module_name: str) -> Dict[str, Any]:
        """Get statistics for a module"""
        db_path = self.get_module_db_path(module_name)
        
        if not db_path.exists():
            return {'learned_responses': 0, 'total_conversations': 0}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM module_stats')
        stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'learned_responses': int(stats.get('learned_responses', 0)),
            'total_conversations': int(stats.get('total_conversations', 0))
        }
