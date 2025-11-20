from flask import Flask, jsonify, request, send_from_directory


app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory("front", "index.html")

@app.route('/<path:filename>')
def arquivos_estaticos(filename):
    return send_from_directory('front', filename)



# Lista de tarefas (banco de dados temporário em memória)
tarefas = []

# Prioridades e origens válidas
prioridades_validas = ["Urgente", "Alta", "Média", "Baixa"]
origens_validas = ["Email", "Telefone", "Chamado do Sistema"]


# ROTA 1 - Listar todas as tarefas
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)



# ROTA 2 - Criar nova tarefa
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()

    # Validação simples
    if not dados.get("titulo") or not dados.get("prioridade") or not dados.get("origem"):
        return jsonify({"erro": "Campos obrigatórios: titulo, prioridade, origem"}), 400

    if dados["prioridade"] not in prioridades_validas:
        return jsonify({"erro": "Prioridade inválida"}), 400

    if dados["origem"] not in origens_validas:
        return jsonify({"erro": "Origem inválida"}), 400

    nova_tarefa = {
        "id": len(tarefas) + 1,
        "titulo": dados["titulo"],
        "prioridade": dados["prioridade"],
        "origem": dados["origem"],
        "status": "Pendente"
    }

    tarefas.append(nova_tarefa)
    return jsonify({"mensagem": "Tarefa criada com sucesso!", "tarefa": nova_tarefa}), 201



# ROTA 3 - Atualizar status ou prioridade
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    dados = request.get_json()
    for tarefa in tarefas:
        if tarefa["id"] == id:
            if "status" in dados:
                tarefa["status"] = dados["status"]
            if "prioridade" in dados:
                if dados["prioridade"] in prioridades_validas:
                    tarefa["prioridade"] = dados["prioridade"]
                else:
                    return jsonify({"erro": "Prioridade inválida"}), 400
            return jsonify({"mensagem": "Tarefa atualizada com sucesso!", "tarefa": tarefa})
    return jsonify({"erro": "Tarefa não encontrada"}), 404



# ROTA 4 - Deletar uma tarefa
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    global tarefas
    tarefas = [t for t in tarefas if t["id"] != id]
    return jsonify({"mensagem": f"Tarefa {id} removida com sucesso!"})



# ROTA 5 - Verificar tarefa urgente
@app.route("/tarefas/urgente", methods=["GET"])
def pegar_urgente():
    for prioridade in prioridades_validas:
        for t in tarefas:
            if t["prioridade"] == prioridade and t["status"] == "Pendente":
                return jsonify(t)
    return jsonify({"mensagem": "Nenhuma tarefa urgente encontrada."})



# Executando
if __name__ == "__main__":
    app.run(debug=True)
