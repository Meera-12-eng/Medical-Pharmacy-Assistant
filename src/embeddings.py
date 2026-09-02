from sentence_transformers import SentenceTransformer


def load_embedding_model(
    model_name="BAAI/bge-base-en-v1.5"
):
    return SentenceTransformer(model_name)


def embed_texts(
    texts,
    embedding_model,
    batch_size=256
):
    embeddings = embedding_model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings


def embed_query(
    query,
    embedding_model
):
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    return query_embedding
