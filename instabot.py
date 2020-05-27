import telebot,config, admin_data, user_data, getminfo
bot = telebot.TeleBot(config.token, threaded=False)


def reset(m):
    bot.send_message(m.chat.id, "Начнём по-новой. Что нужно сделать?",reply_markup = config.keyboard)
    admin_data.set_state(m.chat.id, config.AdminStates.S_ENTER_TODO.value)
    admin_data.set_tag(str(m.chat.id), 'no tag')
    print(admin_data.get_current_state(m.chat.id))


@bot.message_handler(commands=['start'])
def start(m):
    print(admin_data.get_current_state(m.chat.id))
    bot.send_message(m.chat.id, 'Привет, что нужно сделать?', reply_markup = config.keyboard)
    admin_data.set_state(m.chat.id, config.AdminStates.S_ENTER_TODO.value)
    admin_data.set_tag(str(m.chat.id), 'no tag')
    print(admin_data.get_current_state(m.chat.id))
    print(m.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        chatid = str(call.message.chat.id)
        if call.data == "old":
            bot.send_message(chatid, "Пожалуйста, введите название(тег) марафона в который надо внести изменения следующим сообщением: ")
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_OLD.value)
        if call.data == "new":
            bot.send_message(chatid, "Пожалуйста, введите название(тег) нового марафона следующим сообщением: ")
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_NEWM.value)
        if call.data == "new_follow":
            bot.send_message(chatid, "Пожалуйста, введите список подписок с символом @ перед названием аккаунта следующим сообщением: ")
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_FOLLOWLIST.value)
        if call.data == 'bonus':
            bot.send_message(chatid, "Выберите формат бонуса:", reply_markup = config.bonus_types)
        if call.data == 'text':
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_BONUSTEXT.value)
            bot.send_message(chatid, "Пожалуйста, введите новый текст бонуса следующим сообщением: ")
        if call.data == 'document':
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_BONUSDOC.value)
            bot.send_message(chatid, "Пожалуйста, отправьте бонусный документ следующим сообщением: ")
        if call.data == 'photo':
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_BONUSPIC.value)
            bot.send_message(chatid, "Пожалуйста, отправьте бонусное изображение следующим сообщением: ")
        if call.data == 'reset':
            reset(call.message)
        if call.data == 'show':
            admin_data.set_state(chatid, config.AdminStates.S_ENTER_SHOW.value)
            bot.send_message(chatid, "Пожалуйста, введите тег марафона для которого нужно узнать информацию следующим сообщением: ")


@bot.message_handler(func=lambda message: admin_data.get_current_state(message.chat.id) == config.AdminStates.S_ENTER_NEWM.value)
def create_new_marathon(m):
    chatid, tag = str(m.chat.id), m.text.strip()
    abc = getminfo.get_user_cell(chatid)
    if not abc:
        getminfo.set_user_cell(chatid, {tag:{'bonus':{'text':'бонус не задан', 'pic':'нет изображения', 'doc':'нет документа'}, 'followlist':'список подписок пуст'}})
    else:
        getminfo.set_tag_cell(chatid,tag,{'bonus':{'text':'бонус не задан', 'pic':'нет изображения', 'doc':'нет документа'}, 'followlist':'список подписок пуст'})
    admin_data.set_tag(chatid, tag)
    bot.send_message(chatid, "Новый марафон с тегом «{}» успешно создан. Что нужно добавить/изменить?".format(tag), reply_markup = config.new_key)

@bot.message_handler(func=lambda message: admin_data.get_current_state(message.chat.id) == config.AdminStates.S_ENTER_OLD.value)
def change_old_marathon(m):
    chatid, tag = str(m.chat.id), m.text.strip()
    if getminfo.tag_cell(chatid, tag):
        admin_data.set_tag(chatid, tag)
        bot.send_message(chatid, "Что нужно изменить для марафона с тегом «{}» ?".format(tag), reply_markup = config.change_key)
    else:
        bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")
