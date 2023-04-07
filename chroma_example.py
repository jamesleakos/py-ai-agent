
# set up chroma
import chromadb
client = chromadb.Client()

# collection = client.create_collection(name="vectors")
# collection.add(
#     documents=["This is a document", "This is another document"],
#     metadatas=[{"source": "my_source"}, {"source": "my_source"}],
#     ids=["id1", "id2"]
# )
# results = collection.query(
#     query_texts=["This is a query document"],
#     n_results=2
# )
# print(results)

