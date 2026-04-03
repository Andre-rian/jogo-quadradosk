import sqlite3

class DatabaseManager:
    def __init__(self, db_name="ranking.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    nick TEXT PRIMARY KEY,
                    senha TEXT,
                    max_score INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def login(self, nick, senha):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT senha FROM players WHERE nick = ?", (nick,))
            row = cursor.fetchone()

            if row is None:
                # Se o player não existe, cria um novo
                cursor.execute("INSERT INTO players (nick, senha, max_score) VALUES (?, ?, ?)", (nick, senha, 0))
                conn.commit()
                return "criado"
            else:
                # Se existe, verifica a senha
                return "login" if row[0] == senha else "erro"

    def save_score(self, nick, score):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT max_score FROM players WHERE nick = ?', (nick,))
            row = cursor.fetchone()
            
            if row and score > row[0]:
                cursor.execute('UPDATE players SET max_score = ? WHERE nick = ?', (score, nick))
                conn.commit()

    def get_top_scores(self, limit=5):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nick, max_score FROM players ORDER BY max_score DESC LIMIT ?", (limit,))
            return cursor.fetchall()