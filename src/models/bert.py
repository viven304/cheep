from transformers import BertTokenizer, BertModel, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import torch
import numpy
import json
from pathlib import Path
from datasets import load_dataset, load_metric, Dataset, DatasetDict
from src.models.preprocess_data import preprocess_data


class CategoriesClassifierBERT:
    _tokenizer: BertTokenizer
    _model: BertModel
    _sequenceModel: BertForSequenceClassification
    _device: torch.device
    _categories = 4

    def __init__(self):
        self._tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self._model = BertModel.from_pretrained(
            "bert-base-uncased", num_labels=self._categories
        )
        self._sequenceModel = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1550)
        self._device = torch.device(
            "mps"
        )
        self._model.to(self._device)
        self._sequenceModel.to(self._device)

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer
    
    def train(self):
        # Load and preprocess dataset
        train_df, val_df, category_to_id = preprocess_data()
        def tokenize_function(examples):
            return self._tokenizer(examples['words'], padding='max_length', truncation=True)

        # Convert DataFrame to Dataset format
        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)

        # Tokenize the datasets
        train_dataset = train_dataset.map(tokenize_function, batched=True)
        val_dataset = val_dataset.map(tokenize_function, batched=True)
        print(train_df["label"].nunique())

        # Define training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            evaluation_strategy='epoch',
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            no_cuda=True
        )

        # Define metric
        metric = load_metric('accuracy')

        # Define compute_metrics function
        def compute_metrics(p):
            print(p.predictions)
            predictions = torch.argmax(p.predictions, axis=1)
            return metric.compute(predictions=predictions, references=p.label_ids)

        # Initialize Trainer
        trainer = Trainer(
            model=self._sequenceModel,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=compute_metrics,
        )

        # Train the model
        trainer.train()
        def predict_category(words):
            inputs = self._tokenizer(words, return_tensors='pt', padding=True, truncation=True)
            outputs = self._sequenceModel(**inputs)
            predictions = torch.argmax(outputs.logits, dim=1)
            category = [k for k, v in category_to_id.items() if v == predictions.item()][0]
            return category

        # Example usage
        new_words = ["apple", "banana", "kiwi", "mango"]
        predicted_category = predict_category(new_words)
        print(f'Predicted category for {new_words}: {predicted_category}')
        trainer.save_model("./retrained_model")


    def cli_word_categorizer(self, words) -> dict:
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
