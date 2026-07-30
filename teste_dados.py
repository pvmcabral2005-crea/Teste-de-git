import sqlite3
conexao = sqlite3.connect("ficha.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM Ingredientes")

Ingredientes = cursor.fetchall()
print("Ingredientes cadastrados com sucesso")

for ingrediente in Ingredientes:
        print(f"Ingrediente: {ingrediente[0]}| Quantidade_comprada{ingrediente[1]}| Valor_ingrediente{ingrediente[2]}| Quant_usada{ingrediente[3]}| Unidade{ingrediente[4]}| Valor_final{ingrediente[5]}")
