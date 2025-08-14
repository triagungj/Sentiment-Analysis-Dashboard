from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
import os

MODEL_NAME = "triagungj/indobert-large-p2-stock-news"
LOCAL_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pretrained_model')

# Label mapping
i2w = {0: "positive", 1: "neutral", 2: "negative"}

# Check if local model exists
if os.path.exists(LOCAL_MODEL_PATH):
    print(f"Loading model from local path: {LOCAL_MODEL_PATH}")
    tokenizer = BertTokenizer.from_pretrained(LOCAL_MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(LOCAL_MODEL_PATH)
else:
    print(f"Downloading model from Hugging Face and saving to: {LOCAL_MODEL_PATH}")
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
    os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)
    tokenizer.save_pretrained(LOCAL_MODEL_PATH)
    model.save_pretrained(LOCAL_MODEL_PATH)
model.eval()

# Label mapping
i2w = {0: "positive", 1: "neutral", 2: "negative"}

def predict_sentiment(text: str):
    """Run sentiment prediction for given text and return label + confidence."""
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=128,
        truncation=True,
        padding=True
    )
    with torch.no_grad():
        outputs = model(**inputs)
        probs = softmax(outputs.logits, dim=1)
        predicted_label = torch.argmax(probs, dim=1).item()
        confidence = torch.max(probs).item()

    return {
        "label": i2w[predicted_label],
        "confidence": round(confidence, 4)
    }
