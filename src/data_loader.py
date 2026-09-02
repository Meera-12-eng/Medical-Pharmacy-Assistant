import pickle
import gzip
import json
import os


def load_json_file(file_path):
    """Load one OpenFDA JSON file."""

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["results"]


def load_all_json_files(json_files):
    """Load records from multiple JSON files."""

    all_records = []

    for file_path in json_files:
        records = load_json_file(file_path)
        all_records.extend(records)

    return all_records


def save_documents(documents, output_path):
    """Save processed documents using gzip + pickle."""

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with gzip.open(output_path, "wb") as f:
        pickle.dump(documents, f)


def load_documents(input_path):
    """Load saved processed documents."""

    with gzip.open(input_path, "rb") as f:
        documents = pickle.load(f)

    return documents
