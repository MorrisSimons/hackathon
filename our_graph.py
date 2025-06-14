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

class TherapyGraph:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def delete_all_relationships_types():
        with driver.session() as session:
            # Delete all relationship nodes
            query = "MATCH (r:Relationship) DETACH DELETE r"
            session.run(query)
            print("All relationship nodes deleted successfully!")

        # Verify deletion
        with driver.session() as session:
            count_query = "MATCH (r:Relationship) RETURN count(r) as relationship_count"
            result = session.run(count_query)
            relationship_count = result.single()["relationship_count"]
            print(f"Remaining relationship nodes: {relationship_count}")
            return relationship_count


    @staticmethod
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

    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def insert_relationships_types():
        relationships = ["dad", "mom", "brother", "sister", "friend", "colleague", "partner", "child"]
        
        with driver.session() as session:
            # Create relationship nodes
            for relationship in relationships:
                query = """
                CREATE (r:Relationship {
                    name: $relationship_name,
                    created_at: datetime()
                })
                """
                session.run(query, relationship_name=relationship)
            
            # Get count of created relationship nodes
            count_query = "MATCH (r:Relationship) RETURN count(r) as relationship_count"
            result = session.run(count_query)
            return result.single()["relationship_count"]

    @staticmethod
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

    @staticmethod
    def get_all_nodes(print_nodes=False):
        with driver.session() as session:
            query = "MATCH (n) RETURN n"
            result = session.run(query)
            all_nodes = [record["n"] for record in result]

        if print_nodes:
            for node in all_nodes:
                print(node.labels)

        return all_nodes
    
    @staticmethod
    def get_all_emotions(print_emotions=False):
        with driver.session() as session:
            query = "MATCH (e:Emotion) RETURN e"
            result = session.run(query)
            all_emotions = [record["e"] for record in result]

        if print_emotions:
            for emotion in all_emotions:
                print(emotion["name"])

        return all_emotions
    
    @staticmethod
    def get_all_relationships(print_relationships=False):
        with driver.session() as session:
            query = "MATCH (r:Relationship) RETURN r"
            result = session.run(query)
            all_relationships = [record["r"] for record in result]

        if print_relationships:
            for relationship in all_relationships:
                print(relationship["type"])

        return all_relationships
    


    @staticmethod
    def add_message_node(text ,conversation_id, message_id, username) -> dict:
        with driver.session() as session:
            query = """
            MATCH (u:Username {username: $username})
            CREATE (m:Message {
                text: $text,
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
                                text=text,
                                conversation_id=conversation_id,
                                message_id=message_id,
                                username=username)
            return result.single()

    @staticmethod
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


    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
    def connect_problem(problem_name, message_id, username):
        """Add problem to a message and user"""
        with driver.session() as session:
            # First create the problem node if it doesn't exist
            create_problem_query = """
            MERGE (p:Problem {name: $problem_name})
            ON CREATE SET p.created_at = datetime()
            RETURN p
            """
            session.run(create_problem_query, problem_name=problem_name)
            
            # Then connect it to message and username
            query = """
            MATCH (p:Problem {name: $problem_name})
            MATCH (m:Message {message_id: $message_id})
            MATCH (u:Username {username: $username})
            CREATE (m)-[:HAS_PROBLEM]->(p)
            CREATE (u)-[:HAS_PROBLEM]->(p)
            RETURN m, p, u
            """
            result = session.run(query, problem_name=problem_name, message_id=message_id, username=username)
            
            print(f"Problem '{problem_name}' added to message '{message_id}' and user '{username}' successfully!")
            return result.single()

    @staticmethod
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

    @staticmethod
    def create_conversation(conversation_id):
        """Create a simple conversation node"""
        with driver.session() as session:
            query = """
            CREATE (c:Conversation {
                conversation_id: $conversation_id,
                created_at: datetime()
            })
            RETURN c
            """
            result = session.run(query, conversation_id=conversation_id)
            print(f"Conversation '{conversation_id}' created successfully!")
            return result.single()

    @staticmethod
    def connect_message_to_conversation(message_id, conversation_id):
        """Connect a specific message to a conversation summary"""
        with driver.session() as session:
            query = """
            MATCH (m:Message {message_id: $message_id})
            MATCH (cs:ConversationSummary {conversation_id: $conversation_id})
            CREATE (m)-[:BELONGS_TO]->(cs)
            RETURN m, cs
            """
            result = session.run(query, message_id=message_id, conversation_id=conversation_id)
            return result.single()

def connect_all_messages_to_conversation(agent_message, conversation_id="conv_1"):
    """Connect all messages from agent_message to a conversation summary"""
    print(f"Connecting all messages to conversation: {conversation_id}")
    
    # Get all messages and connect them to the conversation
    for msg in agent_message["conversation"]:
        message_id = f"msg_{msg['message_id']}"
        print(f"Connecting message {message_id} to conversation {conversation_id}")
        TherapyGraph.connect_message_to_conversation(message_id=message_id, conversation_id=conversation_id)
    
    print(f"Successfully connected all {len(agent_message['conversation'])} messages to conversation {conversation_id}")

if __name__ == "__main__":
    print("hello")
    #all_nodes = TherapyGraph.get_all_nodes(print_nodes=True)
    #TherapyGraph.add_person(name="mom", username="user_1", role="mother")
    #TherapyGraph.add_emotion(username="user_1", emotion_name="joy")
    #TherapyGraph.delete_all_people()
    #TherapyGraph.create_username("John Doe", "user_1")
    #TherapyGraph.add_message_node(conversation_id="conv_1", message_id="msg_1", username="user_1")

    #TherapyGraph.delete_all_messages()
    #TherapyGraph.delete_all_emotion_connections()
    #TherapyGraph.add_message_node(conversation_id="conv_1", message_id="msg_1", username="user_1")
    #TherapyGraph.connect_emotion(emotion_name="joy", message_id="msg_1")

    #TherapyGraph.connect_problem(problem_name="stress", message_id="msg_1", username="user_1")


