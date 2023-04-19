import sqlite3


def get_cursor():
    con = sqlite3.connect('user_data.db')
    cursor = con.cursor()
    return cursor, con


def create_table():
    '''BD creating.'''
    cursor, con = get_cursor()
    cursor.execute("""CREATE TABLE user
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    mail TEXT
                    token TEXT)
                """)
    con.close()


def create_user(name, wb_token, mail):
    '''Аdding a new user.'''
    cursor, con = get_cursor()
    cursor.execute(
        "INSERT INTO user (name, mail, token) VALUES (?, ?, ?)", (
         name, mail, wb_token))
    con.commit()
    con.close()


def check_user(name):
    '''User exists checking.'''
    cursor, con = get_cursor()
    cursor.execute("SELECT name FROM user")
    for person in cursor.fetchall():
        person = person[0]
        if person == name:
            return True
    con.close()
    return False


def get_token(name):
    '''Getting token from database.'''
    cursor, con = get_cursor()
    cursor.execute("SELECT token FROM user WHERE name=name")
    token = cursor.fetchone()
    con.close()
    return token


def token_update(name, token):
    '''Refreshing token.'''
    cursor, con = get_cursor()
    cursor.execute("Update user SET token=token WHERE name=name")
    con.commit()
    con.close()


def get_mail(name):
    '''Getting mail.'''
    cursor, con = get_cursor()
    cursor.execute("SELECT mail FROM user WHERE name=name")
    mail = cursor.fetchone()
    con.close()
    return mail


def mail_update(name, mail):
    '''Refreshing mail.'''
    cursor, con = get_cursor()
    cursor.execute("Update user SET mail=mail WHERE name=name")
    con.commit()
    con.close()
