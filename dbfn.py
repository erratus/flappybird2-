import sqlite3

DB_FILE = "flappy_bird.db"


def db_init():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS SCORE(
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER DEFAULT 0
        )
    """
    )
    connection.commit()
    connection.close()


def db_print():
    connection = sqlite3.connect("flappy_bird.db")
    cursor = connection.cursor()
    print("Current score db in the format [game_id,score] : ", end=" ")
    cursor.execute("SELECT * FROM SCORE")
    rows = cursor.fetchall()
    print(rows)
    connection.commit()
    connection.close()


def save_game_state(score):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO SCORE(score) VALUES (?)", (score,))
    cursor.execute("SELECT MAX(score) FROM SCORE")
    highscore = cursor.fetchone()[0]
    connection.commit()
    connection.close()


save_game_state(10)


def load_game_state(score):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(score) FROM SCORE")
    highscore = cursor.fetchone()

    try:
        if highscore is None or highscore[0] is None:
            score = 0
        else:
            score = highscore[0]
        return score
    except sqlite3.Error as e:
        print("Error occurred while loading game state:", e)
        return 0
    finally:
        connection.close()
