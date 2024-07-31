from flask import Flask, redirect, render_template, request, url_for
import uuid, datetime

app = Flask(__name__)

def cadastrar_usuario(usuario):
    with open("usuarios.csv", "a") as file:
        file.write(f"\n{usuario['nome']},{usuario['email']},{usuario['password']}")

def verificar_usuario(email, senha):
    with open("usuarios.csv") as file:
        for linha in file.readlines():
            nome, email_usuario, senha_usuario = linha.strip().split(",")
            if email == email_usuario and senha == senha_usuario:
                return True
    return False

def cadastrar_sala(sala):
    with open("salas.csv", "a") as file:
        file.write(f"\n{str(uuid.uuid4())},{sala['tipo']},{sala['capacidade']},{sala['descricao']},Sim")

def mostrar_salas():
    with open("salas.csv") as file:
        salas = []
        for linha in file:
            valores = linha.strip().split(",")
            if len(valores) == 5:
                sala_id, tipo, capacidade, descricao, ativa = valores
                sala = {
                    "id": sala_id,
                    "tipo": tipo,
                    "capacidade": capacidade,
                    "descricao": descricao,
                    "ativa": ativa
                }
                salas.append(sala)
    return salas

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        cadastrar_usuario({"nome": request.form["nome"], "email": request.form["email"], "password": request.form["password"]})
        return redirect(url_for("home"))
    return render_template("cadastro.html")

@app.route("/gerenciar/lista-salas")
def lista_salas():
    salas = mostrar_salas()
    return render_template("listar-salas.html", salas=salas)

@app.route("/gerenciar/cadastrar-salas", methods=["GET", "POST"])
def cadastrar_salas():
    if request.method == "POST":
        cadastrar_sala({"tipo": request.form["tipo"], "capacidade": request.form["capacidade"], "descricao": request.form["descricao"]})
        return redirect(url_for("lista_salas"))
    return render_template("cadastrar-sala.html")

@app.route("/gerenciar/excluir-sala/<sala_id>", methods=["GET", "POST"])
def excluir_sala(sala_id):
    salas = mostrar_salas()
    salas = [sala for sala in salas if sala["id"] != sala_id]
    
    with open("salas.csv", "w") as file:
        for sala in salas:
            file.write(f"{sala['id']},{sala['tipo']},{sala['capacidade']},{sala['descricao']}\n")
    
    return redirect(url_for("lista_salas"))

@app.route("/gerenciar/desativar-sala/<sala_id>", methods=["GET", "POST"])
def desativar_sala(sala_id):
    salas = mostrar_salas()
    for sala in salas:
        if sala["id"] == sala_id:
            sala["ativa"] = "Não" if sala["ativa"] == "Sim" else "Sim"
    
    with open("salas.csv", "w") as file:
        for sala in salas:
            file.write(f"{sala['id']},{sala['tipo']},{sala['capacidade']},{sala['descricao']},{sala['ativa']}\n")
    
    return redirect(url_for("lista_salas"))

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

def carregar_reservas():
    reserva = []
    with open("reservas.csv") as file:
        for linha in file:
            sala_id, inicio, fim = linha.strip().split(",")
            reserva.append({
                "sala_id": sala_id,
                "inicio": datetime.datetime.fromisoformat(inicio),
                "fim": datetime.datetime.fromisoformat(fim)
            })
    return reserva

def salvar_reserva(sala_id, inicio, fim):
    with open("reservas.csv", "a") as file:
        file.write(f"{sala_id},{inicio},{fim}\n")

def verificar_reservas(sala_id, inicio, fim):
    for reserva in carregar_reservas():
        if reserva["sala_id"] == sala_id:
            if inicio < reserva["fim"] and fim > reserva["inicio"]:
                return True
    return False

@app.route("/detalhe-reserva")
def detalhe_reserva():
    sala_id = request.args.get("sala_id")
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    sala = next((s for s in lista_salas() if s["id"] == sala_id), None)

    return render_template("reserva/detalhe-reserva.html", sala=sala, inicio=inicio, fim=fim)


@app.route("/reservar", methods=["GET", "POST"])
def reservar_sala():
    salas = lista_salas()
    if request.method == "POST":
        sala_id = request.form.get("sala")
        inicio = request.form.get("inicio")
        fim = request.form.get("fim")
        inicio_dt = datetime.datetime.fromisoformat(inicio)
        fim_dt = datetime.datetime.fromisoformat(fim)

        if verificar_reservas(sala_id, inicio_dt, fim_dt):
            return render_template("reservar-sala.html", salas=salas, error="Conflito de horário! Escolha outro horário.")

        salvar_reserva(sala_id, inicio, fim)
        return redirect(url_for("detalhe-reserva", sala_id=sala_id, inicio=inicio, fim=fim))

    return render_template("reservar-sala.html", salas=salas)

app.run()