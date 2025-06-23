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
            {"role": "system", "content": ("Gera apenas SQL Oracle para perguntas sobre finanças/vendas/compras." 
            "A tabela de vendas chama-se 'vendas' e a de compras chama-se 'compras'. Ambas com colunas de total para os valores e data_evento para saber quando foi o registo"
            "Se a pergunta contiver o nome de um mês (ex:Janeiro), gera o SQL correspondente ao mês respectivo."
            "Devolve apenas o SQL sem justificações e não inventes colunas ou tabelas.")},
            {"role": "user", "content": pergunta}
        ],
        model="llama3-8b-8192", temperature=0.2
    )
    sql = resp.choices[0].message.content.strip()
    if sql.lower().startswith("select"):
        return jsonify({"sql": sql})
    return jsonify({"sql": None, "mensagem": "Não consegui entender o que pertende refaça a sua questão."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Porta do Render ou 5000 localmente
    app.run(host="0.0.0.0", port=port)    