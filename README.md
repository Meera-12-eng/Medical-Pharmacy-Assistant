<p align="center">
  <img src="https://github.com/user-attachments/assets/01b7883a-3435-48f5-b4ad-b7b4fcbe45f5" width="100%" alt="Medical Pharmacy Assistant Banner" />
</p>

# Medical Pharmacy Assistant

> An AI-powered, source-grounded pharmacy assistant for retrieving reliable drug information from medical drug labels.

## 📌 Overview

**Medical Pharmacy Assistant** is a Retrieval-Augmented Generation (RAG) project designed to help users retrieve reliable information about medications from a medical knowledge base.

The system is being built using official drug-labeling data and semantic/keyword-based retrieval techniques. The final system will provide grounded answers to questions about medications while referencing the retrieved medical sources.

The assistant focuses on:

* Drug indications and uses
* Active ingredients
* Adverse reactions
* Warnings
* Contraindications
* Drug interactions
* Dosage and administration

---

## 🎯 Project Goals

The project aims to:

* Provide fast access to medication information.
* Build a searchable medical knowledge base.
* Retrieve relevant medical information using semantic and keyword search.
* Generate source-grounded answers using RAG.
* Provide source information with generated responses.
* Reduce hallucinations by grounding answers in retrieved evidence.
* Avoid unsupported medical recommendations and diagnoses.

---

# 🔄 Current Pipeline

The project has currently completed the data processing, chunking, embedding, vector database, and retrieval stages.

```text
OpenFDA Drug Labels
        ↓
Data Processing & Cleaning
        ↓
Medical Section Extraction
        ↓
Document Chunking
        ↓
BGE Embeddings
        ↓
Weaviate Cloud
        ↓
Vector / BM25 / Hybrid Retrieval
        ↓
[Next: RAG + LLM Generation]
```

---

# 📚 Data Processing

The knowledge base is built from **OpenFDA Drug Labeling** data.

Three drug-labeling JSON files were processed:

```text
drug-label-0001-of-0014.json
drug-label-0002-of-0014.json
drug-label-0003-of-0014.json
```

### Dataset Statistics

| Stage                           | Records |
| ------------------------------- | ------: |
| Raw records                     |  60,000 |
| Records with medical content    |  58,325 |
| Records without medical content |   1,675 |
| Medical section-level documents | 657,965 |
| Selected drug labels            |   5,000 |
| Final chunks                    |  66,582 |

The processing pipeline includes:

* JSON parsing
* Medical content extraction
* Section extraction
* Text cleaning
* Metadata preservation
* Empty-record filtering

---

# 🧩 Medical Sections

The knowledge base currently focuses on the following drug-label sections:

```text
indications_and_usage
active_ingredient
adverse_reactions
warnings
contraindications
drug_interactions
dosage_and_administration
```

Each processed document preserves metadata including:

```text
brand_name
generic_name
manufacturer_name
substance_name
route
product_type
source_id
set_id
effective_time
version
section
```

---

# ✂️ Document Chunking

The selected medical documents were split into smaller chunks using:

**Recursive Character Text Splitter**

Configuration:

```text
Chunk Size: 800
Chunk Overlap: 160
```

The final processed knowledge base contains:

```text
66,582 chunks
```

Chunking was performed to improve semantic retrieval and ensure that retrieved context remains focused and manageable.

---

# 🧠 Embeddings

Each chunk was converted into a vector representation using:

**BAAI/bge-base-en-v1.5**

Configuration:

```text
Model: BAAI/bge-base-en-v1.5
Embedding Dimension: 768
Normalization: Enabled
Batch Size: 256
```

The final embedding matrix has the shape:

```text
(66,582, 768)
```

A verification step was performed to ensure that every chunk has a corresponding embedding:

```text
Chunks:     66,582
Embeddings: 66,582
```

✅ The counts match successfully.

---

# 🗄️ Vector Database

The pre-computed embeddings and medical chunks were indexed in:

**Weaviate Cloud**

Collection:

```text
MedicalChunk
```

The collection uses:

```text
self_provided()
```

This means that the embeddings generated during the embedding stage are directly provided to Weaviate rather than generating new embeddings inside the vector database.

### Stored Information

Each indexed object contains:

* Chunk text
* Brand name
* Generic name
* Manufacturer name
* Substance name
* Route
* Product type
* Source ID
* Set ID
* Effective time
* Version
* Section
* Chunk index
* Total chunks

### Indexing Verification

```text
Objects in Weaviate: 66,582
Expected objects:    66,582
```

✅ All chunks were successfully indexed.

---

# 🔎 Retrieval

The project currently supports three retrieval strategies.

## 1. Vector Similarity Search

Semantic retrieval is performed using the pre-computed BGE embeddings.

```text
User Query
    ↓
Query Embedding
    ↓
Vector Similarity Search
    ↓
Relevant Medical Chunks
```

---

## 2. BM25 Keyword Search

BM25 provides keyword-based retrieval.

It is useful when exact medical terms, drug names, or specific keywords are important.

