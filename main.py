from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

"""Neo4j functions"""

# Load environment variables
load_dotenv()

# Neo4j connection configuration from environment variables
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

# Create driver and connect to database
driver = GraphDatabase.driver(uri, auth=(username, password))


# Test connection
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' as message")
        return result.single()["message"]

try:
    message = test_connection()
    print(message)
except Exception as e:
    print(f"Connection failed: {e}")
    assert False, "Error connecting to Neo4j database"

print("Connected to Neo4j database successfully!")

class therapy_graph:

    def insert_emotions_as_nodes():
         # List of human emotions
        human_emotions = [
            'joy', 'happiness', 'sadness', 'anger', 'fear', 'disgust', 'surprise',
            'love', 'hate', 'excitement', 'anxiety', 'depression', 'guilt', 'shame',
            'pride', 'envy', 'jealousy', 'gratitude', 'hope', 'despair', 'grief',
            'relief', 'contentment', 'boredom', 'curiosity', 'confusion', 'frustration',
            'irritation', 'rage', 'fury', 'terror', 'panic', 'worry', 'stress',
            'calm', 'peace', 'serenity', 'bliss', 'euphoria', 'melancholy', 'loneliness',
            'nostalgia', 'regret', 'remorse', 'compassion', 'empathy', 'sympathy',
            'admiration', 'respect', 'contempt', 'disdain', 'awe', 'wonder', 'amazement',
            'enthusiasm', 'passion', 'desire', 'lust', 'affection', 'tenderness',
            'warmth', 'hostility', 'resentment', 'bitterness', 'forgiveness',
            'acceptance', 'rejection', 'approval', 'disapproval', 'trust', 'distrust',
            'confidence', 'doubt', 'certainty', 'uncertainty', 'optimism', 'pessimism'
        ]
        print(f"Total emotions: {len(human_emotions)}")
        print("Human emotions list created successfully!")
        with driver.session() as session:
            # Create emotion nodes
            for emotion in human_emotions:
                query = """
                CREATE (e:Emotion {
                    name: $emotion_name,
                    created_at: datetime()
                })
                """
                session.run(query, emotion_name=emotion)
            
            # Get count of created emotion nodes
            count_query = "MATCH (e:Emotion) RETURN count(e) as emotion_count"
            result = session.run(count_query)
            return result.single()["emotion_count"]

        # Insert all emotions as nodes
        try:
            emotion_count = insert_emotions_as_nodes()
            print(f"Successfully created {emotion_count} emotion nodes!")
        except Exception as e:
            print(f"Failed to insert emotions: {e}")
            assert False, "Error inserting emotions into Neo4j database" # TODO: REMOVE ME

    def delete_emotions():
        with driver.session() as session:
            # Delete all emotion nodes
            query = "MATCH (e:Emotion) DETACH DELETE e"
            session.run(query)
            print("All emotion nodes deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (e:Emotion) RETURN count(e) as emotion_count"
            result = session.run(count_query)
            emotion_count = result.single()["emotion_count"]
            print(f"Remaining emotion nodes: {emotion_count}")
            return emotion_count


if __name__ == "__main__":
    print("hello")
    therapy_graph.insert_emotions_as_nodes()
