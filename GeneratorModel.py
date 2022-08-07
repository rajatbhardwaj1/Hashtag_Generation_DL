import argparse
import torch
import pandas as pd
from transformers import AutoTokenizer, BartForConditionalGeneration

class GeneratorModel:
    def __init__(self, args, model_path):
        self.args = args
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.bart_tokenizer = AutoTokenizer.from_pretrained('ankur310794/bart-base-keyphrase-generation-kpTimes')
        self.bart_model = BartForConditionalGeneration.from_pretrained('ankur310794/bart-base-keyphrase-generation-kpTimes')
        self.bart_model.load_state_dict(torch.load(model_path)['bart_model_state_dict'])
        self.bart_model.to(self.device)
    
    def generate(self, text):
        tok = self.bart_tokenizer(text, return_tensors='pt')
        inputs_embeds, input_ids, attention_mask = None, tok["input_ids"].to(self.device), tok["attention_mask"].to(self.device)
        curr_hashtags = self.bart_model.generate(input_ids=input_ids, inputs_embeds=inputs_embeds, attention_mask=attention_mask,
            length_penalty=self.args.length_penalty, num_beams=self.args.beam_size,
            min_length=self.args.decoder_min_length, max_length=64,
            early_stopping=self.args.decoder_early_stopping, no_repeat_ngram_size=self.args.no_repeat_ngram_size)
        output = self.bart_tokenizer.decode(curr_hashtags[0], skip_special_tokens=True)
        
        outputs = output.split('|')
        out_final = ""
        for o in outputs: out_final += f"#{o} "
        return out_final.strip()

