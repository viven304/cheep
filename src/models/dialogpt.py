from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class DialoGPT:
    _tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    _model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    
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