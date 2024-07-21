from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import torch
import numpy
import json
from pathlib import Path


class CategoriesClassifierBERT:
    _tokenizer: BertTokenizer
    _model: BertModel
    _device: torch.device
    _categories = 2

    def __init__(self):
        self._tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self._model = BertModel.from_pretrained(
            "bert-base-uncased", num_labels=self._categories
        )
        self._device = torch.device(
            "mps" if torch.backends.mps.is_available() else "cpu"
        )
        self._model.to(self._device)

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    def word_categorizer(self, words) -> dict:
        # Set random seed for reproducibility
        numpy.random.seed(42)
        torch.manual_seed(42)

        # Function to get BERT embeddings for a list of words
        def get_embeddings(words):
            inputs = self._tokenizer(
                words, return_tensors="pt", padding=True, truncation=True
            ).to(self._device)
            with torch.no_grad():
                outputs = self._model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]
            return embeddings.cpu().numpy()

        # Get embeddings for the words
        embeddings = get_embeddings(words)

        # Normalize embeddings
        scaler = StandardScaler()
        embeddings_normalized = scaler.fit_transform(embeddings)

        kmeans = KMeans(n_clusters=self._categories, random_state=42, init="k-means++")
        kmeans.fit(embeddings_normalized)
        labels = kmeans.labels_
        for i, word in enumerate(words):
            print(f"Word: {word}, Category: {labels[i]}")
        self._write_to_disk(words, labels)
        return labels

    def _write_to_disk(self, words, labels):
        categorized_data = {"data": []}
        for i, word in enumerate(words):
            categorized_data["data"].append({"word": word, "category": int(labels[i])})
        from datetime import datetime

        file_name = f"categorized-{datetime.now().strftime('%d-%m-%Y')}.json"
        file_path = Path(f"result/{file_name}")
        if file_path.exists():
            file_path.unlink()
        with open(f"results/{file_name}", "w+") as f:
            json.dump(categorized_data, f, indent=4)
