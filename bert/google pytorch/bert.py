import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM

#pre-trained tokenizer
tokenizer =  BertTokenizer.from_pretrained('bert-base-uncased')

text = "Who was Jim Henson ? Jim Henson was a puppeteer"
tokenized_text = tokenizer.tokenize(text)

#masking a token
mask_index = 6
tokenized_text[mask_index] = '[MASK]'
assert tokenized_text == ['who', 'was', 'jim', 'henson', '?', 'jim', '[MASK]', 'was', 'a', 'puppet', '##eer']

#converting token to vocab indexes
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
print(indexed_tokens)

#defining bidirectional indices
segments_ids = [0,0,0,0,0,1,1,1,1,1,1]

#tensoring the inputs for pytorch
tokens_tensor = torch.tensor(indexed_tokens)
segments_tensor = torch.tensor(segments_ids)
print(tokens_tensor)
print(segments_tensor)

#init the BERT model to get the hidden state
#1. load the pre-trained weights
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

#2. Predict hidden state features for each layer
encoded_layers, _ = model(tokens_tensor, segments_tensor)
#check if prediction is made for all 12 hidden layers
assert len(encoded_layers) == 12

#3. Predicting using BERT Masked Language Model
# predicting all tokens
predictions = model(tokens_tensor, segments_tensor)

#4. confirm prediction
predicted_index = torch.argmax(predictions[0, mask_index]).item()
predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
print(predicted_token)