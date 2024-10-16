from flask import Flask, redirect, render_template, request, url_for
import datetime
from reserva_app.database import *

app = Flask(__name__)

def busca_binaria(lista, elemento):
    inicio = 0
    fim = len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == elemento:
            return meio
        elif lista[meio] > elemento:
            fim = meio - 1
        else:
            inicio = meio + 1
    return -1

def cadastrar_usuario(usuario):
    salvar_db(usuario, "Usuario")

def verificar_usuario(email, senha):
    salas = ler_db("Usuario")
    for linha in salas:
        nome, email_usuario, senha_usuario = linha.strip().split(",")
        if email == email_usuario and senha == senha_usuario:
            return True
    return False

def cadastrar_sala(sala):
    salvar_db(sala, "Sala")

def mostrar_salas():
    return ler_db("Sala")

@app.route("/")
def home():
    init_db()
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
    excluir_sala_db(sala_id)
    return redirect(url_for("lista_salas"))

@app.route("/gerenciar/desativar-sala/<sala_id>", methods=["GET", "POST"])
def desativar_sala(sala_id):
    salas = mostrar_salas()
    for sala in salas:
        if sala["id"] == sala_id:
            update_sala_db(sala["id"], sala["ativa"])

    return redirect(url_for("lista_salas"))

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

def carregar_reservas():
    return ler_db("Reserva")

def salvar_reserva(sala_id, inicio, fim):
    salvar_db([sala_id, inicio, fim], "Reserva")

def verificar_reservas(sala_id, inicio, fim):
    for reserva in ler_db("Reserva"):
        if reserva["sala_id"] == sala_id:
            if inicio < reserva["fim"] and fim > reserva["inicio"]:
                return True
    return False

@app.route("/detalhe-reserva")
def detalhe_reserva(sala_id, inicio, fim):
    sala = next((s for s in mostrar_salas() if s["id"] == sala_id), None)

    return render_template("detalhe-reserva.html", sala=sala, inicio=inicio, fim=fim)


@app.route("/reservar", methods=["GET", "POST"])
def reservar_sala():
    salas = mostrar_salas()
    if request.method == "POST":
        sala_id = request.form.get("sala")
        inicio = request.form.get("inicio")
        fim = request.form.get("fim")
        inicio_dt = datetime.datetime.fromisoformat(inicio)
        fim_dt = datetime.datetime.fromisoformat(fim)

        if verificar_reservas(sala_id, inicio_dt, fim_dt):
            return render_template("reservar-sala.html", salas=salas, error="Conflito de horário! Escolha outro horário.")

        salvar_reserva(sala_id, inicio_dt, fim_dt)
        return redirect(url_for("reservar_sala"))

    return render_template("reservar-sala.html", salas=salas)
   
app.run(debug=True)