import requests
import json
from memoryclass import ConversationMemory

# Initialize memory
conversation_memory = ConversationMemory()

def chat_with_llm(prompt):
    url = "http://localhost:11434/api/generate"

    # Retrieve relevant stored information
    relevant_info = conversation_memory.retrieve_relevant_information(prompt)
    context = ""
    if relevant_info:
        context = "Based on our previous conversation: "
        for key, value, similarity in relevant_info:
            context += f"{key}: {value}. "
    
    # Get conversation history
    history = conversation_memory.get_conversation_history()
    if history:
        context += "\nPrevious conversation:\n"
        for message, is_user in history:
            context += f"{'Human' if is_user else 'AI'}: {message}\n"
    
    context += "\nNow, based on this context:\n"

    full_prompt = f"""
    {context}
    Human: {prompt}
    AI: Please respond to the human's query, taking into account any relevant information from our previous conversation mentioned above. If there's no relevant previous information, just respond naturally to the query.
    """

    data = {
        "model": "llama3.1",
        "prompt": full_prompt
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        # Split and parse the response
        responses = response.text.strip().splitlines()
        combined_response = ""
        for resp in responses:
            try:
                json_data = json.loads(resp)
                combined_response += json_data.get('response', '')
            except json.JSONDecodeError as e:
                return f"JSON Decode Error: {e} | Response: {resp}"
        
        # Save conversation in memory
        conversation_memory.save_message(prompt, combined_response)
        
        return combined_response

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage with memory retrieval
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    if user_input.lower() == 'history':
        print("Conversation History:\n", conversation_memory.get_conversation_history())
        continue
    response = chat_with_llm(user_input)
    print("AI: ", response)

# Don't forget to close the database connection when you're done
conversation_memory.close()