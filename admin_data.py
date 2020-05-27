from vedis import Vedis
import config

def get_current_state(user_id):
    with Vedis(config.admin_db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_START.value  # значение по умолчанию - начало диалога

def set_state(user_id, value):
    with Vedis(config.admin_db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False
def get_current_tag(user_id):
    with Vedis(config.tag_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_START.value  # значение по умолчанию - начало диалога

def set_tag(user_id, value):
    with Vedis(config.tag_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False
