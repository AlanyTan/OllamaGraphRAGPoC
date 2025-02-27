import logging
from neo4j import GraphDatabase
from llama_index.graph_stores.neo4j import Neo4jGraphStore

from config import config
# Enable logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Connection details
uri = config.NEO4J_URI
username = config.NEO4J_USERNAME
password = config.NEO4J_PASSWORD
auth=(username, password)
# Create the driver
driver = GraphDatabase.driver(uri, auth=auth)

# Verify the connection
try:
    with GraphDatabase.driver(uri, auth=auth) as driver:
        driver.verify_connectivity()
        print("Connection successful")

    # with driver.session(database="neo4j") as session:
    #     result = session.run("RETURN 1")
    #     print("Connection successful:", result.single()[0])
except Exception as e:
    logging.error("Failed to connect to the database:", exc_info=e)
exit()
# Use the driver in your application
graph_store = Neo4jGraphStore(
    username=username,
    password=password,
    url=uri,
    database="neo4j",
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

# NOTE: can take a while!
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=2,
)