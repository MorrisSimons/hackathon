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

    def get_all_nodes(print_nodes=False):
        with driver.session() as session:
            query = "MATCH (n) RETURN n"
            result = session.run(query)
            all_nodes = [record["n"] for record in result]

        if print_nodes:
            for node in all_nodes:
                print(node.labels)

        return all_nodes
    
    def create_vector_index(consume=False):
        """this is only a 1 time use function"""
        with driver.session() as session:
            query = """
            CREATE VECTOR INDEX message_text_vector IF NOT EXISTS
            FOR (m:Message) ON (m.text_vector)
            OPTIONS {
              indexConfig: {
                `vector.dimensions`: 384,
                `vector.similarity_function`: 'cosine'
              }
            }
            """
            result = session.run(query)
            if consume:
                consume_item = result.consume()
                print(f"Query executed in: {consume_item.result_available_after} ms")
                print(f"Records available: {consume_item.result_consumed_after} ms")
  



if __name__ == "__main__":
    print("hello")
    #all_nodes = therapy_graph.get_all_nodes(print_nodes=True)
    therapy_graph.create_vector_index()
   
    

    

