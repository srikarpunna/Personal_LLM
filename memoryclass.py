import mysql.connector
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ConversationMemory:
    def __init__(self, db_name='lucky'):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Srikar@123456",
            database=db_name
        )
        self.cursor = self.conn.cursor()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create conversation_history table if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL,
            is_user BOOLEAN NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def save_message(self, user_message, ai_response):
        embedding = self.embedding_model.encode([user_message])[0]
        embedding_blob = embedding.tobytes()

        # Insert into the general user_data table
        sql = """
        INSERT INTO user_data (user_message, ai_response, embedding)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (user_message, ai_response, embedding_blob))
        self.conn.commit()

        # Extract key-value pairs dynamically
        self.extract_key_value(user_message, embedding_blob)

        # Add to conversation history
        sql = """
        INSERT INTO conversation_history (message, is_user)
        VALUES (%s, %s), (%s, %s)
        """
        self.cursor.execute(sql, (user_message, True, ai_response, False))
        self.conn.commit()
        
    def extract_key_value(self, user_message, embedding_blob):
        if "my name is" in user_message.lower():
            key = "name"
            value = user_message.lower().split("my name is")[-1].strip()
        elif "i like" in user_message.lower() or "i love" in user_message.lower():
            key = "likes"
            value = user_message.lower().split("i like")[-1].strip() if "i like" in user_message.lower() else user_message.lower().split("i love")[-1].strip()
        else:
            return

        sql = """
        INSERT INTO key_value_store (`key`, value, embedding)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (key, value, embedding_blob))
        self.conn.commit()

    def retrieve_relevant_information(self, query, top_n=5, threshold=0.1):
        query_embedding = self.embedding_model.encode([query])[0]
        self.cursor.execute("SELECT `key`, value, embedding FROM key_value_store")
        rows = self.cursor.fetchall()
        if not rows:
            return []  # No interactions found, return an empty list

        embeddings = [np.frombuffer(row[2], dtype=np.float32) for row in rows]
        keys = [row[0] for row in rows]
        values = [row[1] for row in rows]

        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]

        relevant_info = [(keys[i], values[i], similarities[i]) for i in top_indices if similarities[i] > threshold]
        return relevant_info

    def get_conversation_history(self, limit=5):
        sql = "SELECT message, is_user FROM conversation_history ORDER BY id DESC LIMIT %s"
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()[::-1]  # Reverse to get oldest first

    def close(self):
        self.cursor.close()
        self.conn.close()