import sqlite3
conexao = sqlite3.connect('exemplo.db')
cursor = conexao.cursor()

cursor.execute('''
     CREATE TABLE Alunos (
     ID Integer Primary Key,
     Nome Text Not Null,
     Idade Int Integer,
     Curso Text)
     ''')

# conexao.commit()

cursor.execute('''
Insert Into Alunos (Nome, Idade, Curso)
Values ("Pedro", 21, "Programador de sistemas"),
        ("Carla", 22, "Medicina"),
        ("Marcos", 30, "Direito")''')

conexao.commit()

print("Banco de dados criado")