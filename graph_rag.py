import os
import openai

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# A very simple knowledge graph represented as a dictionary
knowledge_graph = {
    "Queen Elizabeth II": {
        "diagnosed with": "COVID-19"
    },
    "COVID-19": {
        "treated with": "Paxlovid",
        "symptoms": ["Fever", "Cough", "Fatigue"]
    },
    "Paxlovid": {
        "side effects": ["Dysgeusia (altered taste)", "Diarrhea"],
        "manufacturer": "Pfizer"
    }
}

def retrieve_context(query):
    """
    Retrieves context from the knowledge graph based on a simple query.

    Args:
        query: The user's question.

    Returns:
        Relevant context from the knowledge graph as a string.
    """
    context = ""
    query_lower = query.lower()

    for entity, relations in knowledge_graph.items():
        if entity.lower() in query_lower:
            context += f"{entity}: {relations}. "
            for relation_type, related_entity in relations.items():
                if isinstance(related_entity, list):
                    context += f"{entity} {relation_type}: {', '.join(related_entity)}. "
                else:
                    context += f"{entity} {relation_type}: {related_entity}. "
                    if related_entity in knowledge_graph:
                        for sub_relation, sub_entity in knowledge_graph[related_entity].items():
                           if isinstance(sub_entity, list):
                                context += f"{related_entity} {sub_relation}: {', '.join(sub_entity)}. "
                           else:
                                context += f"{related_entity} {sub_relation}: {sub_entity}. "
    return context


def generate_response(query, context):
    """
    Generates a response using the OpenAI API, given the query and context.

    Args:
        query: The user's question.
        context: Relevant context from the knowledge graph.

    Returns:
        The generated response from the OpenAI API.
    """
    
    prompt = f"""
    Answer the question based on the provided context. 
    If the answer is not in the context, say 'I don't know'.

    Context: {context}

    Question: {query}

    Answer:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content'].strip()

# Example Usage
user_query = "What are the side effects of the medication that was developed to treat the disease affecting Queen Elizabeth II?"
retrieved_context = retrieve_context(user_query)
response = generate_response(user_query, retrieved_context)

print(f"Query: {user_query}")
print(f"Retrieved Context: {retrieved_context}")
print(f"Response: {response}")
