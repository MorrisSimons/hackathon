from our_graph import TherapyGraph
import json
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Optional

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0.3)

def setup_database():
    """Initialize the database with emotions and relationships"""
    print("Setting up database...")
    TherapyGraph.clean_database()
    TherapyGraph.delete_emotions_classes()
    TherapyGraph.delete_all_relationships_types()
    
    TherapyGraph.insert_emotions_as_nodes()
    TherapyGraph.insert_relationships_types()
    
    # Add usernames
    TherapyGraph.add_username(name="John Doe", username="user_1")
    TherapyGraph.add_username(name="Our_Therapist", username="therapist_1")
    
    print("Database setup complete!")

def get_emotions_and_relationships():
    """Get available emotions and relationships from database"""
    emotions = TherapyGraph.get_all_emotions(True)
    emotion_names = [emotion['name'] for emotion in emotions]
    
    relationships_labels = TherapyGraph.get_all_relationships()
    relationships = [relationship["name"] for relationship in relationships_labels]
    
    return emotion_names, relationships

def connect_emotions(analysis, message_id, emotion_names):
    """Connect emotions to a message"""
    if 'emotions' in analysis and analysis['emotions']:
        for emotion_name in analysis['emotions']:
            if emotion_name in emotion_names:
                print(f"Connecting emotion '{emotion_name}' to message {message_id}")
                TherapyGraph.connect_emotion(message_id=f"msg_{message_id}", emotion_name=emotion_name)
            else:
                print(f"Emotion '{emotion_name}' not found in the list.")

def analyze_message_with_llm(msg, emotion_names, relationships):
    """Use LLM to analyze message for emotions and relationships"""
    class EmotionRelationshipAnalysis(BaseModel):
        emotions: Optional[List[str]] = None
        relationships: Optional[List[str]] = None

    try: 
        prompt = f"""Analyze this message to identify:
        1. Emotions expressed or implied in the message
        2. People or relationships the user is talking about
        
        Return a JSON object with:
        - 'emotions' field: list of emotions from this list {emotion_names} or null if none found
        - 'relationships' field: list of people/relationship from this list {relationships} or null if none found
        
        Message: '{msg}'
        
        Expected format: {{"emotions": ["stress"], "relationships": ["dad", "child"]}}
        Use null for fields where nothing is found."""
        
        response = llm.invoke(prompt)
        
        # Parse and validate the response using Pydantic
        analysis_data = json.loads(response.content)
        analysis = EmotionRelationshipAnalysis(**analysis_data)
        
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return EmotionRelationshipAnalysis(emotions=None, relationships=None)
    except Exception as e:
        print(f"Error analyzing message: {e}")
        return EmotionRelationshipAnalysis(emotions=None, relationships=None)

def analyze_problems(message_content, message_id):
    """Analyze message for problems using LLM"""
    class ProblemAnalysis(BaseModel):
        problems: Optional[List[Optional[dict]]] = None

    try:
        problem_prompt = f"""Analyze the following message to identify specific problems or issues that the user might be facing or that are being discussed.
        
        Return a JSON object with:
        - 'problems' field: list of objects with 'name' (the problem) and 'message_id' (where it was identified) or null if none found
        
        Message {message_id}: {message_content}
        
        Expected format: {{"problems": [{{"name": "trauma", "message_id": "{message_id}"}}, {{"name": "stress", "message_id": "{message_id}"}}]}}
        Use null if no problems are identified."""
        
        problem_response = llm.invoke(problem_prompt)
        problem_data = json.loads(problem_response.content)
        problem_analysis = ProblemAnalysis(**problem_data)
        
        print(f"Problem analysis for message {message_id}: {problem_analysis.model_dump()}")
        
        # Connect problems to graph database
        if problem_analysis.problems:
            for problem in problem_analysis.problems:
                # Skip None values that might be returned by the LLM
                if problem is None:
                    continue
                    
                # Validate that problem has the required fields
                if not isinstance(problem, dict) or 'name' not in problem:
                    print(f"Skipping invalid problem format: {problem}")
                    continue
                    
                problem_name = problem['name']
                username = "user_1"  # Default to user_1 for problems
                
                print(f"Connecting problem '{problem_name}' from message {message_id}")
                TherapyGraph.connect_problem(problem_name=problem_name, message_id=f"msg_{message_id}", username=username)
        else:
            print(f"No problems identified in message {message_id}.")
                
    except json.JSONDecodeError as e:
        print(f"JSON parsing error for problems: {e}")
    except Exception as e:
        print(f"Error analyzing problems: {e}")

def process_rasmus_message():
    """Process the rasmus_msg.json file"""
    # Load the rasmus message
    with open('rasmus_msg.json', 'r') as file:
        rasmus_data = json.load(file)
    
    # Get emotions and relationships from database
    emotion_names, relationships = get_emotions_and_relationships()
    
    # Process each item in the rasmus message
    for i, item in enumerate(rasmus_data["items"]):
        message_id = str(i + 1)  # Generate message IDs starting from 1
        msg_content = item["content"][0] if item["content"] else ""
        role = item["role"]
        
        print(f"Adding message {message_id} from {role}")
        print(f"Message content: {msg_content}")
        
        # Determine username based on role
        username = "therapist_1" if role == "assistant" else "user_1"
        
        # Add message node to graph
        TherapyGraph.add_message_node(
            text=msg_content, 
            conversation_id="conv_1", 
            message_id=f"msg_{message_id}", 
            username=username
        )
        
        # Analyze message for emotions and relationships
        analysis = analyze_message_with_llm(msg_content, emotion_names, relationships)
        print(f"Analysis for message {message_id}: {analysis.model_dump()}")
        
        # Connect emotions
        if analysis.emotions:
            connect_emotions(analysis.model_dump(), message_id, emotion_names)
        
        # Connect relationships
        if analysis.relationships:
            for relationship in analysis.relationships:
                print(f"Connecting relationship '{relationship}' to message {message_id}")
                TherapyGraph.connect_person(name=relationship, username=username, role="person")
        
        # Analyze for problems
        analyze_problems(msg_content, message_id)
    
    # Create conversation and connect messages
    conversation_id = "conv_1"
    create_conversation = TherapyGraph.create_conversation(conversation_id=conversation_id)
    
    print(f"Connecting all messages to conversation: {conversation_id}")
    
    # Connect all messages to the conversation
    for i in range(len(rasmus_data["items"])):
        message_id = f"msg_{str(i + 1)}"
        print(f"Connecting message {message_id} to conversation {conversation_id}")
        TherapyGraph.connect_message_to_conversation(message_id=message_id, conversation_id=conversation_id)
    
    print(f"Successfully processed {len(rasmus_data['items'])} messages from rasmus_msg.json")

def main():
    """Main function to run the processing"""
    print("Starting rasmus message processing...")
    
    # Setup database
    setup_database()
    
    # Process the rasmus message
    process_rasmus_message()
    
    print("Processing complete!")

if __name__ == "__main__":
    main()