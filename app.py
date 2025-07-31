from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy #Utilizado para manipular os dados para o banco de dados
from sqlalchemy import text # Utilizado no connection para poder receber o valor do em texto da versão do sql
import bcrypt #Biblioteca que irá fornecer a criptografia para as senhas.
# import psycopg2 # Biblioteca importante para a conecção com o banco de dados postgres
import re #para usar expressões regulares
#Biblioteca que gerencia o login dentro da aplicação
from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
#Biblioteca para usar corretamente o .env e proteger dados sensíveis
from dotenv import load_dotenv
import os # necessário para o funcionamento do .env (embora essa biblioteca tenha muitos outros usos)
from models import Usuarios
from config import db # Importa o inicializador do banco de dados
load_dotenv() #importação para o funcionamento do .env

app = Flask(__name__)
logMan = LoginManager(app)
#O view redireciona para a rota que realiza o login evitando que usuario sem acesso receba a mensagem de não autorizado em uma página 401
logMan.login_view = "/"
#Mensagem que aparecerá na pagina de login
logMan.login_message = "Você precisa estar logado para acessar esta página."
logMan.login_message_category = "warning"

#Chave secreta é usada para que seja guardada as informações da sessão.
CHAVE_SECRETA = os.getenv("CHAVESEGURA")
# Adicione uma verificação para garantir que a chave não seja None em produção
if not CHAVE_SECRETA:
    raise ValueError("CHAVESEGURA não definida! Verifique seu arquivo .env ou variáveis de ambiente.")
app.secret_key = CHAVE_SECRETA
# Configuração do banco de dados

POSTGRES_URI = os.getenv("DATABASE_URL")
# Verificações básicas para garantir que as variáveis do DB foram carregadas
if not POSTGRES_URI:
    raise ValueError("DATABASE_URL não definida! Verifique o arquivo .env ou variáveis de ambiente")
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
db.init_app(app)

#--------------------------------------------------------------------------------------------------------#
                                            #Funções do projeto#
#--------------------------------------------------------------------------------------------------------#

#Função que verifica se o e-mail foi escrito dentro do padrão correto#
def verifica_email(email):
    #Expressão regular para verificação da escrita correta de e-mail.
    # "exemplo" + @ + "email" . "com" e ou ."br"
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.fullmatch(padrao, email):
        return True
    else:
        return False
    
#Função que formata os nomes para deixar padronizdo com as iniciais maiúsculas#
def formatar_nome(nome):
    particulas = {"da", "das", "de", "do", "dos", "e"}
    # Aplica title() pra capitalizar
    nome_formatado = nome.title()
    
    # Quebrar o nome em palavras para avaliar as partículas
    palavras = nome_formatado.split()
    
    # Ajustar partículas para minúsculo
    resultado = []
    for palavra in palavras:
        if palavra.lower() in particulas:
            resultado.append(palavra.lower())
        else:
            resultado.append(palavra)
    
    return " ".join(resultado)
#-------------------------------------------Verificador da conexão com o banco de dados--------------------------#
try:
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("✅ Conectado! Versão do PostgreSQL:", result.fetchone())
except Exception as e:
    print("❌ Erro ao conectar com o PostgreSQL:")
    print(e)

#---------------------------------------------------------Rotas do projeto-----------------------------------------#

#verificador se o usuario está logado

@logMan.user_loader #quando estamos logado o que fica guardado é o id
def user_loader(id):
    # usuario = db.session.query(Usuarios).filter_by(id=id).first()
    usuario = Usuarios.query.filter_by(id=id).first()
    return usuario
#Rota do index da página que tem o login
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").lower().strip()
        senha = request.form.get("senha","").lower().strip()
        usuario_cadastrado = Usuarios.query.filter_by(usuario=usuario).first()
        
        if usuario_cadastrado:
            #Verificador se a senha com hash corresponde com a senha do salva
            if bcrypt.checkpw(senha.encode('utf-8'), usuario_cadastrado.senha):
                login_user(usuario_cadastrado)
                return redirect(url_for("home"))
            else:
                flash(f"Senha incorreta! Tente novamente.", "danger")
                return redirect(url_for("index"))
        else:
            flash(f"Usuário não está cadastrado! Cadastre-se para efetuar o login", "warning")
            return redirect(url_for("index"))
    return render_template("index.html")

