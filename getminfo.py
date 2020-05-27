import json

def get_user_cell(chatid):
    m = json.load(open("marathons_list.json", "r"))
    try:
        return m[chatid]
    except KeyError:
        return False
def set_user_cell(chatid, value):
    m = json.load(open("marathons_list.json", "r"))
    try:
        m[chatid] = value
        json.dump(m, open("marathons_list.json", "w"))
    except:
        return False
def tag_cell(chatid, tag):
    m = json.load(open("marathons_list.json", "r"))
    abc = get_user_cell(chatid)
    if abc:
        try:
            return m[chatid][tag]
        except KeyError:
            return False
    else:
        return abc
def set_tag_cell(chatid, tag, value):
    m = json.load(open("marathons_list.json", "r"))
    abc = get_user_cell(chatid)
    if abc:
        try:
            m[chatid][tag] = value
            json.dump(m, open("marathons_list.json", "w"))
        except KeyError:
            return False
    else:
        return abc