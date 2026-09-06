import os, sqlite3, telebot, asyncio
from telebot import types
from flask import Flask, request
from datetime import datetime

TOKEN = os.environ.get('8909899304:AAHr3aV0DyYUHCtNaScAfFl_feP-Jt1I26w')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
ADMIN_ID = 7135825858 

CHANNEL = "follewrs_free_10"
GROUP = "criminal_store_10"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
user_state = {}

# ===== 6 LINGUE COMPLETE =====
LANG = {
    'it': {
        'welcome':"Benvenuto! +550 punti 🎉", 'menu':"Menu principale",
        'profile':"👤 Profilo", 'points':"⭐ Punti", 'buy':"💰 Compra Punti",
        'invite':"👥 Invita", 'bonus':"🎁 Bonus", 'promote':"📢 Promuovi",
        'transfer':"🔄 Trasferisci", 'settings':"⚙️ Impostazioni", 'lang':"🌐 Lingua",
        'earn':"⭐ Guadagna", 'rank':"📊 Classifica", 'force_sub':"Devi iscriverti prima:",
        'your_points':"Il tuo saldo: ⭐ ", 'bonus_ok':"+250 punti! Torna domani",
        'bonus_no':"Hai già preso il bonus oggi", 'select_lang':"Scegli la lingua:",
        'link_sent':"Il tuo link di invito:", 'points_added':"✅ Punti aggiunti!",
        'store':"🛒 Store", 'no_points':"Punti insufficienti", 'promo_cost':"Costo: 50 punti a persona. Min 10",
        'send_link':"Invia il link del canale da promuovere:", 'send_amount':"Quante persone?"
    },
    'en': {
        'welcome':"Welcome! +550 points 🎉", 'menu':"Main Menu",
        'profile':"👤 Profile", 'points':"⭐ Points", 'buy':"💰 Buy Points",
        'invite':"👥 Invite", 'bonus':"🎁 Daily Bonus", 'promote':"📢 Promote",
        'transfer':"🔄 Transfer", 'settings':"⚙️ Settings", 'lang':"🌐 Language",
        'earn':"⭐ Earn", 'rank':"📊 Leaderboard", 'force_sub':"You must subscribe first:",
        'your_points':"Your balance: ⭐ ", 'bonus_ok':"+250 points! Come back tomorrow",
        'bonus_no':"You already took bonus today", 'select_lang':"Choose language:",
        'link_sent':"Your invite link:", 'points_added':"✅ Points added!",
        'store':"🛒 Store", 'no_points':"Not enough points", 'promo_cost':"Cost: 50 points per person. Min 10",
        'send_link':"Send the channel link to promote:", 'send_amount':"How many people?"
    },
    'fr': {
        'welcome':"Bienvenue! +550 points 🎉", 'menu':"Menu principal",
        'profile':"👤 Profil", 'points':"⭐ Points", 'buy':"💰 Acheter Points",
        'invite':"👥 Inviter", 'bonus':"🎁 Bonus", 'promote':"📢 Promouvoir",
        'transfer':"🔄 Transférer", 'settings':"⚙️ Paramètres", 'lang':"🌐 Langue",
        'earn':"⭐ Gagner", 'rank':"📊 Classement", 'force_sub':"Vous devez vous abonner d'abord:",
        'your_points':"Votre solde: ⭐ ", 'bonus_ok':"+250 points! Revenez demain",
        'bonus_no':"Bonus déjà pris aujourd'hui", 'select_lang':"Choisissez la langue:",
        'link_sent':"Votre lien d'invitation:", 'points_added':"✅ Points ajoutés!",
        'store':"🛒 Boutique", 'no_points':"Pas assez de points", 'promo_cost':"Coût: 50 points par personne. Min 10",
        'send_link':"Envoyez le lien de la chaîne à promouvoir:", 'send_amount':"Combien de personnes?"
    },
    'ar': {
        'welcome':"مرحبا! +550 نقطة 🎉", 'menu':"القائمة الرئيسية",
        'profile':"👤 الملف", 'points':"⭐ النقاط", 'buy':"💰 شراء النقاط",
        'invite':"👥 دعوة", 'bonus':"🎁 مكافأة", 'promote':"📢 ترويج",
        'transfer':"🔄 تحويل", 'settings':"⚙️ الاعدادات", 'lang':"🌐 اللغة",
        'earn':"⭐ اكسب", 'rank':"📊 الترتيب", 'force_sub':"يجب الاشتراك اولا:",
        'your_points':"رصيدك: ⭐ ", 'bonus_ok':"+250 نقطة! ارجع غدا",
        'bonus_no':"اخذت المكافأة اليوم", 'select_lang':"اختر اللغة:",
        'link_sent':"رابط الدعوة الخاص بك:", 'points_added':"✅ تم اضافة النقاط!",
        'store':"🛒 المتجر", 'no_points':"نقاط غير كافية", 'promo_cost':"السعر: 50 نقطة لكل شخص. اقل شي 10",
        'send_link':"ارسل رابط القناة للترويج:", 'send_amount':"كم شخص؟"
    },
    'ma': {
        'welcome':"مرحبا بيك! +550 نقطة 🎉", 'menu':"القائمة الرئيسية",
        'profile':"👤 البروفايل", 'points':"⭐ النقط", 'buy':"💰 شري النقط",
        'invite':"👥 عيط لصحابك", 'bonus':"🎁 المكافأة اليومية", 'promote':"📢 طلع القناة",
        'transfer':"🔄 صيفط النقط", 'settings':"⚙️ الاعدادات", 'lang':"🌐 اللغة",
        'earn':"⭐ ربح النقط", 'rank':"📊 الترتيب", 'force_sub':"خاصك تدخل القناة والكروب الاول:",
        'your_points':"عندك: ⭐ ", 'bonus_ok':"+250 نقطة! ارجع غدا",
        'bonus_no':"ديتي المكافأة ديال اليوم", 'select_lang':"ختار اللغة:",
        'link_sent':"الرابط ديالك:", 'points_added':"✅ تزادو النقط!",
        'store':"🛒 المتجر", 'no_points':"معندكش النقط كافيين", 'promo_cost':"الثمن: 50 نقطة لكل واحد. اقل حاجة 10",
        'send_link':"صيفط ليان القناة:", 'send_amount':"شحال من واحد؟"
    },
    'ru': {
        'welcome':"Добро пожаловать! +550 баллов 🎉", 'menu':"Главное меню",
        'profile':"👤 Профиль", 'points':"⭐ Баллы", 'buy':"💰 Купить баллы",
        'invite':"👥 Пригласить", 'bonus':"🎁 Бонус", 'promote':"📢 Продвижение",
        'transfer':"🔄 Перевести", 'settings':"⚙️ Настройки", 'lang':"🌐 Язык",
        'earn':"⭐ Заработать", 'rank':"📊 Рейтинг", 'force_sub':"Сначала подпишитесь:",
        'your_points':"Ваш баланс: ⭐ ", 'bonus_ok':"+250 баллов! Возвращайтесь завтра",
        'bonus_no':"Вы уже получили бонус сегодня", 'select_lang':"Выберите язык:",
        'link_sent':"Ваша реферальная ссылка:", 'points_added':"✅ Баллы добавлены!",
        'store':"🛒 Магазин", 'no_points':"Недостаточно баллов", 'promo_cost':"Цена: 50 баллов за человека. Мин 10",
        'send_link':"Отправьте ссылку канала для продвижения:", 'send_amount':"Сколько человек?"
    }
}

