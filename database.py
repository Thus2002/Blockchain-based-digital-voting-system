import sqlite3


def create_database():

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        voter_id TEXT UNIQUE,
        email TEXT,
        password TEXT,
        voted INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id TEXT,
        candidate TEXT
    )
    """)

    conn.commit()
    conn.close()


def register_voter(name, voter_id, email, password):

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO voters
        (name,voter_id,email,password)
        VALUES (?,?,?,?)
        """, (name, voter_id, email, password))

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def login_voter(voter_id, password):

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM voters
    WHERE voter_id=? AND password=?
    """, (voter_id, password))

    voter = cursor.fetchone()

    conn.close()

    return voter


def has_voted(voter_id):

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT voted FROM voters
    WHERE voter_id=?
    """, (voter_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0] == 1

    return False


def record_vote(voter_id, candidate):

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO votes(voter_id,candidate)
    VALUES (?,?)
    """, (voter_id, candidate))

    cursor.execute("""
    UPDATE voters
    SET voted=1
    WHERE voter_id=?
    """, (voter_id,))

    conn.commit()
    conn.close()


def get_results():

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT candidate, COUNT(*)
    FROM votes
    GROUP BY candidate
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_all_voters():

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name,voter_id,email,voted
    FROM voters
    """)

    voters = cursor.fetchall()

    conn.close()

    return voters
