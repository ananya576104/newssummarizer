

import re
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer

model_path = "Helsinki-NLP/opus-mt-hi-en"
tokenizer = MarianTokenizer.from_pretrained(model_path)
model = MarianMTModel.from_pretrained(model_path)

def clean_translated_text(text):
    text = re.sub(r"(image source|Getty Images|@[\w]+|hours ago|external sites)", "", text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def translate_text(text, max_chunk_length=450):
    lang = detect(text)
    if lang == "en":
        return text  # No translation needed

    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        try:
            inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs, max_length=512, num_beams=4)
            output = tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(output)
        except Exception as e:
            print(f"❌ Translation error in chunk {i}: {e}")
            translated_chunks.append("[Translation failed]")

    return clean_translated_text(" ".join(translated_chunks))


