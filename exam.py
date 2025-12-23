import random
import psycopg2
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = ''
bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []
userStep = {}
buttons = []


def db():
    con = psycopg2.connect(database='bot', password='dasha', user='postgres')
    return con

def show_hint(*lines):
    return '\n'.join(lines)

def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()
    add_russian = State()
    add_english = State()

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    conn = db()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO users (userId, username) 
        VALUES (%s, %s) 
        ON CONFLICT (userId) DO NOTHING
    """, (message.chat.id, message.from_user.username or 'user'))
    conn.commit()
    
    cur.execute('SELECT english_word, russian_word FROM words ORDER BY RANDOM() LIMIT 1')
    word_pair = cur.fetchone()
    
    if word_pair:
        target_word = word_pair[0]
        translate = word_pair[1]
    else:
        target_word = 'apple'
        translate = 'яблоко'
    
    cur.close()
    conn.close()
    
    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        welcome_text = """Привет 👋
Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе."""
        bot.send_message(cid, welcome_text)
    
    markup = types.ReplyKeyboardMarkup(row_width=2)

    global buttons
    buttons = []
    
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT english_word FROM words 
        WHERE english_word != %s 
        ORDER BY RANDOM() 
        LIMIT 3
    """, (target_word,))
    
    others = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])
    
    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    conn = db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT w.wordId, w.russian_word, w.english_word
        FROM words w
        JOIN "userWords" uw ON w.wordId = uw.word_id
        WHERE uw.user_id = %s
    """, (message.chat.id,))
    
    words = cur.fetchall()
    cur.close()
    conn.close()
    
    if not words:
        bot.send_message(message.chat.id, "У вас нет слов для удаления.")
        create_cards(message)
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=1)
    for word_id, russian, english in words:
        btn = types.KeyboardButton(f"{word_id}: {russian} - {english}")
        markup.add(btn)
    
    back_btn = types.KeyboardButton("Отмена")
    markup.add(back_btn)
    
    bot.send_message(message.chat.id, "Выберите слово для удаления:", reply_markup=markup)
    bot.register_next_step_handler(message, process_delete_word)

def process_delete_word(message):
    """Обработать удаление слова"""
    if message.text == "Отмена":
        create_cards(message)
        return
    
    try:
        word_id = int(message.text.split(":")[0].strip())
    except:
        bot.send_message(message.chat.id, "Ошибка выбора слова")
        create_cards(message)
        return
    
    conn = db()
    cur = conn.cursor()
    
    cur.execute("""
        DELETE FROM "userWords"
        WHERE user_id = %s AND word_id = %s
    """, (message.chat.id, word_id))
    
    conn.commit()
    cur.close()
    conn.close()
    
    bot.send_message(message.chat.id, "✅ Слово удалено!")
    create_cards(message)

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    bot.send_message(message.chat.id, "Введите слово на русском:")
    bot.set_state(message.from_user.id, MyStates.add_russian, message.chat.id)

@bot.message_handler(state=MyStates.add_russian)
def get_russian_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['new_russian'] = message.text
    
    bot.send_message(message.chat.id, "Введите перевод на английском:")
    bot.set_state(message.from_user.id, MyStates.add_english, message.chat.id)

@bot.message_handler(state=MyStates.add_english)
def get_english_word_and_save(message):
    english_word = message.text
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        russian_word = data['new_russian']
    
    conn = db()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO words (english_word, russian_word) 
            VALUES (%s, %s) 
            RETURNING wordId
        """, (english_word, russian_word))
        
        word_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO "userWords" (user_id, word_id, added_at) 
            VALUES (%s, %s, CURRENT_DATE)
        """, (message.chat.id, word_id))
        
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Слово '{russian_word} - {english_word}' добавлено!")
        
    except Exception as e:
        conn.rollback()
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")
    
    finally:
        cur.close()
        conn.close()
    
    bot.delete_state(message.from_user.id, message.chat.id)
    create_cards(message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        
        markup = types.ReplyKeyboardMarkup(row_width=2)
        current_buttons = []
        
        if text == target_word:
            hint = show_target(data)
            hint_text = ["Отлично!❤", hint]
            
            current_buttons.append(types.KeyboardButton(target_word))
            for word in data['other_words']:
                current_buttons.append(types.KeyboardButton(word))
            
            random.shuffle(current_buttons)
            
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            current_buttons.extend([next_btn, add_word_btn, delete_word_btn])
            
            hint = show_hint(*hint_text)
        else:
            current_buttons.append(types.KeyboardButton(target_word))
            for word in data['other_words']:
                current_buttons.append(types.KeyboardButton(word))
            
            random.shuffle(current_buttons)
            
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            current_buttons.extend([next_btn, add_word_btn, delete_word_btn])
            
            hint = show_hint("Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
        
        markup.add(*current_buttons)
        
    bot.send_message(message.chat.id, hint, reply_markup=markup)

bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)
