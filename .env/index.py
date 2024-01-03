from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

#Rotas
@app.route('/')
def index01():
    return render_template('index.html')

@app.route('/notas-alunos')
def allgrades():
    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Query para buscar alunos
    query_alunos = "SELECT cpf, estudante_nome FROM matheus_TB_student"
    mycursor.execute(query_alunos)
    alunos = mycursor.fetchall()

    return render_template('notas_aluno.html', alunos=alunos)

@app.route('/aluno-login')
def aluno_login():
    return render_template('aluno-login.html')

@app.route('/processar-login-aluno', methods=['POST'])
def processar_login_aluno():
    cpf = request.form['cpf']
    senha = request.form['senha']

    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Consulta para verificar se o aluno existe
    query = "SELECT 1 FROM matheus_TB_student WHERE cpf = %s AND senha = %s"
    values = (cpf, senha)

    mycursor.execute(query, values)
    aluno_exists = mycursor.fetchone()

    if aluno_exists:
        # Aluno existe, redirecione para a página de notas do aluno
        return redirect(url_for('exibir_notas', aluno=cpf))    
    else:
        # Aluno não existe ou credenciais inválidas
        return 'Credenciais inválidas'
    

@app.route('/secretaria-login')
def secretaria_login():
    return render_template('secretaria-login.html')

@app.route('/processar-login-secretaria', methods=['POST'])
def processar_login_secretaria():
    usuario = request.form['usuario']
    senha = request.form['senha']

    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Consulta para verificar as credenciais no banco de dados
    query = "SELECT 1 FROM matheus_TB_employee WHERE usuario = %s AND senha = %s"
    values = (usuario, senha)

    mycursor.execute(query, values)
    result = mycursor.fetchone()

    if result:
        return render_template('home-secretaria.html')
    else:
        return 'Credenciais inválidas'

@app.route('/cadastrar-aluno')
def cadastrar_aluno():
    return render_template('cadastrar-aluno.html')

@app.route('/cadastrar-funcionario')
def cadastrar_funcionario():
    return render_template('cadastrar-funcionario.html')

@app.route('/cadastrar-disciplina')
def cadastrar_disciplina():
    return render_template('cadastrar-disciplina.html')


@app.route('/cadastrar-aluno', methods=['POST'])
def cadastrar_aluno01():
    nome = request.form['nome']
    cpf = request.form['cpf']
    senha = request.form['senha']

    # Conexão com o banco de dados
    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com', user='aluno_fatec', password='aluno_fatec', database='meu_banco' )
    mycursor = db.cursor()

    # Query para inserir dados na tabela matheus_TB_student
    query = "INSERT INTO matheus_TB_student (estudante_nome, cpf, senha) VALUES (%s, %s, %s)"
    values = (nome, cpf, senha)
    mycursor.execute(query, values)
    db.commit()
    return 'Cadastro confirmado'

@app.route('/cadastrar-funcionario', methods=['POST'])
def cadastrar_funcionario01():
    nome = request.form['nome']
    email = request.form['email']
    cpf = request.form['cpf']
    login = request.form['login']
    senha = request.form['senha']

    # Conexão com o banco de dados
    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com', user='aluno_fatec', password='aluno_fatec', database='meu_banco' )
    mycursor = db.cursor()

    # Query para inserir dados na tabela matheus_TB_employee
    query = "INSERT INTO matheus_TB_employee (nome, email, cpf, usuario, senha) VALUES (%s, %s, %s, %s, %s)"
    values = (nome, email, cpf, login, senha)

    mycursor.execute(query, values)
    db.commit()

    return 'Cadastro de funcionario confirmado'

@app.route('/cadastrar-disciplina', methods=['POST'])
def cadastrar_disciplina01():
    nome_disciplina = request.form['nome']

    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Query para inserir dados na tabela matheus_TB_discipline
    query = "INSERT INTO matheus_TB_discipline (nome_disciplina) VALUES (%s)"
    values = (nome_disciplina,)

    mycursor.execute(query, values)
    db.commit()

    return 'Disciplina cadastrada'

@app.route('/cadastrar-notas', methods=['GET'])
def cadastrar_notas001():
    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Query para buscar alunos
    query_alunos = "SELECT cpf, estudante_nome FROM matheus_TB_student"
    mycursor.execute(query_alunos)
    alunos = mycursor.fetchall()

    # Query para buscar disciplinas
    query_disciplinas = "SELECT id, nome_disciplina FROM matheus_TB_discipline"
    mycursor.execute(query_disciplinas)
    disciplinas = mycursor.fetchall()

    return render_template('cadastrar-notas.html', alunos=alunos, disciplinas=disciplinas)

@app.route('/cadastrar-notas', methods=['POST'])
def cadastrar_notas_post():
    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Capturar dados do formulário
    aluno_nome = request.form['aluno']
    disciplina_nome = request.form['disciplina']
    nota = request.form['nota']

    # Obter IDs a partir dos nomes
    aluno_id_query = "SELECT cpf FROM matheus_TB_student WHERE estudante_nome = %s"
    disciplina_id_query = "SELECT id FROM matheus_TB_discipline WHERE nome_disciplina = %s"

    mycursor.execute(aluno_id_query, (aluno_nome,))
    aluno_id = mycursor.fetchone()

    mycursor.execute(disciplina_id_query, (disciplina_nome,))
    disciplina_id = mycursor.fetchone()

    if not aluno_id or not disciplina_id:
        return 'Aluno ou disciplina não existem.'

    # Inserir dados na tabela matheus_TB_grades
    query = "INSERT INTO matheus_TB_grades (aluno_cpf, disciplina_id, nota) VALUES (%s, %s, %s)"
    values = (aluno_id[0], disciplina_id[0], nota)

    mycursor.execute(query, values)
    db.commit()

    return 'Nota cadastrada'

@app.route('/exibir-notas/', methods=['GET'])
def exibir_notas():
    # Obtenha o CPF do aluno selecionado
    aluno_cpf = request.args.get('aluno')

    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )
    mycursor = db.cursor()

    # Query para buscar notas do aluno
    query = """
        SELECT matheus_TB_discipline.nome_disciplina, matheus_TB_grades.nota
        FROM matheus_TB_grades
        JOIN matheus_TB_discipline ON matheus_TB_grades.disciplina_id = matheus_TB_discipline.id
        WHERE matheus_TB_grades.aluno_cpf = %s
    """

    mycursor.execute(query, (aluno_cpf,))
    notas = mycursor.fetchall()

    return render_template('exibir_notas.html', aluno_cpf=aluno_cpf, notas=notas)

app.run()