STAR_PACKAGES = {
    1: {'points': 1000, 'stars': 50},
    2: {'points': 5500, 'stars': 250},
    3: {'points': 12000, 'stars': 500}
}

# ===== DATABASE =====
def init_db():
    conn = sqlite3.connect('database.db'); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, name TEXT, surname TEXT,
                  reg_date TEXT, lang TEXT, points INTEGER, invites INTEGER, invited_by INTEGER,
                  level INTEGER, badge TEXT, last_bonus TEXT, hidden INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS promos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER, link TEXT,
                  people INTEGER, cost INTEGER, status TEXT)''')
    conn.commit(); conn.close()

def db(query, params=()): conn = sqlite3.connect('database.db'); c=conn.cursor(); c.execute(query,params); conn.commit(); conn.close()
def get_user(uid): conn = sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT * FROM users WHERE id=?",(uid,)); u=c.fetchone(); conn.close(); return u
def get_lang(uid): u=get_user(uid); return u[5] if u else 'ma'
def add_user(uid,username,name,surname,invited_by=None):
    db("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
       (uid,username,name,surname,str(datetime.now().date()),'ma',550,0,invited_by,1,'🌱','',0))
    if invited_by: db("UPDATE users SET points=points+1000, invites=invites+1 WHERE id=?",(invited_by,)); db("UPDATE users SET points=points+300 WHERE id=?",(uid,))

# ===== CHECK SUB =====
def check_sub(uid):
    try: ch=bot.get_chat_member(f"@{CHANNEL}",uid).status; gr=bot.get_chat_member(f"@{GROUP}",uid).status
    except: return False
    return ch in ['member','admin','creator'] and gr in ['member','admin','creator']

def force_sub_menu(lang):
    m=types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("📢 Canale",url=f"https://t.me/{CHANNEL}"))
    m.add(types.InlineKeyboardButton("👥 Gruppo",url=f"https://t.me/{GROUP}"))
    m.add(types.InlineKeyboardButton("✅ Ho completato",callback_data="check_sub"))
    return m

# ===== MENUS =====
def main_menu(lang):
    t=LANG[lang]; m=types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(t['profile'],t['points']); m.row(t['promote'],t['earn'])
    m.row(t['invite'],t['transfer']); m.row(t['buy'],t['bonus'])
    m.row(t['rank'],t['lang']); return m

def lang_menu():
    m=types.InlineKeyboardMarkup()
    m.row(types.InlineKeyboardButton("🇮🇹 Italiano",callback_data="lang_it"),
          types.InlineKeyboardButton("🇬🇧 English",callback_data="lang_en"))
    m.row(types.InlineKeyboardButton("🇫🇷 Français",callback_data="lang_fr"),
          types.InlineKeyboardButton("🇷🇺 Русский",callback_data="lang_ru"))
    m.row(types.InlineKeyboardButton("🇸🇦 العربية",callback_data="lang_ar"),
          types.InlineKeyboardButton("🇲🇦 الدارجة",callback_data="lang_ma"))
    return m

# ===== SET COMANDI =====
async def set_bot_commands():
    for lang in LANG:
        cmds = [
            types.BotCommand("start", LANG[lang]['welcome'].split('!')[0]),
            types.BotCommand("admin", "Admin Panel" if lang!='ma' else "لوحة الادمين"),
            types.BotCommand("lingua", LANG[lang]['lang'])
        ]
        await bot.set_my_commands(cmds, language_code=lang)

async def set_user_commands(user_id, lang):
    cmds = [
        types.BotCommand("start", LANG[lang]['welcome'].split('!')[0]),
        types.BotCommand("admin", "Admin Panel"),
        types.BotCommand("lingua", LANG[lang]['lang'])
    ]
    await bot.set_my_commands(cmds, scope=types.BotCommandScopeChat(user_id))

# ===== HANDLERS =====
@bot.message_handler(commands=['start'])
def start(msg):
    inv = int(msg.text.split()[1]) if len(msg.text.split())>1 else None
    if not get_user(msg.from_user.id):
        add_user(msg.from_user.id,msg.from_user.username,msg.from_user.first_name,msg.from_user.last_name,inv)
        bot.send_message(msg.chat.id, LANG['ma']['welcome'])
        bot.send_message(msg.chat.id, LANG['ma']['select_lang'], reply_markup=lang_menu())
        asyncio.run(set_user_commands(msg.from_user.id, 'ma'))
    else:
        lang=get_lang(msg.from_user.id)
        if check_sub(msg.from_user.id):
            bot.send_message(msg.chat.id, LANG[lang]['menu'], reply_markup=main_menu(lang))
        else:
            bot.send_message(msg.chat.id, LANG[lang]['force_sub'], reply_markup=force_sub_menu(lang))

@bot.callback_query_handler(func=lambda c: c.data=="check_sub")
def check_sub_btn(c):
    lang=get_lang(c.from_user.id)
    if check_sub(c.from_user.id):
        bot.edit_message_text("✅ OK",c.message.chat.id,c.message_id)
        bot.send_message(c.message.chat.id, LANG[lang]['menu'], reply_markup=main_menu(lang))
    else: bot.answer_callback_query(c.id,"Non sei iscritto!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def set_lang(c):
    lang=c.data.split('_')[1]
    db("UPDATE users SET lang=? WHERE id=?", (lang,c.from_user.id))
    asyncio.run(set_user_commands(c.from_user.id, lang))
    bot.edit_message_text(LANG[lang]['menu'],c.message.chat.id,c.message_id)
    bot.send_message(c.message.chat.id, LANG[lang]['menu'], reply_markup=main_menu(lang))

@bot.message_handler(commands=['lingua'])
def cmd_lang(msg): lang=get_lang(msg.from_user.id); bot.send_message(msg.chat.id, LANG[lang]['select_lang'], reply_markup=lang_menu())

@bot.message_handler(func=lambda m: any(m.text == LANG[x]['profile'] for x in LANG))
def profilo(m): lang=get_lang(m.from_user.id); u=get_user(m.from_user.id); bot.send_message(m.chat.id,f"{LANG[lang]['profile']}\nID:`{u[0]}`\n{LANG[lang]['your_points']}{u[6]}",parse_mode='Markdown')

@bot.message_handler(func=lambda m: any(m.text == LANG[x]['bonus'] for x in LANG))
def bonus(m): lang=get_lang(m.from_user.id); u=get_user(m.from_user.id); oggi=str(datetime.now().date());
if u[11]!=oggi: db("UPDATE users SET points=points+250, last_bonus=? WHERE id=?",(oggi,m.from_user.id)); bot.send_message(m.chat.id,LANG[lang]['bonus_ok'])
else: bot.send_message(m.chat.id,LANG[lang]['bonus_no'])

@bot.message_handler(func=lambda m: any(m.text == LANG[x]['invite'] for x in LANG))
def invite(m): lang=get_lang(m.from_user.id); bot.send_message(m.chat.id,f"{LANG[lang]['link_sent']}\nhttps://t.me/{bot.get_me().username}?start={m.from_user.id}")

@bot.message_handler(func=lambda m: any(m.text == LANG[x]['buy'] for x in LANG))
def store(m): lang=get_lang(m.from_user.id); markup = types.InlineKeyboardMarkup();
for id,p in STAR_PACKAGES.items(): markup.add(types.InlineKeyboardButton(f"{p['points']} - {p['stars']} ⭐", callback_data=f"buy_{id}"))
bot.send_message(m.chat.id,LANG[lang]['store'],reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy(c): pack_id = int(c.data.split('_')[1]); pack = STAR_PACKAGES[pack_id]; prices = [types.LabeledPrice(label=f"{pack['points']} points", amount=pack['stars'])]; bot.send_invoice(c.from_user.id,title=f"{pack['points']} Points",description="Buy points",invoice_payload=f"points_{pack_id}_{c.from_user.id}",provider_token="",currency="XTR",prices=prices)

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q): bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment(msg): pack_id = int(msg.successful_payment.invoice_payload.split('_')[1]); pack = STAR_PACKAGES[pack_id]; db("UPDATE users SET points=points+? WHERE id=?", (pack['points'], msg.from_user.id)); lang=get_lang(msg.from_user.id); bot.send_message(msg.chat.id, LANG[lang]['points_added'])

@bot.message_handler(func=lambda m: any(m.text == LANG[x]['promote'] for x in LANG))
def p1(m): lang=get_lang(m.from_user.id); user_state[m.from_user.id]='p_link'; bot.send_message(m.chat.id,LANG[lang]['send_link']+"\n"+LANG[lang]['promo_cost'])
@bot.message_handler(func=lambda m: user_state.get(m.from_user.id)=='p_link')
def p2(m): lang=get_lang(m.from_user.id); user_state[m.from_user.id]={'s':'p_num','link':m.text}; bot.send_message(m.chat.id,LANG[lang]['send_amount'])
@bot.message_handler(func=lambda m: isinstance(user_state.get(m.from_user.id),dict))
def p3(m): lang=get_lang(m.from_user.id); num=int(m.text); cost=num*50; u=get_user(m.from_user.id);
if num<10 or u[6]<cost: bot.send_message(m.chat.id,LANG[lang]['no_points']); return
db("UPDATE users SET points=points-? WHERE id=?",(cost,m.from_user.id)); db("INSERT INTO promos VALUES (NULL,?,?,?,?,?)",(m.from_user.id,user_state[m.from_user.id]['link'],num,cost,'pending')); bot.send_message(m.chat.id,"✅ Inviata",reply_markup=main_menu(lang)); bot.send_message(ADMIN_ID,f"Nuova promo: {user_state[m.from_user.id]['link']}"); user_state[m.from_user.id]=None

@bot.message_handler(commands=['admin'])
def admin(m):
    if m.from_user.id==ADMIN_ID: bot.send_message(m.chat.id,"👑 Admin Panel")

# ===== WEBHOOK =====
@app.route('/',methods=['POST'])
def webhook(): bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]); return "ok",200
@app.route('/'): return "ok",200

if __name__=="__main__":
    init_db()
    asyncio.run(set_bot_commands())
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/")
    app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))