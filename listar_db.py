import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("database/usuario.db")
cursor = conn.cursor()

# Apagar todas as ordens de serviço
cursor.execute("DELETE FROM ordens_servico")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='ordens_servico'")

# Apagar todos os usuários
cursor.execute("DELETE FROM usuario")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuario'")

# Inserir novamente o usuário admin
cursor.execute("INSERT INTO usuario (usuario, senha) VALUES (?, ?)", ("admin", "000000"))

# Salvar e fechar
conn.commit()
conn.close()

print("Banco de dados limpo. Usuário admin recriado com sucesso.")