@bot.message_handler(func=lambda message: admin_data.get_current_state(message.chat.id) == config.AdminStates.S_ENTER_FOLLOWLIST.value)
def follow(m):
    chatid, array = str(m.chat.id), [i.strip() for i in m.text.split('@') if i !='']
    tag = admin_data.get_current_tag(chatid)
    abc= getminfo.tag_cell(chatid, tag)
    if abc:
        abc['followlist'] = array
        getminfo.set_tag_cell(chatid, tag, abc)
        bot.send_message(chatid, "Список подписок для марафона с тегом «{}» успешно обновлен. Всего подписок - {}. Что нужно сделать дальше?".format(tag,len(array)), reply_markup = config.after_follow_key)
    else:
        bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")
@bot.message_handler(func=lambda message: admin_data.get_current_state(message.chat.id) == config.AdminStates.S_ENTER_BONUSTEXT.value)
def bonustext(m):
    chatid = str(m.chat.id)
    tag = admin_data.get_current_tag(chatid)
    abc = getminfo.tag_cell(chatid, tag)
    if abc:
        abc['bonus']['text'] = m.text.strip()
        bot.send_message(chatid, "Бонусный текст для марафона с тегом «{}» успешно обновлен. Значение текста - !{}! Что нужно сделать дальше?".format(tag,m.text), reply_markup = config.after_follow_key)
        getminfo.set_tag_cell(chatid, tag, abc)
    else:
        bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")

@bot.message_handler(content_types=["photo"])
def bonuspic(m):
    if admin_data.get_current_state(m.chat.id) == config.AdminStates.S_ENTER_BONUSPIC.value:
        print('picpic')
        chatid = str(m.chat.id)
        tag = admin_data.get_current_tag(chatid)
        file = m.photo[len(m.photo)-1].file_id
        abc = getminfo.tag_cell(chatid, tag)
        if abc:
            print(abc['bonus'])
            abc['bonus']['pic'] = file
            getminfo.set_tag_cell(chatid, tag, abc)
            bot.send_message(chatid, "Бонусное изображение для марафона с тегом «{}» успешно обновлено. Что нужно сделать дальше?".format(tag), reply_markup = config.after_file_key)
        else:
            bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")
    else:
        bot.send_message(chatid, "Ошибка! Выберите что мне сделать, нажав кнопку.")
        reset(m)

@bot.message_handler(content_types=["document"])
def bonusdoc(m):
    if admin_data.get_current_state(m.chat.id) == config.AdminStates.S_ENTER_BONUSDOC.value:
        print('docdoc')
        chatid = str(m.chat.id)
        tag = admin_data.get_current_tag(chatid)
        file = m.document.file_id
        print(file)
        abc = getminfo.tag_cell(chatid, tag)
        if abc:
            print(abc['bonus'])
            abc['bonus']['doc'] = file
            getminfo.set_tag_cell(chatid, tag, abc)
            bot.send_message(chatid, "Бонусный документ для марафона с тегом «{}» успешно обновлен. Что нужно сделать дальше?".format(tag), reply_markup = config.after_file_key)
        else:
            bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")
    else:
        bot.send_message(chatid, "Ошибка! Выберите что мне сделать, нажав кнопку.")
        reset(m)
@bot.message_handler(func=lambda message: admin_data.get_current_state(message.chat.id) == config.AdminStates.S_ENTER_SHOW.value)
def show(m):
    chatid = str(m.chat.id)
    tag = m.text.strip()
    admin_data.set_tag(chatid, tag)
    abc = getminfo.tag_cell(chatid, tag)
    if abc:
        bonus, follow, pic, doc = abc['bonus']["text"], abc['followlist'], abc['bonus']["pic"], abc['bonus']["doc"]
        if follow != 'список подписок пуст':
            if len(follow) > 5:
                follow = follow[:3]
            follow = '\n'.join(follow)
        elif pic != 'нет изображения':
            pic = 'есть изображение'
        elif doc != 'нет документа':
            pic = 'есть документ'
        bot.send_message(chatid, "Информация о марафоне «{}»\nБонус: {}\n{}\n{}\nПервые строки из списка подписок:\n{} ".format(tag, bonus, pic, doc, follow), reply_markup = config.after_follow_key)
    else:
        bot.send_message(chatid, "Ошибка! Марафона с таким тегом не существует. Введите еще раз.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
