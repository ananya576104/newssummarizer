from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-hi-en"

print("📦 Downloading tokenizer and model...")

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

print("💾 Saving locally to ./my_custom_translator")

tokenizer.save_pretrained("./my_custom_translator")
model.save_pretrained("./my_custom_translator")

print("✅ Model saved locally.")
