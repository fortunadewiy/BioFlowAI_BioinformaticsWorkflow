from rag_pipeline import build_rag_pipeline

print("Building pipeline...")

chain, chunks = build_rag_pipeline()

print(f"Pipeline berhasil dibuat.")
print(f"Total chunks: {chunks}")