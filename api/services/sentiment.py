from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

MODEL_NAME = "triagungj/indobert-large-p2-stock-news"

# Load model/tokenizer once (avoid reloading each call)
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
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
