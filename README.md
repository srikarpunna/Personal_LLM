# Personal AI Assistant with Persistent Memory

# Personal AI Assistant with Persistent Memory

This project is a Personal AI Assistant designed to act as a conversational friend, capable of storing and recalling personal information such as your name, tasks, appointments, behavior, likes, dislikes, health conditions, and more. It uses a combination of semantic vector search and structured key-value storage to provide contextually relevant responses across sessions, ensuring that the assistant can remember and adapt to user interactions over time.

The assistant leverages a MySQL database for persistent memory, storing user interactions, embeddings, and key-value pairs dynamically extracted from conversations. The AI model used is llama3.1, and the project is implemented using Python, with integration of the sentence-transformers library for generating embeddings.

## Features

- Dynamic Memory Storage: The assistant can store various types of user data dynamically without predefined structures.
- Persistent Memory: Information stored by the assistant is persistent across sessions, allowing the AI to recall previous interactions.
- Contextual Responses: Uses semantic vector search to provide contextually relevant responses based on past interactions.
- Flexible Information Retrieval: Capable of retrieving and using specific information like names, tasks, and preferences without requiring explicit functions for each data type.

## Technology Stack

- Programming Language: Python 3.8+
- AI Model: llama3.1
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Database: MySQL with LONGBLOB support for storing embeddings
- Libraries:
  - mysql-connector-python
  - sentence-transformers
  - sklearn
  - requests

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8+
- MySQL 5.7+ (with an existing database, e.g., lucky)
- Git (for version control)

## Setup

1. Clone the Repository

```bash
git clone https://github.com/srikarpunna/Personal_LLM.git
cd Personal_LLM
```

2. Set Up a Virtual Environment

```bash
python -m venv langchain_env
source langchain_env/bin/activate # On Windows, use `langchain_env\Scripts\activate`
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set Up the MySQL Database

Ensure your MySQL server is running, and create a new database:

```sql
CREATE DATABASE LLM;
USE LLM;

CREATE TABLE IF NOT EXISTS user_data (
id INT AUTO_INCREMENT PRIMARY KEY,
user_message TEXT NOT NULL,
ai_response TEXT NOT NULL,
embedding LONGBLOB NOT NULL,
interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS key_value_store (
id INT AUTO_INCREMENT PRIMARY KEY,
`key` VARCHAR(255) NOT NULL,
value TEXT NOT NULL,
embedding LONGBLOB NOT NULL,
interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

5. Configure Database Connection

Update the database connection details in `memoryclass.py`:

```python
self.conn = mysql.connector.connect(
host="127.0.0.1",
user="your_mysql_username",
password="your_mysql_password",
database="LLM"
)
```

## Usage

Running the Assistant

To start interacting with the AI assistant:

```bash
python custom_llama_llm.py
```

Example Interactions

Introduction

You: "Hi, my name is Srikar."
AI: "Nice to meet you, Srikar! How can I help you today?"

Remembering Information

You: "What is my name?"
AI: "You mentioned earlier that your name is Srikar."

## Project Structure

```
personal-ai-assistant/
│
├── memoryclass.py # Handles storage and retrieval of information
├── custom_llama_llm.py # Main script for interacting with the AI
├── README.md # Project documentation
├── requirements.txt # Project dependencies
```

## Contribution Guidelines

We welcome contributions to enhance the project! Please follow these guidelines:

1. Fork the Repository: Create your own fork of the repository.
2. Create a New Branch: Work on your feature or bugfix in a new branch.

```bash
git checkout -b feature/your-feature-name
```

3. Commit Changes: Write clear and concise commit messages.

```bash
git commit -m "Add feature X"
```

4. Push Changes: Push your changes to your fork.

```bash
git push origin feature/your-feature-name
```

5. Submit a Pull Request: Once your changes are ready, submit a pull request to the main branch.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact Information

For any questions, suggestions, or contributions, please contact:

- Name: Srikar Punna
- Email: [srikarv526@gmail.com](mailto:srikarv526@gmail.com)
- GitHub: [srikarpunna](https://github.com/srikarpunna)
