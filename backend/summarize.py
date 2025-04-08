from universal_extractor import extract_article
from translate import translate_text
from transformers import T5Tokenizer, T5ForConditionalGeneration

summarizer_model = T5ForConditionalGeneration.from_pretrained("t5-base")
summarizer_tokenizer = T5Tokenizer.from_pretrained("t5-base")

def summarize_text(text, max_input_length=512, max_output_length=150):
    input_text = "summarize: " + text
    input_ids = summarizer_tokenizer.encode(
        input_text, return_tensors="pt", truncation=True, max_length=max_input_length
    )
    summary_ids = summarizer_model.generate(
        input_ids,
        max_length=max_output_length,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def main():
    url = input("🔗 Enter article URL: ")
    title, content = extract_article(url)

    if not content:
        print("❌ Could not extract content.")
        return

    print(f"\n📌 Original Title: {title}")
    print("\n🔄 Translating if needed...")
    translated_text = translate_text(content)

    print("\n🧠 Abstractive Summary:\n")
    summary = summarize_text(translated_text)
    print(summary)

if __name__ == "__main__":
    main()
