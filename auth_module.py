import os

from db_module import (get_cursor, create_table, create_user,
                       check_user, get_token, token_update,
                       mail_update, get_mail)


def db_existence_check():
    '''Сhecking if a person has a base.'''
    try:
        open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
             'user_data.db'))
    except IOError:
        create_table()
