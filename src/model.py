from datasets import load_dataset, Dataset
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from utils import preprocess_data
from pathlib import Path

class DialoGPT:
    _tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    _model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    _device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    @property
    def model(self):
        return self._model
    
    def dialogue_loop(self):
        chat_history_ids = None
        while True:
            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = self._tokenizer.encode(input(">> ") + self._tokenizer.eos_token, return_tensors='pt')
            # append the new user input tokens to the chat history
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

            # generated a response while limiting the total chat history to 1000 tokens, 
            chat_history_ids = self._model.generate(bot_input_ids, max_length=1000, pad_token_id=50000)

            # pretty print last ouput tokens from bot
            print("Cheep: {}".format(self._tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

    def preprocess_function(self, examples):
        return self._tokenizer(examples['text'], truncation=True, padding='max_length', max_length=128)
    
    def retrain(self):
        root = Path.cwd()
        print(f"Project root: {root}")
        if not Path("data/dataset.json").exists():
            preprocess_data(root / "data" / "raw_data.json")
        # Load your dataset
        dataset = load_dataset('json', data_files='data/dataset.json', split='train')

        # Flatten the dialog to a single list of strings
        flat_dialogs = []
        for dialog in dataset:
            flat_dialogs.extend(dialog)
            
        if self._tokenizer.pad_token is None:
            self._tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        # Convert the flat dialogs to the format required by the tokenizer
        dataset = Dataset.from_dict({'text': flat_dialogs})
        tokenized_dataset = dataset.map(self.preprocess_function, batched=True)

        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=3,
            per_device_train_batch_size=2,
            save_steps=10_000,
            save_total_limit=2,
            logging_dir='./logs',
            logging_steps=500,
            use_mps_device=True,
        )
        trainer = Trainer(
            model=self._model,
            args=training_args,
            train_dataset=tokenized_dataset,
        )
        trainer.train()
        self._model.save_pretrained(root / "retrained_model")
        self._tokenizer.save_pretrained(root / "retrained_model")
        return