import sqlite3
conexao = sqlite3.connect('exemplo.db')
cursor = conexao.cursor()

cursor.execute('''
      CREATE TABLE If Not Exists Alunos (
     ID Integer Primary Key,
      Nome Text Not Null,
      Idade Int Integer,
      Curso Text)
      ''')
conexao.commit()
def inserir_dados(nome,idade,curso):

        cursor.execute('''
Insert Into Alunos (Nome, Idade, Curso)
Values (?,?,?)''', (nome, idade, curso))

conexao.commit()

nome = input("Digite o nome do aluno:")
idade = int(input("Digite a idade do aluno:"))
curso = input("Digite nome do curso:")
inserir_dados(nome,idade,curso)

