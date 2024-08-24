"""
Preprocess data into a format that transformers will understand
"""
import json
import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data():
    # Load your dataset
    with open('data/answers.json', 'r') as file:
        data = json.load(file)

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data)

    # Flatten the data: create one row per word with the corresponding category label
    df = df.explode('words')

    # Map categories to numerical labels
    category_to_id = {category: idx for idx, category in enumerate(df['category'].unique())}
    df['label'] = df['category'].map(category_to_id)
    print(df)

    # Split into train and validation sets
    train_df, val_df = train_test_split(df, test_size=0.25, stratify=df['label'])
    return train_df, val_df, category_to_id
