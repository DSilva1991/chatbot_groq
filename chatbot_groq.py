import os
import requests
import json
from flask import Flask, request, jsonify
from groq import Groq  # usa o client oficial

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/interpretar", methods=["POST"])
def interpretar():
    pergunta = request.json.get("pergunta", "")
    resp = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Gera apenas SQL Oracle para perguntas sobre finanças/vendas/compras."},
            {"role": "user", "content": pergunta}
        ],
        model="llama3-8b-8192", temperature=0.2
    )
    sql = resp.choices[0].message.content.strip()
    if sql.lower().startswith("select"):
        return jsonify({"sql": sql})
    return jsonify({"sql": None, "mensagem": "SQL inválido ou não reconhecido."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Porta do Render ou 5000 localmente
    app.run(host="0.0.0.0", port=port)    