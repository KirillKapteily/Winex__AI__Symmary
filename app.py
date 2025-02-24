from flask import Flask, request, render_template, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration

app = Flask(__name__)

# Загружаем модель и токенизатор (делается 1 раз при запуске)
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text, max_length=100):
    """Функция суммаризации текста с использованием T5-small."""
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        min_length=30, 
        length_penalty=2.0, 
        num_beams=2,  # Быстрее, чем 4
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"error": "Текст не должен быть пустым"}), 400

    summary = summarize_text(text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