```text
User Query
    ↓
Keyword Matching
    ↓
BM25
    ↓
Relevant Chunks
```

---

## 3. Hybrid Search

Hybrid Search combines:

* Vector semantic search
* BM25 keyword search

The current implementation uses:

```text
alpha = 0.5
```

This provides a balance between semantic similarity and exact keyword matching.

```text
                User Query
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
    Vector Search          BM25 Search
          ↓                   ↓
          └─────────┬─────────┘
                    ↓
             Hybrid Ranking
                    ↓
             Top-K Chunks
```

---

# ⚙️ Retrieval Function

A reusable retrieval function was implemented:

```python
results = retrieve_chunks(
    question,
    top_k=5,
    alpha=0.5
)
```

The function returns relevant medical chunks together with metadata such as:

```text
text
section
source_id
brand_name
generic_name
chunk_index
```

This function will be used directly by the next stage of the project.

---

# 📊 Retrieval Evaluation

The retrieval system was evaluated using three metrics:

| Metric      |  Score |
| ----------- | -----: |
| Precision@5 | 0.6444 |
| Recall@5    | 0.7778 |
| MRR         | 0.6889 |

The evaluation covered questions related to:

* Warnings
* Adverse reactions
* Drug interactions

### Evaluation Note

The reported Recall@5 is measured at the **section level**.

The ground truth is based on the expected medical section rather than every relevant chunk available in the corpus.

---

# 🛠️ Tech Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy
* JSON
* Regular Expressions

### NLP & Embeddings

* Sentence Transformers
* BAAI/bge-base-en-v1.5

### Vector Database

* Weaviate Cloud

### Retrieval

* Vector Similarity Search
* BM25
* Hybrid Search

### Planned RAG Layer

* LangChain
* Large Language Model

### Planned Interface

* Streamlit

---

# 📁 Project Structure

```text
Medical-Pharmacy-Assistant/
│
├── data/
│   ├── raw/
│   │   ├── drug-label-0001-of-0014.json
│   │   ├── drug-label-0002-of-0014.json
│   │   └── drug-label-0003-of-0014.json
│   │
│   └── processed/
│       └── medical_documents.jsonl
│
├── outputs/
│   ├── chunks/
│   │   └── medical_chunks_selected.jsonl
│   │
│   └── embeddings/
│       └── embeddings_final.zip
│
├── notebooks/
│   ├── data_processing.ipynb
│   ├── chunking.ipynb
│   ├── embeddings.ipynb
│   └── retrieval.ipynb
│
├── src/
│   ├── data_processing.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── chroma_db.py
│   ├── retriever.py
│   └── rag.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The exact project structure may evolve as the remaining RAG and application stages are implemented.

---

# 🔐 Security

API credentials are not stored directly in the notebooks or source code.

The Weaviate connection uses environment/secret variables:

```text
WEAVIATE_URL
WEAVIATE_API_KEY
```

Sensitive credentials should never be committed to the repository.

---

# 🚧 Current Status

### Completed

* [x] OpenFDA data collection
* [x] Data processing and cleaning
* [x] Medical section extraction
* [x] Document chunking
* [x] Embedding generation
* [x] Embedding verification
* [x] Weaviate Cloud setup
* [x] Chunk indexing
* [x] Vector similarity search
* [x] BM25 keyword search
* [x] Hybrid search
* [x] Retrieval function
* [x] Retrieval evaluation

### In Progress

* [ ] RAG pipeline
* [ ] Prompt engineering
* [ ] LLM integration
* [ ] Source-grounded answer generation
* [ ] Conversational follow-up handling
* [ ] Final evaluation

### Planned

* [ ] Streamlit interface
* [ ] End-to-end testing
* [ ] Deployment

---

# 🔮 Next Stage: RAG Generation

The next stage will connect the retrieval system to a Large Language Model.

The planned pipeline is:

```text
User Question
      ↓
retrieve_chunks()
      ↓
Top-K Relevant Medical Chunks
      ↓
Context Construction
      ↓
Prompt
      ↓
LLM
      ↓
Grounded Answer
      ↓
Source References
```

The LLM will be instructed to rely on retrieved medical context and avoid generating unsupported information.

---

# 🛡️ Medical Safety & Limitations

This project is intended as an **educational and information-retrieval system**.

It is not designed to:

* Diagnose medical conditions.
* Prescribe medications.
* Provide personalized treatment plans.
* Replace a healthcare professional.
* Generate unsupported medical recommendations.

If the required information is not available in the retrieved knowledge base, the final system should indicate that sufficient information is unavailable rather than hallucinating an answer.

> **Important:** Medication-related decisions should always be made in consultation with a qualified healthcare professional.

---

# 📄 Data Source

The project uses drug-labeling information from **OpenFDA** to build its medical knowledge base.

The data is processed and indexed for information retrieval and RAG-based question answering.

---

## 👥 Team

This project is developed collaboratively, with responsibilities distributed across:

* Data Collection & Processing
* Chunking & Embeddings
* Vector Database & Retrieval
* RAG & LLM Integration
* Evaluation
* User Interface
