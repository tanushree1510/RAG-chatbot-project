from src.retriever import retrieve  # use src. prefix

def main():
    query = "Who is the founder?"
    hits = retrieve(query, k=13)
    for i, h in enumerate(hits):
        print(f"Result {i+1}:")
        print(h["document"])
        print("Source:", h["metadata"]["source"])
        print("----")

if __name__ == "__main__":
    main()
