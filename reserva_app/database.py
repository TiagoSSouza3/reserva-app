from reserva_app.conexao_bd import conexao_fechar, conexao_abrir

def init_db():
    con = conexao_abrir("localhost", "root", "", "reserva_app")
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL
            
        );

        CREATE TABLE IF NOT EXISTS Reservas (
            id  INT PRIMARY KEY AUTO_INCREMENT,
            dt_inicio DATETIME NOT NULL,
            dt_final DATETIME NOT NULL,
            FOREIGN KEY (Sala_id) REFERENCES Sala(id)
            
        );

        CREATE TABLE IF NOT EXISTS Sala (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tipo VARCHAR(255) NOT NULL,
            capacidade INT NOT NULL,
            descricao VARCHAR(255),
            disponilidade BOOLEAN
            
        );""")

    conexao_fechar(cursor)
    conexao_fechar(con)
    return


def salvar_db(conteudo, tipo):
    con = conexao_abrir("localhost", "root", "", "reserva_app")
    cursor = con.cursor()
    sql = ""

    match tipo:
        case "Usuario":
            sql = "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (conteudo['nome'], conteudo['email'], conteudo['password']))
        case "Reserva":
            sql = "INSERT INTO Reserva (Sala_id, dt_inicio, dt_final) VALUES (%s, %s, %s)"
            cursor.execute(sql, (conteudo[0], conteudo[1], conteudo[2]))
        case "Sala":
            sql = "INSERT INTO Sala (tipo_da_sala, capacidade, descricao, disponibilidade) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (conteudo['tipo'], conteudo['capacidade'], conteudo['descricao'], True))
    
    con.commit()
    conexao_fechar(cursor)
    conexao_fechar(con)
    return
    
def ler_db(tipo):
    con = conexao_abrir("localhost", "root", "", "reserva_app")
    cursor = con.cursor()
    sql = ""
    conteudo = []

    match tipo:
        case "Usuario":
            sql = "SELECT * FROM Usuario (nome, email, senha)"
            cursor.execute(sql)
            for (registro) in cursor:
                usuario = {
                    "nome": registro[0],
                    "email": registro[1],
                    "password": registro[2]
                }
                conteudo.append(usuario)
        case "Reserva":
            sql = "SELECT * FROM Reserva (Sala-id, dt_inicio, dt_final)"
            cursor.execute(sql)
            for (registro) in cursor:
                reserva = {
                    "sala_id": registro[0],
                    "inicio": registro[1],
                    "fim": registro[2]
                }
                conteudo.append(reserva)
        case "Sala":
            sql = "SELECT * FROM Sala (tipo_da_sala, capacidade, descricao, disponibilidade)"
            cursor.execute(sql)
            for (registro) in cursor:
                sala = {
                    "tipo": registro[0],
                    "capacidade": registro[1],
                    "discricao": registro[2],
                    "ativa": registro[3]
                }
                conteudo.append(sala)

    cursor.close()
    conexao_fechar(con)

    return conteudo

def update_sala_db(sala_id, disponibilidade):
    con = conexao_abrir("localhost", "root", "", "reserva_app")
    cursor = con.cursor()

    sql = "UPDATE Sala SET disponibilidade = (%s) WHERE id = (%s),"
    cursor.execute(sql, (disponibilidade, sala_id))
    con.commit()

    cursor.close()
    conexao_fechar(con)
    return

def excluir_sala_db(sala_id):
    con = conexao_abrir("localhost", "root", "", "reserva_app")
    cursor = con.cursor()

    sql = "DELETE FROM Sala WHERE id = (%s)"
    cursor.execute(sql, (sala_id))
    con.commit()

    cursor.close()
    conexao_fechar(con)
    return