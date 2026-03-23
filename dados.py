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
                    max_score INTEGER
                )
            ''')

    def save_score(self, nick, score):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT max_score FROM players WHERE nick = ?', 
                (nick,)
            )
            row = cursor.fetchone()
            
            if row is None:
                cursor.execute(
                    'INSERT INTO players (nick, max_score) VALUES (?, ?)', 
                    (nick, score)
                )
            else:
                old_score = row[0]
                if score > old_score:
                    cursor.execute(
                        'UPDATE players SET max_score = ? WHERE nick = ?', 
                        (score, nick)
                    )

    def get_top_scores(self, limit=5):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nick, max_score FROM players ORDER BY max_score DESC LIMIT ?", (limit,)
            )
            return cursor.fetchall()
        



    def login(self, nick, senha):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT senha FROM players WHERE nick = ?", (nick,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("INSERT INTO players (nick, senha, max_score) VALUES (?, ?, ?)", (nick, senha, 0 ))
            connection.commit()
            connection.close()
            return "criado"
        else:
            if row[0] == senha:
                connection.close()
                return "login"
            else:
                connection.close()
                return "erro"