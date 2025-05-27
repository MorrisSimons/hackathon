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

    def clean_database():
        """Delete all nodes and relationships from the database"""
        with driver.session() as session:
            # Delete all nodes and relationships
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)
            print("All nodes and relationships deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (n) RETURN count(n) as node_count"
            result = session.run(count_query)
            node_count = result.single()["node_count"]
            print(f"Remaining nodes: {node_count}")
            return node_count

    def delete_emotions_classes():
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

    def delete_all_emotion_connections():
        with driver.session() as session:
            # Delete all HAS_EMOTION relationships
            query = "MATCH ()-[r:HAS_EMOTION]->() DELETE r"
            session.run(query)
            print("All emotion connections deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH ()-[r:HAS_EMOTION]->() RETURN count(r) as connection_count"
            result = session.run(count_query)
            connection_count = result.single()["connection_count"]
            print(f"Remaining emotion connections: {connection_count}")
            return connection_count

    def delete_all_people():
        with driver.session() as session:
            # Delete all person nodes
            query = "MATCH (p:Person) DETACH DELETE p"
            session.run(query)
            print("All person nodes deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (p:Person) RETURN count(p) as person_count"
            result = session.run(count_query)
            person_count = result.single()["person_count"]
            print(f"Remaining person nodes: {person_count}")
            return person_count

    def delete_all_usernames():
        with driver.session() as session:
            # Delete all username nodes
            query = "MATCH (u:Username) DETACH DELETE u"
            session.run(query)
            print("All username nodes deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (u:Username) RETURN count(u) as username_count"
            result = session.run(count_query)
            username_count = result.single()["username_count"]
            print(f"Remaining username nodes: {username_count}")
            return username_count
    
    def delete_all_messages():
        with driver.session() as session:
            # Delete all message nodes
            query = "MATCH (m:Message) DETACH DELETE m"
            session.run(query)
            print("All message nodes deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (m:Message) RETURN count(m) as message_count"
            result = session.run(count_query)
            message_count = result.single()["message_count"]
            print(f"Remaining message nodes: {message_count}")
            return message_count


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


    def add_message_node(conversation_id, message_id, username) -> dict:
        with driver.session() as session:
            query = """
            MATCH (u:Username {username: $username})
            CREATE (m:Message {
                text: '',
                conversation_id: $conversation_id,
                message_id: $message_id,
                username: $username,
                created_at: datetime(),
                label: $message_id
            })
            CREATE (m)-[:SENT_BY]->(u)
            RETURN m, u
            """
            result = session.run(query, 
                                conversation_id=conversation_id,
                                message_id=message_id,
                                username=username)
            return result.single()

    def add_username(name, username):
        with driver.session() as session:
            query = """
            CREATE (u:Username {
                name: $name,
                username: $username,
                created_at: datetime()
            })
            RETURN u
            """
            result = session.run(query, name=name, username=username)
            return result.single()


    def connect_person(name, username, role="person"):
        with driver.session() as session:
            query = """
            MATCH (u:Username {username: $username})
            CREATE (p:Person {
                name: $name,
                role: $role,
                created_at: datetime()
            })
            CREATE (p)-[:RELATED_TO]->(u)
            RETURN p, u
            """
            result = session.run(query, name=name, username=username, role=role)
            return result.single()
    
    def connect_emotion(emotion_name, message_id):
        """Add emotion to a message"""
        with driver.session() as session:
            query = """
            MATCH (e:Emotion {name: $emotion_name})
            MATCH (m:Message {message_id: $message_id})
            CREATE (m)-[:HAS_EMOTION]->(e)
            RETURN m, e
            """
            result = session.run(query, emotion_name=emotion_name, message_id=message_id)
            
            print(f"Emotion '{emotion_name}' added to message '{message_id}' successfully!")
            return result.single()

    def connect_problem(problem_name, message_id):
        """Add problem to a message"""
        with driver.session() as session:
            query = """
            MATCH (p:Problem {name: $problem_name})
            MATCH (m:Message {message_id: $message_id})
            CREATE (m)-[:HAS_PROBLEM]->(p)
            RETURN m, p
            """
            result = session.run(query, problem_name=problem_name, message_id=message_id)
            
            print(f"Problem '{problem_name}' added to message '{message_id}' successfully!")
            return result.single()
    
if __name__ == "__main__":
    print("hello")
    #all_nodes = therapy_graph.get_all_nodes(print_nodes=True)
    #therapy_graph.add_person(name="mom", username="user_1", role="mother")
    #therapy_graph.add_emotion(username="user_1", emotion_name="joy")
    #therapy_graph.delete_all_people()
    #therapy_graph.create_username("John Doe", "user_1")
    therapy_graph.add_username(name="John Doe", username="user_1")
    therapy_graph.add_message_node(conversation_id="conv_1", message_id="msg_1", username="user_1")

    #therapy_graph.delete_all_messages()
    #therapy_graph.delete_all_emotion_connections()
    #therapy_graph.add_message_node(conversation_id="conv_1", message_id="msg_1", username="user_1")
    #therapy_graph.connect_emotion(emotion_name="joy", message_id="msg_1")

    

