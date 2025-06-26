import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Utility class for database operations"""
    
    @staticmethod
    def execute_query(db_path: Path, query: str, params: tuple = None) -> List[tuple]:
        """Execute a query and return results"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.commit()
            return results
        finally:
            conn.close()
    
    @staticmethod
    def create_table(db_path: Path, table_name: str, columns: Dict[str, str]):
        """Create a table with specified columns"""
        db_path.parent.mkdir(exist_ok=True)
        
        columns_sql = ", ".join([f"{name} {type_}" for name, type_ in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        
        DatabaseManager.execute_query(db_path, query)
    
    @staticmethod
    def insert_data(db_path: Path, table_name: str, data: Dict[str, Any]):
        """Insert data into a table"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.keys()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        values = tuple(data.values())
        DatabaseManager.execute_query(db_path, query, values)
    
    @staticmethod
    def select_data(db_path: Path, table_name: str, where_clause: str = None, params: tuple = None) -> List[Dict[str, Any]]:
        """Select data from a table"""
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def update_data(db_path: Path, table_name: str, data: Dict[str, Any], where_clause: str, where_params: tuple):
        """Update data in a table"""
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        
        params = tuple(data.values()) + where_params
        DatabaseManager.execute_query(db_path, query, params)
    
    @staticmethod
    def delete_data(db_path: Path, table_name: str, where_clause: str, params: tuple):
        """Delete data from a table"""
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        DatabaseManager.execute_query(db_path, query, params)
