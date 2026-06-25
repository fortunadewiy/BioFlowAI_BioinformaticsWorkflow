from rag_pipeline import build_rag_pipeline

chain, chunks = build_rag_pipeline()

question = "What is CRISPR?"

response = chain.invoke(
    {"query": question}
)

print(response["result"])