#Rota para realizar o logout do sistema.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#Rota da cadastro
@app.route("/cadastro", methods=["POST","GET"])
def cadastro():
    if request.method == "POST":
        nome_recebido= request.form.get("nome","").strip() #as "" faz com que se o input vir sem dados o fluxo não quebre aos tentar aplicar o strip() é preciso validar o dado antes de enviar ao banco de dados
        nome= formatar_nome(nome_recebido)
        email = request.form.get("email", "").lower().strip()
        cep = request.form.get("cep", "").strip()
        rua = request.form.get("rua", "").strip()
        numero =request.form.get("numero", "").strip()
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro", "").strip()
        cidade= request.form.get("cidade", "").strip().title()
        estado= request.form.get("estado", "").upper()
        usuario= request.form.get("usuario", "").lower().strip()
        senha= request.form.get("senha", "").strip()
        
        ##---------------------------------------Validações---------------------------------------##
        #Nos campos obrigatórios se precisamos informar ao usuário qual campo foi preenchido de forma incorreta.
        #Assim as validações deve ser individualizadas e ao final, caso existam erros, retornar os erros ao usuário.
        #Inicia com um verificador de erros inicialmente configurado no False, na ocorrencia de erro irá modificar para TRUE
        existe_erro= False
        
        #Verifica se o nome está preenchido
        if not nome:
            flash("O campo 'Nome' é obrigatório.", "warning")
            existe_erro = True
        
        #Verifica se email está preenchido e se o formato está correto
        if not email:
            flash("O campo 'E-mail' é obrigatório.", "warning")
            existe_erro =True    
        #Verifica se no input o formato do e-mail está correto. Não estando retorna um aviso ao usuário
        elif not verifica_email(email):
            flash(f"{email} - Não corresponde ao padrão de e-mail:'exemplo@email.com'", "danger")
            existe_erro =True    
        
        #Verifica se o CEP está preenchido
        if not cep:
            flash("O campo 'CEP' é obrigatório.", "warning")
            existe_erro =True    
            
        #Verifica se a Rua está preenchida   
        if not rua:
            flash("O campo 'Rua' é obrigatório.", "warning")
            existe_erro =True
                
        #Verifica se o número está preenchido        
        if not numero:
            flash("O campo 'Número' é obrigatório.", "warning")
            existe_erro =True    
        
        #Verifica se o bairro está preenchido
        if not bairro:
            flash("O campo 'Bairro' é obrigatório.", "warning")
            existe_erro =True    
            
        #Verifica se a cidade está preenchida
        if not cidade:
            flash("O campo 'Cidade' é obrigatório.", "warning")
            existe_erro =True 
        
        #Verifica se o Estado está preenchido
        if not estado:
            flash("O campo 'Estado' é obrigatório.", "warning")
            existe_erro =True      

        #Verifica se o Usuário está preenchido
        if not usuario:
            flash("O campo 'Usuário' é obrigatório.", "warning")
            existe_erro =True    
        
        #Verifica se a senha está preenchida
        if not senha:
            flash("O campo 'Senha' é obrigatório.", "warning")
            existe_erro =True    
        
        #Verifica se todos os campos foram preenchidos. Se não forem não realiza o cadastro e retorna uma informação ao usuário.
        #Na existencia de erro irá redirecionar para a página cadastro com as informações.            
        if existe_erro:
            return redirect(url_for("cadastro"))

        #-------------------------------------------------------------------------------------------------------#
        #-------------------------------------Segundo nivel de verificação--------------------------------------#
        #Busca do Banco de dados se há usuario com o mesmo nome
        cadastro_existente = Usuarios.query.filter_by(usuario=usuario).first() #realiza a consulta no banco.
        
        #Verifica se o nome cadastrado já se encontra no banco de dados, se já constar retornará um aviso ao usuário
        if cadastro_existente:
            flash(f"Nome de usuário já existe! Por favor, utilize outro nome de usuário.", "warning")
            return redirect(url_for("cadastro"))
        else:
        #Conversão da senha em hash pelo bcrypt
            hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            novo_usuario = Usuarios(nome=nome, email=email,cep=cep,rua=rua,numero=numero,complemento=complemento,bairro=bairro,cidade=cidade, estado=estado, usuario=usuario,senha=hashed)
            db.session.add(novo_usuario)
            db.session.commit()
            
            #Ao cadastras usando o login_user já deixa o usuário automaticamente logado no sistema
            login_user(novo_usuario)
            return redirect(url_for("sucesso"))  # Evita resubmissão do formulário
        
    return render_template("cadastro.html")

        
    
@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True) 
    