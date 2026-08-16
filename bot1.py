from pyrogram import Client, filters, enums
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton as _TelegramInlineKeyboardButton

# ============================================================
# REAL Telegram colored buttons - requires PyroTGFork 2.2.24+
# ============================================================
try:
    from pyrogram.enums import ButtonStyle
except ImportError as exc:
    raise RuntimeError(
        "این نسخه برای دکمه‌های رنگی واقعی به PyroTGFork نیاز دارد. "
        "ابتدا اجرا کنید: pip uninstall -y pyrogram && pip install -U pyrotgfork==2.2.24"
    ) from exc

try:
    import inspect as _inspect
    if "style" not in _inspect.signature(_TelegramInlineKeyboardButton).parameters:
        raise RuntimeError(
            "نسخه Pyrogram شما style واقعی تلگرام را پشتیبانی نمی‌کند. "
            "اجرا کنید: pip uninstall -y pyrogram && pip install -U pyrotgfork==2.2.24"
        )
except (TypeError, ValueError):
    pass

PREMIUM_EMOJI_IDS = {}

def _button_style(text, callback_data=None, url=None, explicit=None):
    if explicit is not None:
        return explicit
    t = str(text or "").lower()
    d = str(callback_data or "").lower()
    danger_words = ("لغو", "انصراف", "حذف", "رد", "توقف", "خاموش", "خروج", "بازگشت", "پاک", "danger", "cancel", "delete", "stop", "reject")
    success_words = ("تایید", "تأیید", "فعال", "ارسال", "پیوستن", "روشن", "شارژ", "خرید", "ثبت", "success", "approve", "join", "start", "send")
    danger_data = ("cancel", "delete", "stop", "reject", "back")
    success_data = ("approve", "join", "send", "start", "on", "increase", "buy")
    if any(x in t for x in danger_words) or any(x in d for x in danger_data):
        return ButtonStyle.DANGER
    if any(x in t for x in success_words) or any(x in d for x in success_data):
        return ButtonStyle.SUCCESS
    return ButtonStyle.PRIMARY

def InlineKeyboardButton(text, callback_data=None, url=None, style=None, icon_custom_emoji_id=None, **kwargs):
    params = dict(kwargs)
    if callback_data is not None:
        params["callback_data"] = callback_data
    if url is not None:
        params["url"] = url
    params["style"] = _button_style(text, callback_data, url, style)
    emoji_id = icon_custom_emoji_id or PREMIUM_EMOJI_IDS.get(str(callback_data))
    if emoji_id:
        params["icon_custom_emoji_id"] = str(emoji_id)
    return _TelegramInlineKeyboardButton(text=text, **params)

from pyrogram.errors import SessionPasswordNeeded 
import json, os, asyncio, subprocess, sys, time, threading, html, random, signal

# ============================================================
# 🔐 متغیرهای محیطی - برای Railway
# ============================================================
import os as _os

BOT_TOKEN = _os.environ.get("BOT_TOKEN", "8716828809:AAFMccz2mLWjRhBg1svndKjLRbqXiv5M9Zk")
API_ID = int(_os.environ.get("API_ID", 28758742))
API_HASH = _os.environ.get("API_HASH", "9cbae03d2561bf928db520fac44a2bfb")
ADMIN_ID = [7983573730, 8881352692]
ADMIN_USERNAME = "RzStack"
BOT_NAME = "سلف ساز | Iran Self"
SELF_ACTIVATION_COST = 30
SELF_HOURLY_COST = 2
DIAMOND_TO_TOMAN = 15
BET_PHOTO_SETTING = "bet_photo_id"

os.makedirs("sessions", exist_ok=True)

TAX_PERCENT = 10
TAX_MIN_AMOUNT = 2

FORCE_CHANNELS = [
    "Z_CODME",
    "IranSelfux",
    "SELF_lRAN"
]

COIN_RATE = 1000
TOMAN_PER_COIN = DIAMOND_TO_TOMAN

card_info = {
    "card_number": "5022-2915-2648-8786",
    "card_owner": "رضا مرای",
    "bank_name": "پاسارگاد"
}

bot = Client("bo7whe8bt", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

user_temp_codes = {}
user_phone_digits = {}
active_clients = {}
ttt_games = {}

class JSONDatabase:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "settings" not in data:
                        data["settings"] = {
                            "coin_rate": COIN_RATE,
                            "toman_per_coin": TOMAN_PER_COIN,
                            "admin_id": ADMIN_ID,
                            "tax_percent": TAX_PERCENT,
                            "tax_min_amount": TAX_MIN_AMOUNT,
                            "transfer_enabled": True,
                            "self_activation_cost": SELF_ACTIVATION_COST,
                            "self_hourly_cost": SELF_HOURLY_COST,
                            "diamond_to_toman": DIAMOND_TO_TOMAN,
                            "bet_photo_id": None
                        }
                        self.save_data(data)
                    return data
            else:
                initial_data = {
                    "users": {}, 
                    "processes": {}, 
                    "temp_data": {}, 
                    "credits": {}, 
                    "timers": {},
                    "verifications": {},
                    "payments": {},
                    "group_bets": {},
                    "settings": {
                        "coin_rate": COIN_RATE,
                        "toman_per_coin": TOMAN_PER_COIN,
                        "admin_id": ADMIN_ID,
                        "tax_percent": TAX_PERCENT,
                        "tax_min_amount": TAX_MIN_AMOUNT,
                        "transfer_enabled": True,
                        "self_activation_cost": SELF_ACTIVATION_COST,
                        "self_hourly_cost": SELF_HOURLY_COST,
                        "diamond_to_toman": DIAMOND_TO_TOMAN,
                        "bet_photo_id": None
                    }
                }
                self.save_data(initial_data)
                return initial_data
        except Exception as e:
            return {
                "users": {}, "processes": {}, "temp_data": {}, 
                "credits": {}, "timers": {}, "verifications": {}, 
                "payments": {}, "group_bets": {},
                "settings": {
                    "coin_rate": COIN_RATE,
                    "toman_per_coin": TOMAN_PER_COIN,
                    "admin_id": ADMIN_ID,
                    "tax_percent": TAX_PERCENT,
                    "tax_min_amount": TAX_MIN_AMOUNT,
                    "transfer_enabled": True
                }
            }

    def save_data(self, data=None):
        try:
            if data: 
                self.data = data
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def get_welcome_photo(self):
        return self.get("settings", "welcome_photo_id", None)

    def set_welcome_photo(self, photo_id):
        return self.set("settings", "welcome_photo_id", photo_id)

    def delete_welcome_photo(self):
        return self.delete("settings", "welcome_photo_id")
    
    def get(self, category, key, default=None):
        try:
            return self.data.get(category, {}).get(str(key), default)
        except:
            return default
    
    def set(self, category, key, value):
        try:
            if category not in self.data: 
                self.data[category] = {}
            self.data[category][str(key)] = value
            return self.save_data()
        except Exception as e:
            return False
    
    def delete(self, category, key):
        try:
            if category in self.data and str(key) in self.data[category]:
                del self.data[category][str(key)]
                return self.save_data()
            return False
        except Exception as e:
            return False  
    
    def get_all(self, category):
        try:
            return self.data.get(category, {})
        except:
            return {}
    
    def get_pending_verifications(self):
        try:
            verifications = self.data.get("verifications", {})
            return {k: v for k, v in verifications.items() if v.get('status') == 'pending'}
        except:
            return {}
    
    def get_pending_payments(self):
        try:
            payments = self.data.get("payments", {})
            return {k: v for k, v in payments.items() if v.get('status') == 'pending'}
        except:
            return {}
    
    def get_verified_users(self):
        try:
            users = self.data.get("users", {})
            return {k: v for k, v in users.items() if v.get('verified')}
        except:
            return {}
    
    def get_rejected_users(self):
        try:
            users = self.data.get("users", {})
            return {k: v for k, v in users.items() if v.get('rejected')}
        except:
            return {}
    
    def set_transfer_status(self, enabled):
        if "settings" not in self.data:
            self.data["settings"] = {}
        self.data["settings"]["transfer_enabled"] = enabled
        return self.save_data()
    
    def get_transfer_status(self):
        settings = self.data.get("settings", {})
        return settings.get("transfer_enabled", True)

db = JSONDatabase()

_settings_defaults = {
    "self_activation_cost": SELF_ACTIVATION_COST,
    "self_hourly_cost": SELF_HOURLY_COST,
    "diamond_to_toman": DIAMOND_TO_TOMAN,
    "bet_photo_id": None,
    "bot_name": BOT_NAME,
    "owner_username": ADMIN_USERNAME,
}
for _key, _value in _settings_defaults.items():
    if db.get("settings", _key, None) is None:
        db.set("settings", _key, _value)

user_timers = {}

class UserTimer:
    def __init__(self, user_id, callback):
        self.user_id, self.callback, self.timer, self.is_running = user_id, callback, None, False
    
    def start(self):
        if self.is_running: 
            self.stop()
        self.is_running = True
        self.timer = threading.Timer(3600, self._on_timer)
        self.timer.start()
        db.set("timers", self.user_id, {"start_time": time.time(), "is_running": True})
    
    def stop(self):
        if self.timer: 
            self.timer.cancel()
        self.is_running = False
        db.delete("timers", self.user_id)
    
    def _on_timer(self):
        self.is_running = False
        db.delete("timers", self.user_id)
        self.callback(self.user_id)

FONTS = {
    '0': '𝟬',
    '1': '𝟭',
    '2': '𝟮',
    '3': '𝟯',
    '4': '𝟰',
    '5': '𝟱',
    '6': '𝟲',
    '7': '𝟳',
    '8': '𝟴',
    '9': '𝟵'
}

def is_admin_user(user):
    if not user:
        return False
    username = (getattr(user, "username", None) or "").lstrip("@").lower()
    return getattr(user, "id", None) == ADMIN_ID or username == ADMIN_USERNAME.lower()

def settings_value(key, default):
    return db.get("settings", key, default)

def self_costs():
    return int(settings_value("self_activation_cost", SELF_ACTIVATION_COST)), int(settings_value("self_hourly_cost", SELF_HOURLY_COST))

def main_menu_keyboard(user_id, username=None):
    def ib(text, data=None, url=None, style=None):
        if data and url is not None and style is None and ButtonStyle and url in (ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER):
            style, url = url, None
        kw={"callback_data":data} if data else {"url":url}
        if ButtonStyle and style:
            kw["style"]=style
        return InlineKeyboardButton(text, **kw)
    rows = [
        [ib("🟢 فعال سازی سلف", "login", ButtonStyle.SUCCESS if ButtonStyle else None)],
        [ib("💼 موجودی", "status_credits", ButtonStyle.SUCCESS if ButtonStyle else None),
         ib("💰 شارژ حساب", "increase_balance", ButtonStyle.SUCCESS if ButtonStyle else None)],
        [ib("🎁 خرید گیفت", "gift_store", ButtonStyle.PRIMARY if ButtonStyle else None)],
        [ib("🎮 فروشگاه بازی | دوز آنلاین", "ttt_menu", ButtonStyle.PRIMARY if ButtonStyle else None)],
        [ib("🤖 دستیار هوش مصنوعی", "ai_info", ButtonStyle.PRIMARY if ButtonStyle else None),
         ib("💎 انتقال الماس", "transfer_info", ButtonStyle.PRIMARY if ButtonStyle else None)],
        [ib("🎡 چرخ شانس", "daily_challenge", ButtonStyle.PRIMARY if ButtonStyle else None),
         ib("🏆 لیدربورد", "leaderboard", ButtonStyle.PRIMARY if ButtonStyle else None),
         ib("🎯 چالش روزانه", "daily_challenge", ButtonStyle.PRIMARY if ButtonStyle else None)],
        [ib("👥 زیرمجموعه‌گیری", "referral", ButtonStyle.PRIMARY if ButtonStyle else None),
         ib("👤 حساب کاربری", "status_credits", ButtonStyle.PRIMARY if ButtonStyle else None)],
        [ib("🆘 پشتیبانی", url="https://t.me/RzStack", style=ButtonStyle.DANGER if ButtonStyle else None),
         ib("📣 چنل", url="https://t.me/RzStack", style=ButtonStyle.DANGER if ButtonStyle else None)],
        [ib("❓ سلف چیست؟", "about_self", ButtonStyle.DANGER if ButtonStyle else None)],
    ]
    if is_admin_user(type("U", (), {"id": user_id, "username": username or ""})()):
        rows.append([ib("🛠 پنل مدیریت", "admin_panel", ButtonStyle.DANGER if ButtonStyle else None)])
    return InlineKeyboardMarkup(rows)

def phone_numpad_keyboard(prefix="phone"):
    def b(label, data, style=None):
        if ButtonStyle and style:
            return InlineKeyboardButton(label, callback_data=data, style=style)
        return InlineKeyboardButton(label, callback_data=data)
    return InlineKeyboardMarkup([
        [b("1️⃣", f"{prefix}_1"), b("2️⃣", f"{prefix}_2"), b("3️⃣", f"{prefix}_3")],
        [b("4️⃣", f"{prefix}_4"), b("5️⃣", f"{prefix}_5"), b("6️⃣", f"{prefix}_6")],
        [b("7️⃣", f"{prefix}_7"), b("8️⃣", f"{prefix}_8"), b("9️⃣", f"{prefix}_9")],
        [b("➕", f"{prefix}_plus"), b("0️⃣", f"{prefix}_0"), b("⌫ پاک", f"{prefix}_clear", ButtonStyle.DANGER if ButtonStyle else None)],
        [b("🇮🇷 +98", f"{prefix}_country_98"), b("🌍 +", f"{prefix}_country_custom")],
        [b("✅ تأیید شماره", f"{prefix}_send", ButtonStyle.SUCCESS if ButtonStyle else None)],
        [b("🔙 بازگشت", f"{prefix}_cancel", ButtonStyle.DANGER if ButtonStyle else None)],
    ])

def ttt_keyboard(game_id, board):
    rows=[]
    for r in range(3):
        row=[]
        for c in range(3):
            i=r*3+c
            value=board[i] or "▫️"
            row.append(InlineKeyboardButton(value, callback_data=f"ttt_move_{game_id}_{i}"))
        rows.append(row)
    rows.append([InlineKeyboardButton("❌ خروج از بازی", callback_data=f"ttt_cancel_{game_id}")])
    return InlineKeyboardMarkup(rows)

def ttt_text(game):
    p1 = f'<a href="tg://user?id={game["x_id"]}"><b>{html.escape(game["x_name"])}</b></a>'
    p2 = f'<a href="tg://user?id={game["o_id"]}"><b>{html.escape(game["o_name"])}</b></a>' if game.get("o_id") else "⏳ منتظر حریف"
    if game.get("winner"):
        result = "🏆 برنده: " + (p1 if game["winner"] == "X" else p2)
    elif all(game["board"]):
        result = "🤝 بازی مساوی شد!"
    else:
        turn = p1 if game["turn"] == "X" else p2
        result = f"🎯 نوبت: {turn}  |  {game['turn']}"
    return f"🎮 <b>بازی آنلاین دوز</b>\n\n❌ X: {p1}\n⭕ O: {p2}\n\n{result}\n\nبا دکمه‌های زیر حرکت کنید."

def ttt_winner(board):
    wins=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for a,b,c in wins:
        if board[a] and board[a]==board[b]==board[c]: return board[a]
    if all(board): return "D"
    return None

async def send_main_menu(client, chat_id, user_id, message=None):
    credits=db.get("credits", user_id, 0)
    user_data=db.get("users", user_id, {})
    active=check_selfbot_status(user_id)
    status="🟢 فعال" if active else "🔴 غیرفعال"
    text=(f"<b>{BOT_NAME}</b>\n\n"
          f"🤖 <b>سلف ساز حرفه‌ای ایران</b>\n"
          f"👤 کاربر: <b>{html.escape(user_data.get('first_name','کاربر'))}</b>\n"
          f"💎 موجودی شما: <b>{credits:,}</b> الماس\n"
          f"⚡ وضعیت سلف: {status}\n"
          f"⏱ مصرف سلف: <b>{self_costs()[1]}</b> الماس در ساعت\n\n"
          "👇 یکی از گزینه‌های زیر را انتخاب کنید:")
    kb=main_menu_keyboard(user_id, user_data.get("username", ""))
    photo_id=db.get_welcome_photo()
    if message:
        try:
            if getattr(message, "photo", None):
                await message.edit_caption(caption=text, reply_markup=kb, parse_mode=enums.ParseMode.HTML)
            else:
                await message.edit_text(text, reply_markup=kb, parse_mode=enums.ParseMode.HTML)
            return
        except Exception:
            pass
    if photo_id:
        await client.send_photo(chat_id, photo_id, caption=text, reply_markup=kb, parse_mode=enums.ParseMode.HTML)
    else:
        await client.send_message(chat_id, text, reply_markup=kb, parse_mode=enums.ParseMode.HTML)

def font_convert(text):
    if text is None:
        return ""
    result = ""
    for char in str(text):
        if char.isdigit():
            result += FONTS.get(char, char)
        else:
            result += char
    return result

def create_colored_buttons(join_data, cancel_data):
    if ButtonStyle is None:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ پیوستن به شرط", callback_data=join_data),
                InlineKeyboardButton("⛔ لغو شرط", callback_data=cancel_data)
            ]
        ])
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ پیوستن به شرط",
                callback_data=join_data,
                style=ButtonStyle.SUCCESS
            ),
            InlineKeyboardButton(
                "⛔ لغو شرط",
                callback_data=cancel_data,
                style=ButtonStyle.DANGER
            )
        ]
    ])

async def betting_info_handler(client, message):
    info_text = """
🎲 سیستم شرطبندی گروهی 1v1
📋 قوانین شرطبندی:
1️⃣ در گروه با نوشتن `شرطبندی 100` (یا هر مقدار دیگر) می‌توانید شرط ایجاد کنید
2️⃣ نفر دوم می‌تواند با کلیک روی دکمه «پیوستن به شرط» وارد شود
3️⃣ پس از پیوستن نفر دوم، ۵ ثانیه بعد برنده مشخص می‌شود
4️⃣ برنده تمام مبلغ شرط را دریافت می‌کند
5️⃣ اگر در ۵ دقیقه کسی شرکت نکند، شرط لغو و مبلغ بازگردانده می‌شود

💰 مثال:
- شما: `شرطبندی 500`
- حریف: پیوستن به شرط
- برنده: تمام 1000 الماس را می‌برد (500+500)

"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
    ])
    
    await message.edit_text(info_text, reply_markup=keyboard)

def create_numpad_keyboard(prefix="code"):
    buttons = []
    
    row1 = [
        InlineKeyboardButton("1️⃣", callback_data=f"{prefix}_1"),
        InlineKeyboardButton("2️⃣", callback_data=f"{prefix}_2"),
        InlineKeyboardButton("3️⃣", callback_data=f"{prefix}_3")
    ]
    
    row2 = [
        InlineKeyboardButton("4️⃣", callback_data=f"{prefix}_4"),
        InlineKeyboardButton("5️⃣", callback_data=f"{prefix}_5"),
        InlineKeyboardButton("6️⃣", callback_data=f"{prefix}_6")
    ]
    
    row3 = [
        InlineKeyboardButton("7️⃣", callback_data=f"{prefix}_7"),
        InlineKeyboardButton("8️⃣", callback_data=f"{prefix}_8"),
        InlineKeyboardButton("9️⃣", callback_data=f"{prefix}_9")
    ]
    
    row4 = [
        InlineKeyboardButton("⌨️ پاک کن", callback_data=f"{prefix}_clear"),
        InlineKeyboardButton("0️⃣", callback_data=f"{prefix}_0"),
        InlineKeyboardButton("✅ ارسال", callback_data=f"{prefix}_send")
    ]
    
    row5 = [
        InlineKeyboardButton("🔙 انصراف", callback_data=f"{prefix}_cancel")
    ]
    
    buttons.append(row1)
    buttons.append(row2)
    buttons.append(row3)
    buttons.append(row4)
    buttons.append(row5)
    
    return InlineKeyboardMarkup(buttons)

def format_code_display(code):
    if not code:
        return "⚪.⚪.⚪.⚪.⚪"
    
    digits = list(code)
    while len(digits) < 5:
        digits.append("⚪")
    
    return ".".join(digits)

async def activate_self_after_auth(client, user_id, phone, success_message=True):
    activation_cost, hourly_cost = self_costs()
    credits = db.get("credits", user_id, 0)
    if credits < activation_cost:
        await client.send_message(user_id, f"❌ موجودی برای فعال‌سازی کافی نیست.\n\n💎 هزینه فعال‌سازی: <b>{activation_cost}</b> الماس\n💎 موجودی شما: <b>{credits}</b> الماس", parse_mode=enums.ParseMode.HTML)
        return False
    db.set("credits", user_id, credits - activation_cost)
    if not run_selfbot(user_id, phone):
        db.set("credits", user_id, credits)
        await client.send_message(user_id, "❌ راه‌اندازی سلف ناموفق بود و هزینه فعال‌سازی به موجودی شما برگشت داده شد.")
        return False
    remaining = db.get("credits", user_id, 0)
    if success_message:
        await client.send_message(
            user_id,
            f"✅ <b>سلف با موفقیت فعال شد!</b>\n\n"
            f"📱 شماره: <code>{html.escape(phone)}</code>\n"
            f"💎 هزینه فعال‌سازی: <code>{activation_cost}</code> الماس\n"
            f"💎 موجودی باقی‌مانده: <code>{remaining}</code> الماس\n"
            f"⏱ مصرف خودکار: <code>{hourly_cost}</code> الماس در هر ساعت",
            parse_mode=enums.ParseMode.HTML
        )
    return True

async def request_phone_code(client, user_id, phone):
    if not phone.startswith("+") or not phone[1:].isdigit() or not (10 <= len(phone[1:]) <= 15):
        await client.send_message(user_id, "❌ شماره معتبر نیست. شماره را با کد کشور وارد کنید؛ مثال: <code>+989123456789</code>", parse_mode=enums.ParseMode.HTML)
        return False
    if user_id in active_clients:
        try:
            await active_clients[user_id].disconnect()
            del active_clients[user_id]
        except Exception:
            pass
    try:
        session_name=f"sessions/{user_id}"
        temp_client=Client(session_name, api_id=API_ID, api_hash=API_HASH)
        await temp_client.connect()
        active_clients[user_id]=temp_client
        sent_code=await temp_client.send_code(phone)
        user_data=db.get("users", user_id, {})
        user_data["phone"]=phone
        db.set("users", user_id, user_data)
        db.set("temp_data", user_id, {"phone": phone, "phone_code_hash": sent_code.phone_code_hash, "client_active": True, "activation_pending": True})
        user_temp_codes[user_id]=""
        await client.send_message(
            user_id,
            "🔐 <b>کد ورود تلگرام ارسال شد</b>\n\n"
            f"📱 شماره: <code>{html.escape(phone)}</code>\n"
            f"{format_code_display('')}\n\n"
            "کد ۵ رقمی را فقط با صفحه‌کلید زیر وارد کنید.",
            reply_markup=create_numpad_keyboard(),
            parse_mode=enums.ParseMode.HTML
        )
        return True
    except Exception as e:
        await client.send_message(user_id, f"❌ ارسال کد ناموفق بود:\n<code>{html.escape(str(e))}</code>", parse_mode=enums.ParseMode.HTML)
        if user_id in active_clients:
            try:
                await active_clients[user_id].disconnect()
                del active_clients[user_id]
            except Exception:
                pass
        return False

async def handle_code_from_keyboard(client, code_message):
    user_id = code_message.from_user.id
    code = code_message.text 

    code = code.replace(".", "")
    
    temp_data = db.get("temp_data", user_id)
    
    if not temp_data:
        await client.send_message(user_id, "❌ اطلاعات یافت نشد\nلطفا دوباره شماره تلفن را ارسال کنید")
        return
    
    try:
        if user_id in active_clients:
            user_client = active_clients[user_id]
        else:
            session_name = f"sessions/{user_id}"
            user_client = Client(session_name, api_id=API_ID, api_hash=API_HASH)
            await user_client.connect()
            active_clients[user_id] = user_client
        
        try: 
            await user_client.sign_in(temp_data["phone"], temp_data["phone_code_hash"], code)
        except SessionPasswordNeeded:
            await client.send_message(
                user_id,
                "🔒 **رمز دو مرحله‌ای نیاز است**\n\n"
                "لطفا رمز دو مرحله‌ای خود را به صورت متن ارسال کنید:"
            )
            db.set("temp_data", user_id, {**temp_data, "needs_password": True})
            return
        
        user_info = {
            "phone": temp_data["phone"],
            "status": "active", 
            "created_at": time.time(),
            "last_active": time.time(),
            "verified": db.get("users", user_id, {}).get("verified", False)
        }
        db.set("users", user_id, user_info)
        db.delete("temp_data", user_id)
        
        if user_id in active_clients:
            try:
                await active_clients[user_id].disconnect()
                del active_clients[user_id]
            except:
                pass

        await activate_self_after_auth(client, user_id, temp_data["phone"], success_message=True)
        
    except Exception as e: 
        error_msg = str(e)
        if "PHONE_CODE_EXPIRED" in error_msg:
            await client.send_message(
                user_id,
                "❌ **کد منقضی شده!**\n\n"
                "لطفا دوباره شماره تلفن خود را ارسال کنید."
            )
            db.delete("temp_data", user_id)
            if user_id in active_clients:
                try:
                    await active_clients[user_id].disconnect()
                    del active_clients[user_id]
                except:
                    pass
        else:
            await client.send_message(user_id, f"❌ **خطا:** {error_msg}")

async def cancel_group_bet_if_no_joiner(client, bet_key):
    await asyncio.sleep(300) 

    bet_data = db.get("group_bets", bet_key)
    if not bet_data or bet_data.get("finished"):
        return

    participants = bet_data.get("participants", [])
    chat_id = bet_data["chat_id"]
    message_id = bet_data["message_id"]
    amount = bet_data["amount"]
    creator_id = bet_data["creator_id"]
    creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
    creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
    
    if len(participants) > 0:
        return
    
    if bet_data.get("refunded"):
        return
    
    creator_credits = db.get("credits", creator_id, 0)
    db.set("credits", creator_id, creator_credits + amount)

    bet_data["finished"] = True
    bet_data["is_active"] = False
    bet_data["refunded"] = True
    db.set("group_bets", bet_key, bet_data)

    text = (
        "⛔ شرط به دلیل عدم شرکت‌کننده لغو شد.\n\n"
        f"👤 سازنده: {creator_mention}\n"
        f"💰 مبلغ شرط: <code>{amount}</code> الماس\n"
        "💸 مبلغ به سازنده برگشت داده شد."
    )
    
    try:
        await client.edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
    except:
        pass

    try:
        await client.send_message(
            creator_id,
            f"⛔ **شرط شما لغو شد!**\n\n"
            f"به دلیل عدم شرکت‌کننده، شرط شما لغو شد.\n"
            f"💰 مبلغ شرط: <code>{amount}</code> الماس\n"
            f"💸 مبلغ به حساب شما برگشت داده شد.\n\n"
            f"📊 موجودی جدید شما: <code>{db.get('credits', creator_id, 0)}</code> الماس"
        )
    except:
        pass

async def finish_group_bet(client, bet_key):
    await asyncio.sleep(5)

    bet_data = db.get("group_bets", bet_key)
    if not bet_data or bet_data.get("finished"):
        return

    chat_id = bet_data["chat_id"]
    message_id = bet_data["message_id"]
    amount = bet_data["amount"]
    creator_id = bet_data["creator_id"]
    creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
    creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
    participants = bet_data.get("participants", [])
    
    if len(participants) == 0:
        if not bet_data.get("refunded"):
            creator_credits = db.get("credits", creator_id, 0)
            db.set("credits", creator_id, creator_credits + amount)
            bet_data["refunded"] = True

        bet_data["finished"] = True
        bet_data["is_active"] = False
        db.set("group_bets", bet_key, bet_data)

        text = (
            "⛔ <b>شرط به حد نصاب نرسید و لغو شد.</b>\n\n"
            f"💰 <b>مبلغ هر نفر:</b> <code>{amount}</code> الماس\n"
            f"👤 <b>سازنده:</b> {creator_mention}"
        )
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=None,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            pass
        return
    
    players = [{"id": creator_id, "name": bet_data.get('creator_name', 'کاربر')}] + participants
    player_ids = [creator_id] + [p["id"] for p in participants]
    player_mentions = [creator_mention]
    for p in participants:
        p_name = html.escape(p.get('name', 'کاربر'))
        player_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
    
    pot = (1 + len(participants)) * amount 

    winner_index = random.choice(range(len(players)))
    winner_id = player_ids[winner_index]
    winner_mention = player_mentions[winner_index]
    winner_credits = db.get("credits", winner_id, 0) + pot
    db.set("credits", winner_id, winner_credits)

    bet_data["finished"] = True
    bet_data["is_active"] = False
    bet_data["winner_id"] = winner_id
    bet_data["winner_name"] = players[winner_index].get("name", "کاربر")
    bet_data["pot"] = pot
    db.set("group_bets", bet_key, bet_data)

    players_list = []
    for mention in player_mentions:
        players_list.append(f"• {mention}")
    players_text = "\n".join(players_list)

    result_text = (
        "🎉 <b>نتیجه شرط 1v1</b>\n\n"
        f"💰 <b>مبلغ هر نفر:</b> <code>{amount}</code> الماس\n"
        f"👥 <b>تعداد بازیکنان:</b> <code>{len(players)}</code> نفر\n"
        f"📋 <b>فهرست بازیکنان:</b>\n{players_text}\n\n"
        f"🏆 <b>برنده:</b> {winner_mention}\n"
        f"💎 <b>جایزه:</b> <code>{pot}</code> الماس"
    )

    try:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=result_text,
            reply_markup=None,
            parse_mode=enums.ParseMode.HTML
        )
    except:
        pass

    try:
        await client.send_message(
            chat_id,
            f"🏆 {winner_mention} برنده شرط <code>{amount}</code> الماس‌ای شد و <b>{pot}</b> الماس دریافت کرد!",
            parse_mode=enums.ParseMode.HTML
        )
    except:
        pass
    try:
        await client.send_message(
            winner_id,
            f"🎉 <b>تبریک! شما برنده شرط شدید!</b>\n\n"
            f"💰 <b>مبلغ شرط:</b> <code>{amount}</code> الماس\n"
            f"💎 <b>جایزه دریافتی:</b> <code>{pot}</code> الماس\n"
            f"👥 <b>تعداد بازیکنان:</b> {len(players)} نفر\n\n"
            f"📊 <b>موجودی جدید شما:</b> <code>{db.get('credits', winner_id, 0)}</code> الماس",
            parse_mode=enums.ParseMode.HTML
        )
    except:
        pass
    for player in players:
        if player["id"] != winner_id:
            try:
                await client.send_message(
                    player["id"],
                    f"😔 <b>متاسفانه شما در شرط باختید!</b>\n\n"
                    f"💰 <b>مبلغ شرط:</b> <code>{amount}</code> الماس\n"
                    f"👥 <b>تعداد بازیکنان:</b> {len(players)} نفر\n"
                    f"🏆 <b>برنده:</b> {winner_mention}\n\n"
                    f"📊 <b>موجودی فعلی شما:</b> <code>{db.get('credits', player['id'], 0)}</code> الماس",
                    parse_mode=enums.ParseMode.HTML
                )
            except:
                pass

async def check_force_join(client, user_id):
    not_joined = []

    for ch in FORCE_CHANNELS:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ("kicked", "banned"):
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not_joined:
        return False, not_joined
    
    return True, []

def deduct_credit_callback(user_id):
    try:
        if not db.get("processes", user_id): 
            return
        credits = db.get("credits", user_id, 0)
        hourly_cost = int(db.get("settings", "self_hourly_cost", SELF_HOURLY_COST))
        if credits >= hourly_cost:
            new_credits = credits - hourly_cost
            db.set("credits", user_id, new_credits)
            if new_credits < hourly_cost:
                stop_selfbot(user_id)
                db.set("credits", user_id, 0) 
                try: 
                    bot.send_message(
                        user_id, 
                        "❌ **الماس های شما تمام شد!**\n\n"
                        "سلف بات متوقف شد.\n\n"
                        "💰 برای ادامه استفاده، از طریق منوی «افزایش موجودی» حساب خود را شارژ کنید."
                    )
                except: 
                    pass
            else:
                if user_id in user_timers: 
                    user_timers[user_id].start()
        else:
            stop_selfbot(user_id)
            db.set("credits", user_id, 0)
            try: 
                bot.send_message(
                    user_id, 
                    "❌ **الماس های شما تمام شد!**\n\n"
                    "سلف بات متوقف شد.\n\n"
                    "💰 برای ادامه استفاده، از طریق منوی «افزایش موجودی» حساب خود را شارژ کنید."
                )
            except: 
                pass
    except Exception as e:
        print(f"❌ خطا در deduct_credit_callback: {e}")

def run_selfbot(user_id, phone=None):
    try:
        stop_selfbot(user_id)

        if phone:
            cmd = [sys.executable, "self.py", str(user_id), phone, str(API_ID), API_HASH]
        else:
            cmd = [sys.executable, "self.py", str(user_id)]
        
        process = subprocess.Popen(cmd)
        pid = process.pid
        db.set("processes", user_id, pid)
        user_data = db.get("users", user_id, {})
        user_data["status"] = "active"
        user_data["last_active"] = time.time()
        if phone:
            user_data["phone"] = phone
        db.set("users", user_id, user_data)
        
        with open(f"process_{user_id}.pid", "w") as f:
            f.write(str(pid))
        
        print(f"✅ سلف‌بات برای کاربر {user_id} راه‌اندازی شد")
        print(f"   📱 شماره: {phone}")
        print(f"   🆔 PID: {pid}")
        print(f"   💰 الماس: {db.get('credits', user_id, 0)}")
        print("-" * 50)
        
        if user_id not in user_timers:
            user_timers[user_id] = UserTimer(user_id, deduct_credit_callback)
        user_timers[user_id].start()
        
        return True
    except Exception as e:
        print(f"❌ خطا در اجرای سلف‌بات: {e}")
        return False

def stop_selfbot(user_id):
    try:
        if user_id in user_timers:
            user_timers[user_id].stop()
            if not db.get("users", user_id): 
                del user_timers[user_id]
        
        pid = db.get("processes", user_id)
        if pid:
            try:
                import os
                import signal
                try:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.5)
                except:
                    pass
                try:
                    os.kill(pid, signal.SIGKILL)
                except:
                    pass
                try:
                    import subprocess
                    subprocess.run(["pkill", "-f", f"self.py {user_id}"], 
                                 capture_output=True, check=False)
                    subprocess.run(["pkill", "-f", "self.py"], 
                                 capture_output=True, check=False)
                except:
                    pass
                
            except Exception as e:
                print(f"⚠️ خطا در قطع پروسس: {e}")
            
            db.delete("processes", user_id)
            user_data = db.get("users", user_id, {})
            if user_data:
                user_data["status"] = "inactive"
                db.set("users", user_id, user_data)
            
            try:
                os.remove(f"process_{user_id}.pid")
            except:
                pass
            
            print(f"✅ سلف‌بات کاربر {user_id} قطع شد (PID: {pid})")
            return True
        
        try:
            import subprocess
            subprocess.run(["pkill", "-f", f"self.py {user_id}"], check=False)
            subprocess.run(["pkill", "-f", "self.py"], check=False)
            db.delete("processes", user_id)
            user_data = db.get("users", user_id, {})
            if user_data:
                user_data["status"] = "inactive"
                db.set("users", user_id, user_data)
            
            print(f"✅ سلف‌بات کاربر {user_id} قطع شد (از طریق pkill)")
            return True
        except:
            pass
            
        return False
    except Exception as e:
        print(f"❌ خطا در stop_selfbot: {e}")
        return False

def check_selfbot_status(user_id):
    pid = db.get("processes", user_id)
    if not pid:
        return False    
    try:
        import os
        os.kill(pid, 0) 
        return True
    except OSError:
        db.delete("processes", user_id)
        user_data = db.get("users", user_id, {})
        if user_data:
            user_data["status"] = "inactive"
            db.set("users", user_id, user_data)
        return False
        
def stop_all_selfbots():
    try:
        for timer in list(user_timers.values()): 
            timer.stop()
        user_timers.clear()
        for pid in db.data.get("processes", {}).values():
            try: 
                import psutil
                psutil.Process(pid).terminate()
            except: 
                pass
        db.data["processes"], db.data["timers"] = {}, {}
        db.save_data()
    except: 
        pass

@bot.on_message(filters.group & filters.regex(r'^موجودی$'))
async def group_balance_handler(client, message: Message):
    user_id = message.from_user.id
    user_first_name = html.escape(message.from_user.first_name or "کاربر")
    user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
    
    ok, not_joined = await check_force_join(client, user_id)
    if not ok:
        buttons = []
        for ch in FORCE_CHANNELS:
            buttons.append([InlineKeyboardButton(f"● عضویت در @{ch}", url=f"https://t.me/{ch}")])
        buttons.append([InlineKeyboardButton("● بررسی مجدد", callback_data="check_join")])
        
        await message.reply_text(
            "● <b>برای مشاهده موجودی باید در کانال‌های زیر عضو باشید:</b>\n\n" +
            "\n".join([f"• @{channel}" for channel in FORCE_CHANNELS]),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    credits = db.get("credits", user_id, 0)
    user_data = db.get("users", user_id, {})
    phone = user_data.get('phone', 'ثبت نشده')
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"{font_convert(credits)}", 
            callback_data="my_balance"
        )]
    ])
    
    balance_text = f"""
<b>● اطلاعات کاربر●</b>

<b>● آیدی عددی:</b> <code>{font_convert(user_id)}</code>
<b>● نام:</b> {user_mention}
"""
    
    await message.reply_text(
        balance_text,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )

@bot.on_message(filters.command("set") & filters.user(ADMIN_ID))
async def set_credits(client, message: Message):
    if len(message.command) != 3:
        await message.reply_text("❌ فرمت: `/set آیدی تعداد`")
        return    
    try:
        target_id = int(message.command[1])
        amount = int(message.command[2])
        db.set("credits", target_id, amount)
        
        await message.reply_text(f"✅ الماس کاربر {target_id} تنظیم شد به {amount}")       
        try:
            await bot.send_message(target_id, f"🔧 موجودی الماس شما تنظیم شد\n💰 جدید: {amount} الماس")
        except: 
            pass        
    except: 
        await message.reply_text("❌ آیدی/تعداد باید عدد باشد")

@bot.on_message(filters.group & filters.regex(r'^شرطبندی\s+(\d+)(?:\s*الماس)?$'))
async def group_bet_handler(client, message: Message):
    chat_id = message.chat.id
    creator_id = message.from_user.id
    try:
        amount = int(message.matches[0].group(1))
    except:
        return
    if amount <= 0:
        await message.reply_text("❌ مقدار شرط باید بیشتر از صفر باشد.")
        return    
    creator_credits = db.get("credits", creator_id, 0)
    if creator_credits < amount:
        await message.reply_text(
            f"❌ الماس کافی برای ساخت شرط ندارید.\n"
            f"💰 موجودی شما: {creator_credits} الماس"
        )
        return
    
    db.set("credits", creator_id, creator_credits - amount)
    creator_first_name = html.escape(message.from_user.first_name or 'کاربر')
    creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'

    bet_text = (
        "🎲 <b>شرطبندی درحال اجرا ...</b>\n\n"
        f"💰 <b>مبلغ هر نفر:</b> <code>{amount}</code> الماس\n"
        f"👤 <b>سازنده:</b> {creator_mention}\n\n"
        "برای شرکت در این شرط روی دکمه «پیوستن به شرط» بزنید.\n"
        "⛔ اگر تا ۵ دقیقه کسی شرکت نکند، شرط لغو و مبلغ به سازنده برمی‌گردد.\n"
        "⏳ پس از پیوستن نفر دوم، ۵ ثانیه بعد برنده مشخص می‌شود."
    )
    keyboard = create_colored_buttons(
        f"joinbet_{chat_id}_waiting",
        f"cancelbet_{chat_id}_waiting"
    )
    bet_photo = db.get("settings", BET_PHOTO_SETTING, None) or db.get_welcome_photo()
    if bet_photo:
        sent_msg = await message.reply_photo(
            photo=bet_photo,
            caption=bet_text,
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        sent_msg = await message.reply_text(
            bet_text,
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )
    
    msg_id = sent_msg.id
    bet_key = f"{chat_id}_{msg_id}"
    
    new_keyboard = create_colored_buttons(
        f"joinbet_{chat_id}_{msg_id}",
        f"cancelbet_{chat_id}_{msg_id}"
    )
    
    await sent_msg.edit_reply_markup(
        reply_markup=new_keyboard
    )

    bet_data = {
        "chat_id": chat_id,
        "message_id": msg_id,
        "amount": amount,
        "creator_id": creator_id,
        "creator_name": message.from_user.first_name or "",
        "creator_username": message.from_user.username or "",
        "participants": [],
        "is_active": True,
        "finished": False,
        "timer_started": False,
        "created_at": time.time(),
        "refunded": False
    }

    db.set("group_bets", bet_key, bet_data)
    asyncio.create_task(cancel_group_bet_if_no_joiner(client, bet_key))

@bot.on_message(filters.group & filters.regex(r'^انتقال\s+(\d+)\s*(?:الماس)?\s*$'))
async def transfer_coins_handler(client, message: Message):
    user_id = message.from_user.id

    if not db.get_transfer_status():
        await message.reply_text("⛔ سیستم انتقال الماس در حال حاضر غیرفعال است.")
        return

    ok, not_joined = await check_force_join(client, user_id)
    if not ok:
        buttons = []
        for ch in FORCE_CHANNELS:
            buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
        buttons.append([InlineKeyboardButton("🔁 بررسی مجدد", callback_data="check_join")])
        
        await message.reply_text(
            "⚠️ **برای انتقال الماس باید در کانال‌های زیر عضو باشید:**\n\n" +
            "\n".join([f"• @{channel}" for channel in FORCE_CHANNELS]),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    if not message.reply_to_message:
        await message.reply_text(
            "❌ **فرمت اشتباه!**\n\n"
            "برای انتقال الماس به یک پیام ریپلای کنید:\n"
            "<b>انتقال 10</b>"
        )
        return
    
    try:
        amount = int(message.matches[0].group(1))
    except:
        await message.reply_text("❌ مقدار باید عدد باشد")
        return
    
    if amount <= 0:
        await message.reply_text("❌ مقدار انتقال باید بیشتر از صفر باشد")
        return

    settings = db.data.get("settings", {})
    tax_percent = settings.get("tax_percent", 10)
    tax_min_amount = settings.get("tax_min_amount", 10)
    
    tax_amount = 0
    if amount >= tax_min_amount:
        tax_amount = int(amount * tax_percent / 100)
        if tax_amount < 1:
            tax_amount = 1
    
    final_amount = amount - tax_amount
    
    sender_id = message.from_user.id
    sender_credits = db.get("credits", sender_id, 0)
    
    if sender_credits < amount:
        await message.reply_text(
            f"❌ **الماس کافی ندارید!**\n\n"
            f"💰 موجودی شما: <code>{sender_credits}</code> الماس\n"
            f"💸 نیاز دارید: <code>{amount}</code> الماس\n\n"
            f"📊 <b>جزئیات انتقال:</b>\n"
            f"├─ مبلغ اصلی: <code>{amount}</code> الماس\n"
            f"├─ مالیات ({tax_percent}%): <code>{tax_amount}</code> الماس\n"
            f"└─ مبلغ دریافتی گیرنده: <code>{final_amount}</code> الماس"
        )
        return
    
    receiver = message.reply_to_message.from_user
    receiver_id = receiver.id
    
    if sender_id == receiver_id:
        await message.reply_text("❌ نمی‌توانید به خودتان الماس انتقال دهید!")
        return
    
    if receiver.is_bot:
        await message.reply_text("❌ نمی‌توانید به ربات الماس انتقال دهید!")
        return

    db.set("credits", sender_id, sender_credits - amount)
    receiver_credits = db.get("credits", receiver_id, 0)
    db.set("credits", receiver_id, receiver_credits + final_amount)
    
    if tax_amount > 0:
        admin_credits = db.get("credits", ADMIN_ID, 0)
        db.set("credits", ADMIN_ID, admin_credits + tax_amount)
        
    sender_name = html.escape(message.from_user.first_name or "کاربر")
    receiver_name = html.escape(receiver.first_name or "کاربر")
    sender_mention = f'<a href="tg://user?id={sender_id}"><b>{sender_name}</b></a>'
    receiver_mention = f'<a href="tg://user?id={receiver_id}"><b>{receiver_name}</b></a>'

    await message.reply_text(
        f"✔️ <b>انتقال الماس انجام شد!</b>\n\n"
        f"● <b>فرستنده:</b> {sender_mention}\n"
        f"● <b>گیرنده:</b> {receiver_mention}\n"
        f"● <b>مبلغ اصلی:</b> <code>{amount}</code> الماس\n"
        f"● <b>مالیات ({tax_percent}%):</b> <code>{tax_amount}</code> الماس\n"
        f"● <b>مبلغ دریافتی گیرنده:</b> <code>{final_amount}</code> الماس\n\n"
        f"● <b>موجودی {sender_name}:</b> <code>{db.get('credits', sender_id, 0)}</code> الماس\n"
        f"● <b>موجودی {receiver_name}:</b> <code>{db.get('credits', receiver_id, 0)}</code> الماس",
        parse_mode=enums.ParseMode.HTML
    )
    
    try:
        await client.send_message(
            sender_id,
            f"● <b>انتقال الماس انجام شد!</b>\n\n"
            f"● <b>گیرنده:</b> {receiver_mention}\n"
            f"● <b>مبلغ اصلی:</b> <code>{amount}</code> الماس\n"
            f"● <b>مالیات ({tax_percent}%):</b> <code>{tax_amount}</code> الماس\n"
            f"● <b>مبلغ دریافتی گیرنده:</b> <code>{final_amount}</code> الماس\n\n"
            f"● <b>موجودی جدید شما:</b> <code>{db.get('credits', sender_id, 0)}</code> الماس",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"❌ خطا در ارسال پیام به فرستنده: {e}")
      
    try:
        await client.send_message(
            receiver_id,
            f"● <b>الماس دریافت کردید!</b>\n\n"
            f"● <b>از طرف:</b> {sender_mention}\n"
            f"● <b>مبلغ اصلی:</b> <code>{amount}</code> الماس\n"
            f"● <b>مالیات کسر شده:</b> <code>{tax_amount}</code> الماس\n"
            f"● <b>مبلغ دریافتی:</b> <code>{final_amount}</code> الماس\n\n"
            f"● <b>موجودی جدید شما:</b> <code>{db.get('credits', receiver_id, 0)}</code> الماس",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"❌ خطا در ارسال پیام به گیرنده: {e}")

@bot.on_message(filters.command("user") & filters.user(ADMIN_ID))
async def user_info(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("❌ فرمت: `/user آیدی`")
        return
    
    try:
        target_id = int(message.command[1])
        user_data = db.get("users", target_id, {})
        credits = db.get("credits", target_id, 0)
        process = db.get("processes", target_id)
        timer = db.get("timers", target_id)
        
        if not user_data:
            await message.reply_text("❌ کاربر یافت نشد")
            return
        
        status = "🟢 فعال" if user_data.get('status') == 'active' else "🔴 غیرفعال"
        phone = user_data.get('phone', '❌ ثبت نشده')
        created = time.ctime(user_data.get('created_at', time.time()))
        running = "🟢 بله" if process else "🔴 خیر"
        has_timer = "🟢 فعال" if timer and timer.get('is_running') else "🔴 غیرفعال"
        verified_status = "✅ تایید شده" if user_data.get('verified') else "❌ تایید نشده"
        rejected_status = "❌ رد شده" if user_data.get('rejected') else "✅ فعال"
        
        created_time = user_data.get('created_at', time.time())
        time_diff = time.time() - created_time
        days = int(time_diff // 86400)
        hours = int((time_diff % 86400) // 3600)
        
        info_text = f"""
👤 **اطلاعات کاربر {target_id}**

📱 **شماره:** `{phone}`
📊 **وضعیت:** {status}
🔐 **احراز هویت:** {verified_status}
🚫 **وضعیت رد:** {rejected_status}
💰 **الماس ها:** `{credits}`
🔄 **سلف:** {running}
📅 **تاریخ ایجاد:** `{created}`
⏳ **عضو شده:** {days} روز و {hours} ساعت

⏱ **زمان باقی‌مانده:** `{credits}` ساعت
💸 **مصرف الماس:** 2 الماس در ساعت
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 تنظیم الماس", callback_data=f"set_{target_id}"),
             InlineKeyboardButton("🛑 توقف سلف", callback_data=f"stop_{target_id}")],
            [InlineKeyboardButton("✅ تایید احراز", callback_data=f"verify_approve_{target_id}"),
             InlineKeyboardButton("❌ رد احراز", callback_data=f"verify_reject_{target_id}")]
        ])
        
        await message.reply_text(info_text, reply_markup=keyboard)
        
    except: 
        await message.reply_text("❌ آیدی باید عدد باشد")

@bot.on_message(filters.command("admin") & filters.user(ADMIN_ID))
async def admin_panel(client, message: Message):
    users = db.data.get("users", {})
    active_count = len(db.data.get("processes", {}))
    total_credits = sum(db.data.get("credits", {}).values())
    verified_users = len(db.get_verified_users())
    pending_verifications = len(db.get_pending_verifications())
    pending_payments = len(db.get_pending_payments())
    
    today = time.time() - 86400
    new_today = sum(1 for user_data in users.values() if user_data.get('created_at', 0) > today)
    
    transfer_status = db.get_transfer_status()
    transfer_text = "🟢 روشن" if transfer_status else "🔴 خاموش"
    
    stats_text = f"""
🛠 **پنل مدیریت ادمین**

👥 **کل کاربران:** `{len(users)}`
🟢 **کاربران فعال:** `{active_count}`
✅ **کاربران تایید شده:** `{verified_users}`
🆕 **کاربران امروز:** `{new_today}`
💰 **مجموع الماس ها:** `{total_credits}`

📋 **درخواست‌های در انتظار:**
├─ 🔐 احراز هویت: `{pending_verifications}`
└─ 💰 پرداخت: `{pending_payments}`

🔄 **وضعیت انتقال الماس:** {transfer_text}

**📋 دستورات سریع:**
`/set آیدی تعداد` - تنظیم الماس
`/user آیدی` - اطلاعات کاربر
`/admin` - این پنل
"""
    
    if ButtonStyle is None:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list"),
                InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top"),
                InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all")
            ],
            [
                InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications"),
                InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments")
            ],
            [
                InlineKeyboardButton("🔄 روشن کردن انتقال", callback_data="admin_transfer_on"),
                InlineKeyboardButton("⛔ خاموش کردن انتقال", callback_data="admin_transfer_off")
            ],
            [
                InlineKeyboardButton("📸 تنظیم عکس خوش‌آمدگویی", callback_data="admin_set_photo")
            ]
        ])
    else:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats", style=ButtonStyle.PRIMARY)
            ],
            [
                InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all", style=ButtonStyle.DANGER)
            ],
            [
                InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments", style=ButtonStyle.PRIMARY)
            ],
            [
                InlineKeyboardButton("🔄 روشن کردن انتقال", callback_data="admin_transfer_on", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("⛔ خاموش کردن انتقال", callback_data="admin_transfer_off", style=ButtonStyle.DANGER)
            ],
            [
                InlineKeyboardButton("📸 تنظیم عکس خوش‌آمدگویی", callback_data="admin_set_photo", style=ButtonStyle.PRIMARY)
            ]
        ])
    
    await message.reply_text(stats_text, reply_markup=keyboard)

@bot.on_callback_query(filters.regex(r'^code_'))
async def numpad_callback(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    current_code = user_temp_codes.get(user_id, "")
    
    if data == "code_clear":
        user_temp_codes[user_id] = current_code[:-1]
        display_code = user_temp_codes[user_id]

        formatted = format_code_display(display_code)
        
        try:
            await callback_query.message.edit_text(
                f"🔢 **کد تایید را وارد کنید:**\n\n"
                f"<b><code>{formatted}</code></b>\n\n"
                f"📱 کد {len(display_code)}/5 رقم وارد شد",
                reply_markup=create_numpad_keyboard(),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(f"❌ خطا در ویرایش پیام: {e}")
        
        await callback_query.answer()
        
    elif data == "code_send":
        if len(current_code) == 5:
            await callback_query.answer("✅ کد ارسال شد...", show_alert=True)
            class FakeMessage:
                def __init__(self, user_id, code):
                    self.from_user = type('obj', (object,), {'id': user_id})()
                    self.text = code
                    self.chat = type('obj', (object,), {'id': user_id})()
                    self.reply_text = None
                    
                async def reply_text(self, text, *args, **kwargs):
                    await client.send_message(user_id, text, *args, **kwargs)
            
            fake_msg = FakeMessage(user_id, current_code)

            await handle_code_from_keyboard(client, fake_msg)
            
            user_temp_codes.pop(user_id, None)
        else:
            await callback_query.answer(f"❌ کد باید 5 رقم باشد (الان {len(current_code)} رقم)", show_alert=True)
            
    elif data == "code_cancel":
        user_temp_codes.pop(user_id, None)
        try:
            await callback_query.message.edit_text(
                "❌ **ورود کد لغو شد**\n\n"
                "برای شروع مجدد از /start استفاده کنید",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
                ])
            )
        except Exception as e:
            print(f"❌ خطا در ویرایش پیام: {e}")
        
        await callback_query.answer()
        
    else:
        number = data.split("_")[1]
        
        if len(current_code) < 5:
            new_code = current_code + number
            user_temp_codes[user_id] = new_code
            formatted = format_code_display(new_code)
            
            try:
                await callback_query.message.edit_text(
                    f"🔢 **کد تایید را وارد کنید:**\n\n"
                    f"<b><code>{formatted}</code></b>\n\n"
                    f"📱 کد {len(new_code)}/5 رقم وارد شد",
                    reply_markup=create_numpad_keyboard(),
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                print(f"❌ خطا در ویرایش پیام: {e}")
            
            await callback_query.answer()
        else:
            await callback_query.answer("❌ کد کامل شده است! روی 'ارسال' کلیک کنید", show_alert=True)

async def admin_callback_handler(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    if not is_admin_user(callback_query.from_user):
        await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
        return

    if data == "admin_economy":
        a,h=self_costs(); rate=int(settings_value("diamond_to_toman", DIAMOND_TO_TOMAN))
        text=(f"⚙️ <b>تنظیم اقتصاد سلف</b>\n\n💎 فعال‌سازی: <code>{a}</code> الماس\n⏱ مصرف ساعتی: <code>{h}</code> الماس\n💵 هر الماس: <code>{rate}</code> تومان\n\n"
              "برای تغییر هر سه مقدار، یک پیام مثل زیر ارسال کنید:\n<code>30 2 15</code>")
        await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✏️ تغییر مقادیر", callback_data="admin_economy_edit")],[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "admin_economy_edit":
        db.set("temp_data", f"admin_economy_{user_id}", True)
        await callback_query.message.edit_text("✏️ <b>مقادیر جدید را بفرستید</b>\nمثال: <code>30 2 15</code>\n\nترتیب: هزینه فعال‌سازی | هزینه هر ساعت | تومان هر الماس", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 انصراف", callback_data="admin_economy")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "admin_set_bet_photo":
        photo=db.get("settings", BET_PHOTO_SETTING, None)
        await callback_query.message.edit_text("📸 <b>عکس شرط‌بندی</b>\n\nوضعیت: " + ("✅ تنظیم شده" if photo else "❌ تنظیم نشده") + "\n\nعکس را ارسال کنید تا برای شرط‌های گروهی استفاده شود.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 ارسال عکس", callback_data="admin_send_bet_photo")],[InlineKeyboardButton("🗑 حذف عکس", callback_data="admin_delete_bet_photo")],[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "admin_send_bet_photo":
        db.set("temp_data", f"admin_waiting_bet_photo_{user_id}", True)
        await callback_query.message.edit_text("📤 <b>عکس شرط را ارسال کنید.</b>\n\nاین عکس در پیام‌های شرطبندی گروهی قرار می‌گیرد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_set_bet_photo")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "admin_delete_bet_photo":
        db.delete("settings", BET_PHOTO_SETTING)
        db.set("settings", BET_PHOTO_SETTING, None)
        await callback_query.message.edit_text("✅ عکس شرط حذف شد و عکس خوش‌آمدگویی به‌عنوان پشتیبان استفاده می‌شود.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_set_bet_photo")]]))
        await callback_query.answer(); return
    if data == "admin_broadcast":
        db.set("temp_data", f"admin_broadcast_{user_id}", True)
        await callback_query.message.edit_text("📢 <b>پیام همگانی</b>\n\nمتن پیام را ارسال کنید. پیام برای همه کاربران ثبت‌شده ارسال می‌شود.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 انصراف", callback_data="admin_back")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "admin_games":
        active_games=[g for g in ttt_games.values() if not g.get("winner")]
        await callback_query.message.edit_text(f"🎮 <b>بازی‌های دوز فعال:</b> <code>{len(active_games)}</code>\n\nبرای ساخت بازی جدید، از منوی کاربری یا دستور <code>دوز</code> در گروه استفاده کنید.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    
    if data == "admin_panel":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return

        await admin_panel(client, callback_query.message)
        await callback_query.answer()
        return
    if data == "admin_transfer_on":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
        db.set_transfer_status(True)
        await callback_query.message.edit_text("✅ سیستم انتقال الماس روشن شد.")
        await callback_query.answer()
        return
    
    if data == "admin_transfer_off":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
        db.set_transfer_status(False)
        await callback_query.message.edit_text("⛔ سیستم انتقال الماس خاموش شد.")
        await callback_query.answer()
        return
    
    if data == "admin_list":
        users = db.get_all("users")
        if not users:
            await callback_query.message.edit_text("❌ هیچ کاربری ثبت نشده است.")
            return
        
        text = "👥 **لیست کاربران:**\n\n"
        for i, (uid, info) in enumerate(list(users.items())[:20], 1):
            credits = db.get("credits", int(uid), 0)
            status = "🟢" if info.get('status') == 'active' else "🔴"
            verified = "✅" if info.get('verified') else "❌"
            text += f"{i}. {status} {verified} `{uid}` → {credits} الماس\n"
        
        if len(users) > 20:
            text += f"\n... و {len(users) - 20} کاربر دیگر"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()
    elif data == "admin_set_photo":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
    
        current_photo = db.get_welcome_photo()
        status_text = "✅ تنظیم شده" if current_photo else "❌ تنظیم نشده"
    
        text = (
            f"📸 **تنظیم عکس خوش‌آمدگویی**\n\n"
            f"📊 **وضعیت فعلی:** {status_text}\n\n"
            f"🔹 برای تنظیم عکس جدید، عکس را ارسال کنید.\n"
            f"🔹 برای حذف عکس فعلی، روی دکمه حذف کلیک کنید.\n\n"
            f"⚠️ عکس باید با کیفیت مناسب باشد.\n"
            f"📱 عکس در صفحه شروع و تمام بخش‌ها نمایش داده می‌شود."
        )
        
        if ButtonStyle is None:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 ارسال عکس جدید", callback_data="admin_send_photo")],
                [InlineKeyboardButton("🗑️ حذف عکس فعلی", callback_data="admin_delete_photo")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 ارسال عکس جدید", callback_data="admin_send_photo", style=ButtonStyle.SUCCESS)],
                [InlineKeyboardButton("🗑️ حذف عکس فعلی", callback_data="admin_delete_photo", style=ButtonStyle.DANGER)],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back", style=ButtonStyle.DANGER)]
            ])
    
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()

    elif data == "admin_send_photo":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
    
        text = (
        "📸 **لطفا عکس مورد نظر را ارسال کنید**\n\n"
        "🔹 عکس را به صورت مستقیم در این چت ارسال کنید.\n"
        "🔹 پس از ارسال، به‌طور خودکار ذخیره می‌شود.\n"
        "🔹 در تمام بخش‌های ربات نمایش داده می‌شود."
        )
    
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_set_photo")]
        ])
    
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        db.set("temp_data", f"admin_waiting_photo_{user_id}", True)
        await callback_query.answer()

    elif data == "admin_delete_photo":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
    
        current_photo = db.get_welcome_photo()
        if current_photo:
            db.delete_welcome_photo()
            text = "✅ **عکس خوش‌آمدگویی با موفقیت حذف شد!**\n\n🔄 ربات به حالت عادی (بدون عکس) بازگشت."
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت به تنظیمات", callback_data="admin_set_photo")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
        else:
            await callback_query.answer("❌ هیچ عکسی تنظیم نشده است!", show_alert=True)
        await callback_query.answer()    
    elif data == "admin_stats":
        users = db.get_all("users")
        processes = db.get_all("processes")
        credits = db.get_all("credits")
        verifications = db.get_all("verifications")
        payments = db.get_all("payments")
        
        total_users = len(users)
        active_users = len(processes)
        total_credits = sum(credits.values()) if credits else 0
        pending_verif = sum(1 for v in verifications.values() if v.get('status') == 'pending')
        pending_pay = sum(1 for p in payments.values() if p.get('status') == 'pending')
        verified_users = sum(1 for u in users.values() if u.get('verified'))
        rejected_users = sum(1 for u in users.values() if u.get('rejected'))
        
        text = f"""
📊 **آمار کامل سیستم**

👥 **کاربران کل:** {total_users}
🟢 **فعال:** {active_users}
✅ **تایید شده:** {verified_users}
❌ **رد شده:** {rejected_users}

💰 **مجموع الماس‌ها:** {total_credits:,}

🔐 **درخواست احراز:** {pending_verif}
💳 **درخواست پرداخت:** {pending_pay}

📅 **تاریخ:** {time.ctime()}
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()
    
    elif data == "admin_top":
        credits = db.get_all("credits")
        if not credits:
            await callback_query.message.edit_text("❌ هیچ کاربری الماس ندارد.")
            return
        
        sorted_users = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "🏆 **برترین کاربران از نظر الماس:**\n\n"
        for i, (uid, amount) in enumerate(sorted_users, 1):
            user_data = db.get("users", int(uid), {})
            name = user_data.get('first_name', 'ناشناس')
            text += f"{i}. {name} → `{amount:,}` الماس\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()
    
    elif data == "admin_stop_all":
        await callback_query.message.edit_text("🛑 **در حال توقف همه سلف‌بات‌ها...**")
        stop_all_selfbots()
        await asyncio.sleep(1)
        await callback_query.message.edit_text("✅ **همه سلف‌بات‌ها متوقف شدند.**")
        await callback_query.answer()
    
    elif data == "admin_verifications":
        verifications = db.get_pending_verifications()
        if not verifications:
            await callback_query.message.edit_text("❌ هیچ درخواست احراز در انتظاری وجود ندارد.")
            return
        
        text = "🔐 **درخواست‌های احراز هویت:**\n\n"
        for uid, info in list(verifications.items())[:10]:
            name = info.get('first_name', 'ناشناس')
            text += f"👤 {name} → `{uid}`\n"
        
        if len(verifications) > 10:
            text += f"\n... و {len(verifications) - 10} درخواست دیگر"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()
    
    elif data == "admin_payments":
        payments = db.get_pending_payments()
        if not payments:
            await callback_query.message.edit_text("❌ هیچ درخواست پرداخت در انتظاری وجود ندارد.")
            return
        
        text = "💳 **درخواست‌های پرداخت:**\n\n"
        for uid, info in list(payments.items())[:10]:
            name = info.get('first_name', 'ناشناس')
            coins = info.get('coins', 0)
            text += f"👤 {name} → `{uid}` | {coins} الماس\n"
        
        if len(payments) > 10:
            text += f"\n... و {len(payments) - 10} درخواست دیگر"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer()
    
    elif data == "admin_back":
        await admin_panel(client, callback_query.message)
        await callback_query.answer()
    
    elif data.startswith("set_"):
        target_id = int(data.split("_")[1])
        db.set("temp_data", f"admin_set_{user_id}", target_id)
        await callback_query.message.edit_text(
            f"💰 **تعداد الماس جدید برای کاربر {target_id} را وارد کنید:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 انصراف", callback_data="admin_back")]
            ])
        )
        await callback_query.answer()
    
    elif data.startswith("stop_"):
        target_id = int(data.split("_")[1])
        if stop_selfbot(target_id):
            await callback_query.message.edit_text(f"✅ سلف‌بات کاربر {target_id} متوقف شد.")
        else:
            await callback_query.message.edit_text(f"ℹ️ سلف‌بات کاربر {target_id} از قبل متوقف بود.")
        await callback_query.answer()
    
    elif data.startswith("verify_approve_"):
        target_id = int(data.split("_")[2])
        user_data = db.get("users", target_id, {})
        user_data["verified"] = True
        user_data["rejected"] = False
        db.set("users", target_id, user_data)
        db.delete("verifications", target_id)
        
        await callback_query.message.edit_text(f"✅ احراز هویت کاربر {target_id} تایید شد.")
        try:
            await bot.send_message(
                target_id,
                "✅ **احراز هویت شما تایید شد!**\n\n"
                "اکنون می‌توانید از بخش «افزایش موجودی» استفاده کنید."
            )
        except:
            pass
        await callback_query.answer()
    
    elif data.startswith("verify_reject_"):
        target_id = int(data.split("_")[2])
        user_data = db.get("users", target_id, {})
        user_data["verified"] = False
        user_data["rejected"] = True
        db.set("users", target_id, user_data)
        db.delete("verifications", target_id)
        
        await callback_query.message.edit_text(f"❌ احراز هویت کاربر {target_id} رد شد.")
        try:
            await bot.send_message(
                target_id,
                "❌ **احراز هویت شما رد شد!**\n\n"
                "لطفا مجدداً با ارسال عکس واضح‌تر اقدام کنید."
            )
        except:
            pass
        await callback_query.answer()
    
    elif data.startswith("payment_approve_"):
        target_id = int(data.split("_")[2])
        payment_data = db.get("payments", target_id)
        if payment_data:
            coins = payment_data.get("coins", 0)
            current = db.get("credits", target_id, 0)
            db.set("credits", target_id, current + coins)
            payment_data["status"] = "approved"
            db.set("payments", target_id, payment_data)
            
            await callback_query.message.edit_text(
                f"✅ پرداخت کاربر {target_id} تایید شد.\n"
                f"💰 {coins} الماس به حسابش اضافه شد."
            )
            try:
                await bot.send_message(
                    target_id,
                    f"✅ **پرداخت شما تایید شد!**\n\n"
                    f"💰 {coins} الماس به حساب شما اضافه شد.\n"
                    f"📊 موجودی جدید: {db.get('credits', target_id, 0)} الماس"
                )
            except:
                pass
        else:
            await callback_query.message.edit_text(f"❌ اطلاعات پرداخت کاربر {target_id} یافت نشد.")
        await callback_query.answer()
    
    elif data.startswith("payment_reject_"):
        target_id = int(data.split("_")[2])
        payment_data = db.get("payments", target_id)
        if payment_data:
            payment_data["status"] = "rejected"
            db.set("payments", target_id, payment_data)
            
            await callback_query.message.edit_text(f"❌ پرداخت کاربر {target_id} رد شد.")
            try:
                await bot.send_message(
                    target_id,
                    "❌ **پرداخت شما رد شد!**\n\n"
                    "لطفا مجدداً با ارسال رسید واضح‌تر اقدام کنید."
                )
            except:
                pass
        else:
            await callback_query.message.edit_text(f"❌ اطلاعات پرداخت کاربر {target_id} یافت نشد.")
        await callback_query.answer()
        
@bot.on_message(filters.command("set") & filters.user(ADMIN_ID))
async def set_credits(client, message: Message):
    if len(message.command) != 3:
        await message.reply_text("❌ فرمت: `/set آیدی تعداد`")
        return
    
    try:
        target_id = int(message.command[1])
        amount = int(message.command[2])
        db.set("credits", target_id, amount)
        
        await message.reply_text(f"✅ الماس کاربر {target_id} تنظیم شد به {amount}")        
        try:
            await bot.send_message(target_id, f"🔧 موجودی الماس شما تنظیم شد\n💰 جدید: {amount} الماس")
        except: 
            pass        
    except: 
        await message.reply_text("❌ آیدی/تعداد باید عدد باشد")

@bot.on_message(filters.command("user") & filters.user(ADMIN_ID))
async def user_info(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("❌ فرمت: `/user آیدی`")
        return    
    try:
        target_id = int(message.command[1])
        user_data = db.get("users", target_id, {})
        credits = db.get("credits", target_id, 0)
        process = db.get("processes", target_id)
        timer = db.get("timers", target_id)
        
        if not user_data:
            await message.reply_text("❌ کاربر یافت نشد")
            return
        
        status = "🟢 فعال" if user_data.get('status') == 'active' else "🔴 غیرفعال"
        phone = user_data.get('phone', '❌ ثبت نشده')
        created = time.ctime(user_data.get('created_at', time.time()))
        running = "🟢 بله" if process else "🔴 خیر"
        has_timer = "🟢 فعال" if timer and timer.get('is_running') else "🔴 غیرفعال"
        verified_status = "✅ تایید شده" if user_data.get('verified') else "❌ تایید نشده"
        rejected_status = "❌ رد شده" if user_data.get('rejected') else "✅ فعال"
        
        created_time = user_data.get('created_at', time.time())
        time_diff = time.time() - created_time
        days = int(time_diff // 86400)
        hours = int((time_diff % 86400) // 3600)
        
        info_text = f"""
👤 **اطلاعات کاربر {target_id}**

📱 **شماره:** `{phone}`
📊 **وضعیت:** {status}
🔐 **احراز هویت:** {verified_status}
🚫 **وضعیت رد:** {rejected_status}
💰 **الماس ها:** `{credits}`
🔄 **سلف:** {running}
📅 **تاریخ ایجاد:** `{created}`
⏳ **عضو شده:** {days} روز و {hours} ساعت

⏱ **زمان باقی‌مانده:** `{credits}` ساعت
💸 **مصرف الماس:** 2 الماس در ساعت
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 تنظیم الماس", callback_data=f"set_{target_id}"),
             InlineKeyboardButton("🛑 توقف سلف", callback_data=f"stop_{target_id}")],
            [InlineKeyboardButton("✅ تایید احراز", callback_data=f"verify_approve_{target_id}"),
             InlineKeyboardButton("❌ رد احراز", callback_data=f"verify_reject_{target_id}")]
        ])
        
        await message.reply_text(info_text, reply_markup=keyboard)        
    except: 
        await message.reply_text("❌ آیدی باید عدد باشد")

@bot.on_message(filters.command("admin") & filters.user(ADMIN_ID))
async def admin_panel(client, message: Message):
    users = db.data.get("users", {})
    active_count = len(db.data.get("processes", {}))
    total_credits = sum(db.data.get("credits", {}).values())
    verified_users = len(db.get_verified_users())
    pending_verifications = len(db.get_pending_verifications())
    pending_payments = len(db.get_pending_payments())
    
    today = time.time() - 86400
    new_today = sum(1 for user_data in users.values() if user_data.get('created_at', 0) > today)
    
    stats_text = f"""
🛠 **پنل مدیریت ادمین**

👥 **کل کاربران:** `{len(users)}`
🟢 **کاربران فعال:** `{active_count}`
✅ **کاربران تایید شده:** `{verified_users}`
🆕 **کاربران امروز:** `{new_today}`
💰 **مجموع الماس ها:** `{total_credits}`

📋 **درخواست‌های در انتظار:**
├─ 🔐 احراز هویت: `{pending_verifications}`
└─ 💰 پرداخت: `{pending_payments}`

**📋 دستورات سریع:**
`/set آیدی تعداد` - تنظیم الماس
`/user آیدی` - اطلاعات کاربر
`/admin` - این پنل

💎 اقتصاد: {int(settings_value("self_activation_cost", SELF_ACTIVATION_COST))} الماس فعال‌سازی | {int(settings_value("self_hourly_cost", SELF_HOURLY_COST))} الماس/ساعت
💵 نرخ: هر 1000 الماس = {int(settings_value("diamond_to_toman", DIAMOND_TO_TOMAN)) * 1000:,} تومان
"""
    
    if ButtonStyle is None:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list"),
                InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top"),
                InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all")
            ],
            [
                InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications"),
                InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments")
            ],
            [
                InlineKeyboardButton("🔄 روشن کردن انتقال", callback_data="admin_transfer_on"),
                InlineKeyboardButton("⛔ خاموش کردن انتقال", callback_data="admin_transfer_off")
            ],
            [InlineKeyboardButton("⚙️ اقتصاد سلف", callback_data="admin_economy"), InlineKeyboardButton("📸 عکس شرط", callback_data="admin_set_bet_photo")],
            [InlineKeyboardButton("📢 پیام همگانی", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🎮 بازی‌های فعال", callback_data="admin_games")]
        ])
    else:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats", style=ButtonStyle.PRIMARY)
            ],
            [
                InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all", style=ButtonStyle.DANGER)
            ],
            [
                InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments", style=ButtonStyle.PRIMARY)
            ],
            [
                InlineKeyboardButton("🔄 روشن کردن انتقال", callback_data="admin_transfer_on", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("⛔ خاموش کردن انتقال", callback_data="admin_transfer_off", style=ButtonStyle.DANGER)
            ],
            [InlineKeyboardButton("⚙️ اقتصاد سلف", callback_data="admin_economy", style=ButtonStyle.PRIMARY), InlineKeyboardButton("📸 عکس شرط", callback_data="admin_set_bet_photo", style=ButtonStyle.PRIMARY)],
            [InlineKeyboardButton("📢 پیام همگانی", callback_data="admin_broadcast", style=ButtonStyle.PRIMARY)],
            [InlineKeyboardButton("🎮 بازی‌های فعال", callback_data="admin_games", style=ButtonStyle.SUCCESS)]
        ])
    
    await message.reply_text(stats_text, reply_markup=keyboard)

@bot.on_message(filters.command("panel") & filters.private)
async def owner_panel_command(client, message: Message):
    if not is_admin_user(message.from_user):
        await message.reply_text("❌ دسترسی غیرمجاز")
        return
    await admin_panel(client, message)

async def ttt_create_game(client, chat_id, user):
    gid=f"{chat_id}:{user.id}:{int(time.time()*1000)}"
    game={"chat_id":chat_id,"x_id":user.id,"x_name":user.first_name or "کاربر","o_id":None,"o_name":"","board":[None]*9,"turn":"X","winner":None,"created_at":time.time()}
    ttt_games[gid]=game
    db.set("games", gid, game)
    kb=InlineKeyboardMarkup([[InlineKeyboardButton("⭕ پیوستن به بازی", callback_data=f"ttt_join_{gid}")],[InlineKeyboardButton("❌ لغو", callback_data=f"ttt_cancel_{gid}")]])
    return await client.send_message(chat_id, f"🎮 <b>بازی دوز آنلاین ساخته شد!</b>\n\n❌ X: <a href=\"tg://user?id={user.id}\"><b>{html.escape(user.first_name or 'کاربر')}</b></a>\n⭕ O: منتظر بازیکن دوم...\n\nهرکس می‌خواهد بازی کند روی «پیوستن به بازی» بزند.", reply_markup=kb, parse_mode=enums.ParseMode.HTML)

@bot.on_message(filters.group & filters.regex(r'^دوز$'))
async def group_ttt_handler(client, message: Message):
    await ttt_create_game(client, message.chat.id, message.from_user)

async def phone_callback_handler(client, callback_query):
    uid=callback_query.from_user.id
    data=callback_query.data
    current=user_phone_digits.get(uid, "+98")
    if data == "phone_cancel":
        user_phone_digits.pop(uid, None)
        await callback_query.message.edit_text("❌ ورود شماره لغو شد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]]))
    elif data == "phone_clear":
        if len(current)>1: current=current[:-1]
        user_phone_digits[uid]=current
        await callback_query.message.edit_text(f"📱 <b>شماره:</b> <code>{current}</code>\n\nشماره را کامل کنید و تأیید بزنید.", reply_markup=phone_numpad_keyboard(), parse_mode=enums.ParseMode.HTML)
    elif data == "phone_plus":
        if not current.startswith("+"): current="+"+current
        user_phone_digits[uid]=current
    elif data == "phone_country_98":
        user_phone_digits[uid]="+98"
        await callback_query.message.edit_text("📱 <b>شماره:</b> <code>+98</code>\n\nشماره موبایل را ادامه دهید.", reply_markup=phone_numpad_keyboard(), parse_mode=enums.ParseMode.HTML)
    elif data == "phone_country_custom":
        user_phone_digits[uid]="+"
    elif data == "phone_send":
        phone=current
        if not phone.startswith("+") or not phone[1:].isdigit() or not (10 <= len(phone[1:]) <= 15):
            await callback_query.answer("❌ شماره کامل/صحیح نیست", show_alert=True)
            return
        await callback_query.answer("⏳ در حال ارسال کد...")
        user_phone_digits.pop(uid,None)
        await request_phone_code(client, uid, phone)
    elif data.startswith("phone_") and data.rsplit("_",1)[-1].isdigit():
        digit=data.rsplit("_",1)[-1]
        if len(current.replace("+","")) < 15:
            user_phone_digits[uid]=current+digit
        current=user_phone_digits[uid]
        await callback_query.message.edit_text(f"📱 <b>شماره:</b> <code>{current}</code>\n\nشماره را کامل کنید و تأیید بزنید.", reply_markup=phone_numpad_keyboard(), parse_mode=enums.ParseMode.HTML)
    await callback_query.answer()

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data.startswith("phone_"):
        await phone_callback_handler(client, callback_query)
        return

    if data == "ttt_menu":
        kb=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 ایجاد بازی دوز", callback_data="ttt_create")],
            [InlineKeyboardButton("📖 قوانین بازی", callback_data="ttt_rules")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ])
        await callback_query.message.edit_text("🎮 <b>دوز آنلاین</b>\n\nدو نفره و نوبتی، با دکمه‌های شیشه‌ای داخل تلگرام.\n\nبرای بازی جدید، «ایجاد بازی دوز» را بزنید.", reply_markup=kb, parse_mode=enums.ParseMode.HTML)
        await callback_query.answer()
        return
    if data == "ttt_rules":
        await callback_query.message.edit_text("📖 <b>قوانین دوز</b>\n\n❌ بازیکن X شروع می‌کند.\n⭕ بازیکن O بعد از او حرکت می‌کند.\n🏆 هرکس سه مهره پشت‌سرهم افقی، عمودی یا قطری بسازد برنده است.\n🤝 اگر خانه‌ها پر شوند و برنده‌ای نباشد، بازی مساوی است.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="ttt_menu")]]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return
    if data == "ttt_create":
        msg=await ttt_create_game(client, callback_query.message.chat.id if callback_query.message else user_id, callback_query.from_user)
        await callback_query.answer("🎮 بازی ساخته شد")
        return
    if data in {"gift_store","ai_info","referral","leaderboard","daily_challenge","transfer_info","about_self"}:
        a,h=self_costs(); rate=int(settings_value("diamond_to_toman", DIAMOND_TO_TOMAN)); credits=int(db.get("credits",user_id,0))
        if data=="gift_store":
            text="🎁 <b>فروشگاه گیفت</b>\n\nبرای خرید گیفت، موجودی الماس خود را شارژ کنید.\n\n💎 موجودی شما: <b>{:,}</b> الماس\n💰 نرخ: هر 1000 الماس = <b>15,000</b> تومان".format(credits)
            kb=[[InlineKeyboardButton("💰 شارژ حساب",callback_data="increase_balance")],[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        elif data=="ai_info":
            text="🤖 <b>دستیار هوش مصنوعی</b>\n\nاین بخش برای اتصال دستیار هوش مصنوعی به ربات آماده شده است.\n\n🔐 کلید API را فقط مالک می‌تواند از پنل مدیریت تنظیم کند."
            kb=[[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        elif data=="referral":
            me=await client.get_me(); link=f"https://t.me/{me.username}?start=ref_{user_id}" if me.username else "لینک رفرال پس از تنظیم username ربات ساخته می‌شود"
            text=f"👥 <b>زیرمجموعه‌گیری</b>\n\n🔗 لینک دعوت شما:\n<code>{html.escape(link)}</code>\n\n🎁 هر زیرمجموعه در سیستم ثبت می‌شود."
            kb=[[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        elif data=="leaderboard":
            rows=[]
            for uid,amount in sorted(db.get_all("credits").items(), key=lambda x:int(x[1]), reverse=True)[:10]:
                ud=db.get("users",int(uid),{}); name=html.escape(ud.get("first_name","کاربر"))
                rows.append(f"{len(rows)+1}. <b>{name}</b> — 💎 {int(amount):,}")
            text="🏆 <b>لیدربورد الماس</b>\n\n" + ("\n".join(rows) if rows else "هنوز داده‌ای ثبت نشده است.")
            kb=[[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        elif data=="daily_challenge":
            text="🎯 <b>چالش روزانه</b>\n\n🎡 چرخ شانس و چالش روزانه در این بخش قرار دارند.\n\n💎 هزینه فعال‌سازی سلف: <b>{}</b> الماس\n⏱ مصرف: <b>{}</b> الماس در ساعت\n💵 نرخ: هر 1000 الماس = <b>15,000</b> تومان".format(a,h)
            kb=[[InlineKeyboardButton("🎮 بازی دوز",callback_data="ttt_menu")],[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        elif data=="transfer_info":
            text="💎 <b>انتقال الماس</b>\n\nبرای انتقال در گروه بنویسید:\n<code>انتقال 100</code>\n\n⚠️ سیستم انتقال باید توسط مالک فعال باشد.\n💵 هر 1000 الماس معادل 15,000 تومان است."
            kb=[[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        else:
            text=f"❓ <b>سلف چیست؟</b>\n\n<b>{BOT_NAME}</b> یک پنل مدیریت سلف بات است.\n\n🟢 فعال‌سازی: <b>{a}</b> الماس\n⏱ مصرف: <b>{h}</b> الماس در ساعت\n💎 موجودی برای فعال بودن سلف به‌صورت خودکار هر ساعت کسر می‌شود.\n\nاگر موجودی به هزینه ساعتی نرسد، سلف خودکار خاموش می‌شود."
            kb=[[InlineKeyboardButton("🟢 فعال سازی سلف",callback_data="login")],[InlineKeyboardButton("🔙 بازگشت",callback_data="back")]]
        await callback_query.message.edit_text(text,reply_markup=InlineKeyboardMarkup(kb),parse_mode=enums.ParseMode.HTML)
        await callback_query.answer(); return

    if data.startswith("ttt_join_"):
        gid=data[len("ttt_join_"):]
        game=ttt_games.get(gid) or db.get("games",gid)
        if not game or game.get("winner") or game.get("o_id"):
            await callback_query.answer("❌ این بازی دیگر قابل پیوستن نیست.", show_alert=True); return
        if game["x_id"]==user_id:
            await callback_query.answer("ℹ️ شما سازنده بازی هستید.", show_alert=True); return
        game["o_id"]=user_id; game["o_name"]=callback_query.from_user.first_name or "کاربر"; ttt_games[gid]=game; db.set("games",gid,game)
        await callback_query.message.edit_text(ttt_text(game), reply_markup=ttt_keyboard(gid,game["board"]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer("⭕ وارد بازی شدید")
        return
    if data.startswith("ttt_move_"):
        parts=data.split("_"); gid="_".join(parts[2:-1]); idx=int(parts[-1])
        game=ttt_games.get(gid) or db.get("games",gid)
        if not game or not game.get("o_id"):
            await callback_query.answer("⏳ هنوز حریف وارد نشده است.", show_alert=True); return
        symbol="X" if user_id==game["x_id"] else "O" if user_id==game["o_id"] else None
        if not symbol:
            await callback_query.answer("❌ شما بازیکن این بازی نیستید.", show_alert=True); return
        if game.get("winner") or game["board"][idx] or game["turn"]!=symbol:
            await callback_query.answer("⏳ الان نوبت شما نیست یا این خانه پر است.", show_alert=True); return
        game["board"][idx]=symbol; result=ttt_winner(game["board"])
        if result: game["winner"]=result
        else: game["turn"]="O" if symbol=="X" else "X"
        ttt_games[gid]=game; db.set("games",gid,game)
        await callback_query.message.edit_text(ttt_text(game), reply_markup=ttt_keyboard(gid,game["board"]), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer("✅ حرکت ثبت شد")
        return
    if data.startswith("ttt_cancel_"):
        gid=data[len("ttt_cancel_"):]; game=ttt_games.get(gid) or db.get("games",gid)
        if game and user_id in (game.get("x_id"),game.get("o_id")):
            game["winner"]="CANCEL"; db.set("games",gid,game); ttt_games.pop(gid,None)
            await callback_query.message.edit_text("❌ بازی دوز لغو شد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 بازی جدید", callback_data="ttt_menu")]]))
        else: await callback_query.answer("❌ فقط بازیکنان بازی می‌توانند لغو کنند.", show_alert=True)
        return

    if data.startswith("joinbet_"):
        if data == "joinbet_waiting":
            await callback_query.answer("⏳ لطفا چند لحظه صبر کنید...", show_alert=True)
            return
        await join_group_bet_handler(client, callback_query)
        return
    
    if data.startswith("cancelbet_"):
        if data == "cancelbet_waiting":
            await callback_query.answer("⏳ لطفا چند لحظه صبر کنید...", show_alert=True)
            return
        await cancel_group_bet_handler(client, callback_query)
        return
    
    if data.startswith(("admin_", "set_", "stop_", "verify_", "payment_")):
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
        await admin_callback_handler(client, callback_query)
        return
    
    if data == "admin_panel":
        if not is_admin_user(callback_query.from_user):
            await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
            return
        await admin_panel(client, callback_query.message)
        await callback_query.answer()
        return
    
    if data == "back":
        await send_main_menu(client, user_id, user_id, callback_query.message)
        await callback_query.answer()
        return
    if data == "login":
        activation_cost, hourly_cost = self_costs()
        credits = db.get("credits", user_id, 0)
        if credits < activation_cost:
            text = (f"❌ <b>موجودی کافی نیست</b>\n\n"
                    f"💎 هزینه فعال‌سازی سلف: <b>{activation_cost}</b> الماس\n"
                    f"💎 موجودی شما: <b>{credits}</b> الماس\n"
                    f"⏱ مصرف بعد از فعال‌سازی: <b>{hourly_cost}</b> الماس در ساعت")
            keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("💰 شارژ حساب", callback_data="increase_balance")],[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
            await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
            await callback_query.answer()
            return
        user_phone_digits[user_id]="+98"
        text=("📱 <b>شماره تلگرام را وارد کنید</b>\n\n"
              "🇮🇷 پیش‌شماره پیش‌فرض: <code>+98</code>\n"
              f"💎 هزینه فعال‌سازی: <b>{activation_cost}</b> الماس\n"
              "⌨️ شماره را با کد کشور کامل کنید و «تأیید شماره» را بزنید.")
        await callback_query.message.edit_text(text, reply_markup=phone_numpad_keyboard(), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer()

    elif data == "login_again":
        user_phone_digits[user_id]="+98"
        await callback_query.message.edit_text(
            "📱 <b>شماره تلفن جدید را وارد کنید</b>\n\n🇮🇷 <code>+98</code> پیش‌فرض است.",
            reply_markup=phone_numpad_keyboard(), parse_mode=enums.ParseMode.HTML)
        await callback_query.answer()

    elif data == "status_credits":
        user_data=db.get("users", user_id, {})
        credits=int(db.get("credits", user_id, 0))
        active=check_selfbot_status(user_id)
        a,h=self_costs(); rate=int(settings_value("diamond_to_toman", DIAMOND_TO_TOMAN))
        equivalent=credits*rate
        status="🟢 فعال" if active else "🔴 غیرفعال"
        text=(f"💎 <b>موجودی حساب شما</b>\n\n"
              f"💎 <b>{credits:,} الماس</b>\n"
              f"💵 معادل تقریبی: <b>{equivalent:,} تومان</b>\n"
              f"⚡ وضعیت سلف: <b>{status}</b>\n"
              f"⏱ مصرف سلف: <b>{h}</b> الماس در ساعت\n"
              f"🔐 هزینه فعال‌سازی: <b>{a}</b> الماس\n"
              f"📱 شماره: <code>{html.escape(user_data.get('phone','ثبت نشده'))}</code>")
        keyboard=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💎 {credits:,} الماس", callback_data="my_balance", style=ButtonStyle.PRIMARY) if ButtonStyle else InlineKeyboardButton(f"💎 {credits:,} الماس", callback_data="my_balance")],
            [InlineKeyboardButton(f"💰 معادل {equivalent:,} تومان", callback_data="my_balance", style=ButtonStyle.PRIMARY) if ButtonStyle else InlineKeyboardButton(f"💰 معادل {equivalent:,} تومان", callback_data="my_balance")],
            [InlineKeyboardButton("💰 شارژ حساب", callback_data="increase_balance", style=ButtonStyle.SUCCESS) if ButtonStyle else InlineKeyboardButton("💰 شارژ حساب", callback_data="increase_balance")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back", style=ButtonStyle.DANGER) if ButtonStyle else InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ])
        photo_id=db.get_welcome_photo()
        if photo_id and not getattr(callback_query.message,"photo",None):
            await callback_query.message.delete()
            await client.send_photo(user_id, photo_id, caption=text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        elif getattr(callback_query.message,"photo",None):
            await callback_query.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        else:
            await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        await callback_query.answer()

    elif data == "bet":
        info_text = """
🎲 **سیستم شرطبندی گروهی 1v1**

**📋 قوانین شرطبندی:**
1️⃣ در گروه با نوشتن `شرطبندی 100` (یا هر مقدار دیگر) می‌توانید شرط ایجاد کنید
2️⃣ نفر دوم می‌تواند با کلیک روی دکمه «پیوستن به شرط» وارد شود
3️⃣ پس از پیوستن نفر دوم، ۵ ثانیه بعد برنده مشخص می‌شود
4️⃣ برنده تمام مبلغ شرط را دریافت می‌کند
5️⃣ اگر در ۵ دقیقه کسی شرکت نکند، شرط لغو و مبلغ بازگردانده می‌شود

**💰 مثال:**
- شما: `شرطبندی 500`
- حریف: پیوستن به شرط
- برنده: تمام 1000 الماس را می‌برد (500+500)
    """
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ])
    
        photo_id = db.get_welcome_photo()
        if photo_id:
            if callback_query.message.photo:
                await callback_query.message.edit_caption(
                    caption=info_text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await callback_query.message.delete()
                await client.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=info_text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            await callback_query.message.edit_text(
                info_text,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        await callback_query.answer()
    
    elif data == "self_management":
        user_data = db.get("users", user_id, {})
        credits = db.get("credits", user_id, 0)

        is_active = check_selfbot_status(user_id)
        process = db.get("processes", user_id)
    
        if is_active and user_data.get('status') != 'active':
            user_data["status"] = "active"
            db.set("users", user_id, user_data)
        elif not is_active and user_data.get('status') == 'active':
            user_data["status"] = "inactive"
            db.set("users", user_id, user_data)
    
        status_text = "🟢 <b>فعال</b>" if is_active and process else "🔴 <b>غیرفعال</b>"
    
        if ButtonStyle is None:
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start"),
                    InlineKeyboardButton("⏹ خاموش کردن سلف", callback_data="self_stop")
                ],
                [
                    InlineKeyboardButton("🔄 آپدیت سلف", callback_data="self_update")
                ],
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="back")
                ]
            ])
        else:
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start", style=ButtonStyle.SUCCESS),
                    InlineKeyboardButton("⏹ خاموش کردن سلف", callback_data="self_stop", style=ButtonStyle.DANGER)
                ],
                [
                    InlineKeyboardButton("🔄 آپدیت سلف", callback_data="self_update", style=ButtonStyle.PRIMARY)
                ],
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="back", style=ButtonStyle.DANGER)
                ]
            ])
    
        text = (
            f"⚙️ <b>مدیریت سلف بات</b>\n\n"
            f"📊 <b>وضعیت فعلی:</b> {status_text}\n"
            f"💰 <b>الماس ها:</b> <code>{credits}</code>\n\n"
            f"🔹 <b>روشن کردن:</b> سلف بات را فعال می‌کند\n"
            f"🔹 <b>خاموش کردن:</b> سلف بات را متوقف می‌کند\n"
            f"🔹 <b>آپدیت سلف:</b> سلف بات را مجدداً راه‌اندازی می‌کند\n\n"
            f"📱 <b>شماره:</b> <code>{user_data.get('phone', 'ثبت نشده')}</code>"
        )
    
        photo_id = db.get_welcome_photo()
        if photo_id:
            if callback_query.message.photo:
                await callback_query.message.edit_caption(
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await callback_query.message.delete()
                await client.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            await callback_query.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        await callback_query.answer()
    
    elif data == "self_start":
        user_data = db.get("users", user_id, {})
        credits = db.get("credits", user_id, 0)
    
        activation_cost, hourly_cost = self_costs()
        if credits < activation_cost:
            await callback_query.message.edit_text(
                f"❌ <b>الماس کافی ندارید!</b>\n\n"
                f"💎 هزینه فعال‌سازی: <code>{activation_cost}</code> الماس\n"
                f"💎 موجودی شما: <code>{credits}</code> الماس\n\n"
            "💡 لطفا ابتدا موجودی خود را افزایش دهید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("💰 افزایش موجودی", callback_data="increase_balance")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
            return
    
        if not user_data.get('phone'):
            await callback_query.message.edit_text(
                "❌ <b>شماره تلفن ثبت نشده است!</b>\n\n"
            "لطفا ابتدا از طریق دکمه «فعالسازی» شماره خود را ثبت کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("● فعالسازی ●", callback_data="login")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ])
            )
            return
    
        if db.get("processes", user_id):
            await callback_query.message.edit_text(
                "ℹ️ <b>سلف بات در حال حاضر فعال است!</b>\n\n"
            "برای راه‌اندازی مجدد از گزینه «آپدیت سلف» استفاده کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🔄 آپدیت سلف", callback_data="self_update")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ])
            )
            return
    
        db.set("credits", user_id, credits - activation_cost)
        if run_selfbot(user_id, user_data.get('phone')):
            credits = db.get("credits", user_id, 0)
            await callback_query.message.edit_text(
                f"✅ <b>سلف بات با موفقیت روشن شد!</b>\n\n"
                f"💰 <b>الماس باقی‌مانده:</b> <code>{credits}</code>\n"
                f"⏰ <b>زمان باقی‌مانده:</b> <code>{credits}</code> ساعت\n\n"
                f"📱 <b>شماره:</b> <code>{user_data.get('phone')}</code>",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")
                    ]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            db.set("credits", user_id, credits)
            await callback_query.message.edit_text(
                "❌ <b>خطا در روشن کردن سلف بات!</b>\n\n"
            "لطفا دوباره تلاش کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🔄 تلاش مجدد", callback_data="self_start")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ])
            )
        await callback_query.answer()
    
    elif data == "self_stop":
        if stop_selfbot(user_id):
            await callback_query.message.edit_text(
                "✅ <b>سلف بات با موفقیت خاموش شد!</b>\n\n"
            "برای روشن کردن مجدد از گزینه «روشن کردن سلف» استفاده کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")
                    ]
                ])
            )
        else:
            await callback_query.message.edit_text(
                "ℹ️ <b>سلف بات در حال حاضر خاموش است!</b>\n\n"
            "برای روشن کردن از گزینه «روشن کردن سلف» استفاده کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")
                    ]
                ])
            )
        await callback_query.answer()
    
    elif data == "self_update":
        user_data = db.get("users", user_id, {})
        credits = db.get("credits", user_id, 0)
        
        if credits <= 0:
            await callback_query.message.edit_text(
                f"❌ <b>الماس کافی ندارید!</b>\n\n"
                f"💰 الماس های شما: <code>{credits}</code>\n\n"
                "💡 لطفا ابتدا موجودی خود را افزایش دهید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("💰 افزایش موجودی", callback_data="increase_balance")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        if not user_data.get('phone'):
            await callback_query.message.edit_text(
                "❌ <b>شماره تلفن ثبت نشده است!</b>\n\n"
                "لطفا ابتدا از طریق دکمه «فعالسازی» شماره خود را ثبت کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("● فعالسازی ●", callback_data="login")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ])
            )
            return
        
        await callback_query.message.edit_text(
            "🔄 <b>در حال آپدیت سلف بات...</b>\n\n"
            "لطفا چند لحظه صبر کنید...",
            reply_markup=None
        )
        
        stop_selfbot(user_id)
        await asyncio.sleep(1)
        
        if run_selfbot(user_id, user_data.get('phone')):
            credits = db.get("credits", user_id, 0)
            await callback_query.message.edit_text(
                f"✅ <b>سلف بات با موفقیت آپدیت شد!</b>\n\n"
                f"💰 <b>الماس باقی‌مانده:</b> <code>{credits}</code>\n"
                f"⏰ <b>زمان باقی‌مانده:</b> <code>{credits}</code> ساعت\n\n"
                f"📱 <b>شماره:</b> <code>{user_data.get('phone')}</code>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")]
                ]),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await callback_query.message.edit_text(
                "❌ <b>خطا در آپدیت سلف بات!</b>\n\n"
                "لطفا دوباره تلاش کنید.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🔄 تلاش مجدد", callback_data="self_update")
                    ],
                    [
                        InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")
                    ]
                ])
            )
        await callback_query.answer()
    
    elif data == "increase_balance":
        user_data = db.get("users", user_id, {})
    
        if user_data.get('rejected'):
            await callback_query.answer("❌ حساب شما توسط ادمین رد شده است.", show_alert=True)
            return
    
        if not user_data.get('verified'):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("● احراز هویت ●", callback_data="start_verification")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
            ])
        
            text = (
            "🔒 **برای افزایش موجودی نیاز به احراز هویت دارید**\n\n"
            "📋 **مراحل احراز هویت:**\n"
            "1️⃣ کلیک روی دکمه 'احراز هویت'\n"
            "2️⃣ ارسال عکس از کارت بانکی\n"
            "3️⃣ تایید توسط ادمین\n"
            "4️⃣ افزایش موجودی\n\n"
            "⚠️ **توجه:** اطلاعات حساس (CVV2، تاریخ انقضا) در عکس پوشیده شود"
            )
        
            photo_id = db.get_welcome_photo()
            if photo_id:
                if callback_query.message.photo:
                    await callback_query.message.edit_caption(
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode=enums.ParseMode.HTML
                    )
                else:
                    await callback_query.message.delete()
                    await client.send_photo(
                        chat_id=user_id,
                        photo=photo_id,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                await callback_query.message.edit_text(
                    text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            return
    
        text = (
            f"💰 **افزایش موجودی**\n\n"
            f"💎 **نرخ تبدیل:** هر {COIN_RATE} الماس = 15,000 تومان\n"
            f"💵 **قیمت هر الماس:** {TOMAN_PER_COIN:.0f} تومان\n\n"
        "🔢 **تعداد الماس مورد نظر خود را وارد کنید:**\n"
        "مثال: 1000\n\n"
        "💡 **توجه:** فقط عدد وارد کنید (بدون نقطه یا کاما)"
        )
    
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
    
        photo_id = db.get_welcome_photo()
        if photo_id:
            if callback_query.message.photo:
                await callback_query.message.edit_caption(
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await callback_query.message.delete()
                await client.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            await callback_query.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
    
        db.delete("temp_data", f"waiting_coins_{user_id}")
        db.set("temp_data", f"waiting_coins_{user_id}", True)
        await callback_query.answer("✅ لطفا تعداد الماس مورد نظر را وارد کنید")

    elif data == "start_verification":
        user_data = db.get("users", user_id, {})
        if user_data.get('rejected'):
            await callback_query.answer("❌ حساب شما توسط ادمین رد شده است.", show_alert=True)
            return
    
        text = (
            "📸 <b>لطفا عکس کارت بانکی خود را ارسال کنید</b>\n\n"
            "⚠️ <b>قبل از ارسال مطمئن شوید:</b>\n"
        "• نام صاحب کارت مشخص باشد\n"
        "• شماره کارت واضح باشد\n"
        "• CVV2 ❌ پوشیده شود\n"
        "• تاریخ انقضا ❌ پوشیده شود\n\n"
        "📎 یک عکس با کیفیت مناسب ارسال کنید"
        )
    
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="increase_balance")]
        ])
    
        photo_id = db.get_welcome_photo()
        if photo_id:
            if callback_query.message.photo:
                await callback_query.message.edit_caption(
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await callback_query.message.delete()
                await client.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            await callback_query.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
    
        db.set("temp_data", f"waiting_card_photo_{user_id}", True)
    
    elif data == "check_join":
        ok, not_joined = await check_force_join(client, user_id)
        if ok:
            await callback_query.message.edit_text("✅ عضویت شما در همه کانال‌ها تایید شد!\nدوباره /start بزنید.")
            return
        buttons = []
        for ch in not_joined:
            buttons.append([
                InlineKeyboardButton(
                    f"📢 عضویت در @{ch}", 
                    url=f"https://t.me/{ch}"
                )
            ])
        buttons.append([
            InlineKeyboardButton(
                "🔄 بررسی مجدد", 
                callback_data="check_join"
            )
        ])

        await callback_query.message.edit_text(
    "❌ هنوز عضو همه کانال‌ها نیستید!",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await callback_query.answer()

@bot.on_message(filters.user(ADMIN_ID) & filters.regex(r'^\d+$'))
async def handle_admin_input(client, message: Message):
    user_id = message.from_user.id
    amount = int(message.text)
    
    set_target = db.get("temp_data", f"admin_set_{user_id}")
    if set_target:
        db.delete("temp_data", f"admin_set_{user_id}")
        db.set("credits", set_target, amount)
        
        await message.reply_text(f"✅ الماس کاربر {set_target} تنظیم شد به {amount}")
        
        try:
            await bot.send_message(set_target, f"🔧 موجودی الماس شما تنظیم شد\n💰 جدید: {amount} الماس")
        except: pass

@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    global ADMIN_ID
    if (message.from_user.username or "").lower() == ADMIN_USERNAME.lower():
        ADMIN_ID = message.from_user.id
    ok, not_joined = await check_force_join(client, message.from_user.id)
    if not ok:
        buttons = [[InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")] for ch in not_joined]
        buttons.append([InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check_join")])
        await message.reply_text("❌ برای استفاده از ربات باید در تمام کانال‌های زیر عضو شوید:", reply_markup=InlineKeyboardMarkup(buttons))
        return
    user_id=message.from_user.id
    existing_user=db.get("users", user_id)
    if not existing_user:
        db.set("users", user_id, {
            "status":"inactive", "created_at":time.time(),
            "first_name":message.from_user.first_name or "", "username":message.from_user.username or "",
            "verified":False, "rejected":False
        })
        if db.get("credits", user_id, None) is None:
            db.set("credits", user_id, 0)
    else:
        existing_user["first_name"]=message.from_user.first_name or ""
        existing_user["username"]=message.from_user.username or ""
        db.set("users", user_id, existing_user)
    await send_main_menu(client, message.chat.id, user_id)

@bot.on_callback_query(filters.regex(r'^joinbet_(-?\d+)_(-?\d+)$'))
async def join_group_bet_handler(client, callback_query):
    user_id = callback_query.from_user.id
    user_first_name = html.escape(callback_query.from_user.first_name or 'کاربر')
    user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
    data = callback_query.data
    _, chat_id_str, msg_id_str = data.split('_')

    chat_id = int(chat_id_str)
    message_id = int(msg_id_str)
    bet_key = f"{chat_id}_{message_id}"

    bet_data = db.get("group_bets", bet_key)
    if not bet_data or not bet_data.get("is_active"):
        await callback_query.answer("❌ این شرط دیگر فعال نیست.", show_alert=True)
        return

    if bet_data.get("finished"):
        await callback_query.answer("❌ این شرط قبلا به پایان رسیده است.", show_alert=True)
        return
    
    if callback_query.message.chat.id != chat_id:
        await callback_query.answer("❌ این دکمه مخصوص گروه اصلی شرط است.", show_alert=True)
        return

    creator_id = bet_data["creator_id"]
    creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
    creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
    participants = bet_data.get("participants", [])
    
    if user_id == creator_id:
        await callback_query.answer("ℹ️ شما سازنده این شرط هستید و قبلاً داخل شرط هستید.", show_alert=True)
        return
    
    if len(participants) >= 1:
        await callback_query.answer("⛔ ظرفیت این شرط تکمیل شده است.", show_alert=True)
        return

    if user_id in [p["id"] for p in participants]:
        await callback_query.answer("ℹ️ شما قبلا در این شرط شرکت کرده‌اید.", show_alert=True)
        return

    amount = bet_data["amount"]
    current_credits = db.get("credits", user_id, 0)

    if current_credits < amount:
        await callback_query.answer(
            f"❌ الماس کافی ندارید!\n💰 موجودی شما: {current_credits} الماس",
            show_alert=True
        )
        return
    
    db.set("credits", user_id, current_credits - amount)

    participants.append({
        "id": user_id,
        "name": callback_query.from_user.first_name or "",
        "username": callback_query.from_user.username or ""
    })
    bet_data["participants"] = participants
    
    try:
        participants_mentions = []
        for p in participants:
            p_name = html.escape(p.get('name', 'کاربر'))
            participants_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
        
        all_players_mentions = [creator_mention] + participants_mentions
        waiting_text = (
            "⏳ <b>در حال قرعه‌کشی...</b>\n\n"
            f"💰 <b>مبلغ هر نفر:</b> <code>{amount}</code> الماس\n"
            f"👥 <b>شرکت‌کننده‌ها:</b> <code>{len(participants) + 1}/2</code> نفر\n"
            f"👤 <b>بازیکنان:</b> {', '.join(all_players_mentions)}\n\n"
            "🔄 ۵ ثانیه دیگر برنده مشخص می‌شود..."
        )
        await callback_query.message.edit_text(
            waiting_text,
            reply_markup=None, 
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"Error updating bet message: {e}")
    if not bet_data.get("timer_started"):
        bet_data["timer_started"] = True
        db.set("group_bets", bet_key, bet_data)
        asyncio.create_task(finish_group_bet(client, bet_key))
    else:
        db.set("group_bets", bet_key, bet_data)

    await callback_query.answer("✅ در شرط شرکت کردید و الماس از حساب شما کسر شد.")

@bot.on_callback_query(filters.regex(r'^cancelbet_(-?\d+)_(-?\d+)$'))
async def cancel_group_bet_handler(client, callback_query):
    user_id = callback_query.from_user.id
    user_first_name = html.escape(callback_query.from_user.first_name or 'کاربر')
    user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
    data = callback_query.data
    _, chat_id_str, msg_id_str = data.split('_')

    chat_id = int(chat_id_str)
    message_id = int(msg_id_str)
    bet_key = f"{chat_id}_{message_id}"

    bet_data = db.get("group_bets", bet_key)
    if not bet_data:
        await callback_query.answer("❌ این شرط یافت نشد یا قبلا حذف شده.", show_alert=True)
        return

    creator_id = bet_data["creator_id"]
    creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
    creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'

    if user_id != creator_id:
        await callback_query.answer("❌ فقط سازنده شرط می‌تواند آن را لغو کند.", show_alert=True)
        return

    if bet_data.get("finished"):
        await callback_query.answer("❌ این شرط قبلا تمام شده است.", show_alert=True)
        return

    amount = bet_data["amount"]
    participants = bet_data.get("participants", [])
    if not bet_data.get("refunded"):
        creator_credits = db.get("credits", creator_id, 0)
        db.set("credits", creator_id, creator_credits + amount)
        bet_data["refunded"] = True
    for participant in participants:
        uid = participant["id"]
        credits = db.get("credits", uid, 0)
        db.set("credits", uid, credits + amount)

    bet_data["finished"] = True
    bet_data["is_active"] = False
    db.set("group_bets", bet_key, bet_data)

    participants_mentions = []
    for p in participants:
        p_name = html.escape(p.get('name', 'کاربر'))
        participants_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
    
    all_users_text = creator_mention
    if participants_mentions:
        all_users_text += f", {', '.join(participants_mentions)}"

    text = (
        "⛔ این شرط توسط سازنده لغو شد.\n\n"
        f"👤 سازنده: {creator_mention}\n"
        f"👥 سایر بازیکنان: {', '.join(participants_mentions) if participants_mentions else 'ندارد'}\n"
        f"💰 مبلغ شرط: <code>{amount}</code> الماس\n"
        "💸 مبلغ به تمام افراد (سازنده و شرکت‌کننده‌ها) برگشت داده شد."
    )

    try:
        await callback_query.message.edit_text(text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
    except:
        pass

    await callback_query.answer("✅ شرط با موفقیت لغو شد.", show_alert=True)

@bot.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):
    user_id = callback_query.from_user.id
    ok, not_joined = await check_force_join(client, user_id)

    if ok:
        await callback_query.message.edit_text("✅ عضویت شما در همه کانال‌ها تایید شد!\nدوباره /start بزنید.")
        return

    buttons = []
    for ch in not_joined:
        buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])

    buttons.append([InlineKeyboardButton("🔄 بررسی مجدد", callback_data="check_join")])

    await callback_query.message.edit_text(
        "❌ هنوز عضو همه کانال‌ها نیستید!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_message(filters.private & filters.regex(r'^\+\d{10,15}$'))
async def handle_phone(client, message: Message):
    user_id, phone = message.from_user.id, message.text
    
    if user_id in active_clients:
        try:
            await active_clients[user_id].disconnect()
            del active_clients[user_id]
        except:
            pass
    
    credits = db.get("credits", user_id, 0)
    activation_cost, _hourly_cost = self_costs()
    if credits < activation_cost:
        await message.reply_text(f"❌ الماس کافی ندارید!\n💎 هزینه فعال‌سازی: {activation_cost}\n💎 موجودی شما: {credits}")
        return
    
    try:
        session_name = f"sessions/{user_id}"
        temp_client = Client(session_name, api_id=API_ID, api_hash=API_HASH)
        await temp_client.connect()
        
        active_clients[user_id] = temp_client
        sent_code = await temp_client.send_code(phone)
        user_data = db.get("users", user_id, {})
        user_data["phone"] = phone
        db.set("users", user_id, user_data)
        await message.reply_text(
            "✅ **کد تأیید ارسال شد**\n\n"
            "🔢 **کد ۵ رقمی را با دکمه‌های زیر وارد کنید:**\n\n"
            f"<b><code>{format_code_display('')}</code></b>\n\n"
            "📱 کد ارسال شده به شماره شما",
            reply_markup=create_numpad_keyboard(),
            parse_mode=enums.ParseMode.HTML
        )
        
        db.set("temp_data", user_id, {
            "phone": phone,
            "phone_code_hash": sent_code.phone_code_hash,
            "client_active": True,
            "activation_pending": True
        })
        
    except Exception as e:
        await message.reply_text(f"❌ **خطا:** {str(e)}")
        if user_id in active_clients:
            try:
                await active_clients[user_id].disconnect()
                del active_clients[user_id]
            except:
                pass

@bot.on_message(filters.private & filters.photo)
async def handle_photo_messages(client, message: Message):
    user_id = message.from_user.id
    
    if is_admin_user(message.from_user):
        if db.get("temp_data", f"admin_waiting_bet_photo_{user_id}"):
            photo_id = message.photo.file_id
            db.set("settings", BET_PHOTO_SETTING, photo_id)
            db.delete("temp_data", f"admin_waiting_bet_photo_{user_id}")
            await message.reply_photo(photo=photo_id, caption="✅ عکس شرط‌بندی با موفقیت ذخیره شد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 پنل مدیریت", callback_data="admin_panel")]]))
            return
        
        if db.get("temp_data", f"admin_waiting_photo_{user_id}"):
            photo_id = message.photo.file_id
            db.set_welcome_photo(photo_id)
            db.delete("temp_data", f"admin_waiting_photo_{user_id}")
            await message.reply_photo(photo=photo_id, caption="✅ عکس خوش‌آمدگویی با موفقیت تنظیم شد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 پنل مدیریت", callback_data="admin_panel")]]))
            return
    
    if db.get("temp_data", f"waiting_card_photo_{user_id}"):
        verification_data = {
            "user_id": user_id,
            "first_name": message.from_user.first_name or "",
            "username": message.from_user.username or "",
            "photo_id": message.photo.file_id,
            "timestamp": time.time(),
            "status": "pending"
        }
        
        db.set("verifications", user_id, verification_data)
        db.delete("temp_data", f"waiting_card_photo_{user_id}")
        
        admin_text = f"🆕 **درخواست احراز هویت جدید**\n\n"
        admin_text += f"👤 **کاربر:** {verification_data['first_name']}\n"
        admin_text += f"🆔 **آیدی:** `{user_id}`\n"
        admin_text += f"📧 **یوزرنیم:** @{verification_data['username']}\n"
        admin_text += f"⏰ **زمان:** {time.ctime()}"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ تایید", callback_data=f"verify_approve_{user_id}"),
                InlineKeyboardButton("❌ رد", callback_data=f"verify_reject_{user_id}")
            ]
        ])
        
        try:
            await message.forward(ADMIN_ID)
            await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
            
            text = (
                "✅ **عکس شما دریافت شد و برای تایید به ادمین ارسال شد**\n\n"
                "⏳ لطفا منتظر تایید ادمین باشید\n"
                "🔔 پس از تایید به شما اطلاع داده خواهد شد"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
            ])
            
            photo_id = db.get_welcome_photo()
            if photo_id:
                await message.reply_photo(
                    photo=photo_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await message.reply_text(
                    text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
        except Exception as e:
            await message.reply_text("❌ خطا در ارسال به ادمین. لطفا بعدا تلاش کنید.")
        return
    
    elif db.get("temp_data", f"waiting_payment_proof_{user_id}"):
        payment_data = db.get("payments", user_id)
        if not payment_data:
            await message.reply_text("❌ اطلاعات پرداخت یافت نشد. لطفا دوباره تلاش کنید.")
            return
        
        payment_data["proof_photo_id"] = message.photo.file_id
        payment_data["proof_sent_at"] = time.time()
        db.set("payments", user_id, payment_data)
        
        admin_text = (
            f"💰 **درخواست افزایش موجودی جدید**\n\n"
            f"👤 **کاربر:** {message.from_user.first_name or 'ناشناس'}\n"
            f"🆔 **آیدی:** `{user_id}`\n"
            f"📧 **یوزرنیم:** @{message.from_user.username or 'ندارد'}\n"
            f"💎 **تعداد الماس:** {payment_data['coins']}\n"
            f"💵 **مبلغ:** {payment_data['toman']:,.0f} تومان\n"
            f"⏰ **زمان:** {time.ctime()}"
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ تایید پرداخت", callback_data=f"payment_approve_{user_id}"),
                InlineKeyboardButton("❌ رد پرداخت", callback_data=f"payment_reject_{user_id}")
            ]
        ])
        
        try:
            await message.forward(ADMIN_ID)
            await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
            
            text = (
                "✅ **رسید پرداخت شما دریافت شد و برای تایید به ادمین ارسال شد**\n\n"
                "⏳ لطفا منتظر تایید ادمین باشید\n"
                "🔔 پس از تایید، الماس ها به حساب شما اضافه خواهد شد"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
            ])
            
            photo_id = db.get_welcome_photo()
            if photo_id:
                await message.reply_photo(
                    photo=photo_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await message.reply_text(
                    text,
                    reply_markup=keyboard,
                    parse_mode=enums.ParseMode.HTML
                )
            
            db.delete("temp_data", f"waiting_payment_proof_{user_id}")
            
        except Exception as e:
            await message.reply_text("❌ خطا در ارسال به ادمین. لطفا بعدا تلاش کنید.")
        return

@bot.on_message(filters.private & filters.text)
async def handle_text_messages(client, message: Message):
    user_id = message.from_user.id
    text = message.text
    
    if db.get("temp_data", f"waiting_coins_{user_id}"):
        try:
            coins_amount = int(text)
            if coins_amount <= 0:
                await message.reply_text("❌ تعداد الماس باید بیشتر از صفر باشد")
                return
            
            toman_amount = coins_amount * TOMAN_PER_COIN
            
            payment_data = {
                "user_id": user_id,
                "coins": coins_amount,
                "toman": toman_amount,
                "timestamp": time.time(),
                "status": "pending",
                "first_name": message.from_user.first_name or "",
                "username": message.from_user.username or ""
            }
            
            db.set("payments", user_id, payment_data)
            db.delete("temp_data", f"waiting_coins_{user_id}")
            
            payment_text = (
                f"💳 **برای پرداخت لطفا مبلغ {toman_amount:,.0f} تومان به حساب زیر واریز کنید:**\n\n"
                f"🏦 **بانک:** {card_info['bank_name']}\n"
                f"🔢 **شماره کارت:** `{card_info['card_number']}`\n"
                f"👤 **به نام:** {card_info['card_owner']}\n\n"
                f"💎 **تعداد الماس دریافتی:** {coins_amount} الماس\n\n"
                f"📸 **پس از واریز، رسید یا عکس پرداخت را ارسال کنید**\n"
                f"⏰ پرداخت شما حداکثر تا 24 ساعت بررسی خواهد شد"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔙 انصراف", callback_data="increase_balance")
                ]
            ])
            
            await message.reply_text(payment_text, reply_markup=keyboard)
            db.set("temp_data", f"waiting_payment_proof_{user_id}", True)
            
        except ValueError:
            await message.reply_text("❌ لطفا یک عدد معتبر وارد کنید")
        return

    temp_data = db.get("temp_data", user_id)
    if temp_data and temp_data.get("needs_password"):
        try:
            if user_id not in active_clients:
                await message.reply_text("❌ کلاینت فعال نیست. لطفا دوباره شماره را ارسال کنید.")
                return
            
            user_client = active_clients[user_id]
            await user_client.check_password(text)
            
            user_info = {
                "phone": temp_data["phone"],
                "status": "active",
                "created_at": time.time(),
                "last_active": time.time(),
                "verified": db.get("users", user_id, {}).get("verified", False)
            }
            db.set("users", user_id, user_info)
            db.delete("temp_data", user_id)
            
            if user_id in active_clients:
                try:
                    await active_clients[user_id].disconnect()
                    del active_clients[user_id]
                except:
                    pass
            
            await activate_self_after_auth(client, user_id, temp_data["phone"], success_message=True)
            
        except Exception as e: 
            await message.reply_text(f"❌ رمز اشتباه: {str(e)}")
        return

    if is_admin_user(message.from_user):
        set_target = db.get("temp_data", f"admin_set_{user_id}")
        if set_target and text.isdigit():
            amount = int(text)
            db.delete("temp_data", f"admin_set_{user_id}")
            db.set("credits", set_target, amount)
            await message.reply_text(f"✅ الماس کاربر {set_target} تنظیم شد به {amount}")
            try:
                await bot.send_message(set_target, f"🔧 موجودی الماس شما تنظیم شد\n💎 جدید: {amount} الماس")
            except: pass
            return

        if db.get("temp_data", f"admin_economy_{user_id}"):
            parts=text.replace("،"," ").split()
            if len(parts)==3 and all(x.isdigit() for x in parts):
                a,h,rate=map(int,parts)
                if a>0 and h>0 and rate>0:
                    db.set("settings","self_activation_cost",a); db.set("settings","self_hourly_cost",h); db.set("settings","diamond_to_toman",rate)
                    db.delete("temp_data", f"admin_economy_{user_id}")
                    await message.reply_text(f"✅ تنظیمات اقتصاد ذخیره شد.\n💎 فعال‌سازی: {a}\n⏱ ساعتی: {h}\n💵 هر الماس: {rate} تومان")
                else: await message.reply_text("❌ مقادیر باید بیشتر از صفر باشند.")
            else: await message.reply_text("❌ فرمت صحیح: <code>30 2 15</code>", parse_mode=enums.ParseMode.HTML)
            return

        if db.get("temp_data", f"admin_broadcast_{user_id}"):
            db.delete("temp_data", f"admin_broadcast_{user_id}")
            sent=failed=0
            for uid in db.get_all("users"):
                try:
                    await client.send_message(int(uid), f"📢 <b>اطلاعیه {BOT_NAME}</b>\n\n{html.escape(text)}", parse_mode=enums.ParseMode.HTML)
                    sent+=1
                except Exception: failed+=1
            await message.reply_text(f"✅ پیام همگانی ارسال شد.\n📨 موفق: {sent}\n❌ ناموفق: {failed}")
            return

@bot.on_callback_query(filters.regex("increase_balance"))
async def increase_balance_handler(client, callback_query):
    user_id = callback_query.from_user.id
    ok, not_joined = await check_force_join(client, user_id)
    if not ok:
        buttons = []
        for ch in not_joined:
            buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
        buttons.append([
            InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check_join")
        ])
        
        await callback_query.message.edit_text(
            "❌ برای استفاده از ربات باید در تمام کانال‌های زیر عضو شوید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    user_data = db.get("users", user_id, {})
    if user_data.get('rejected'):
        await callback_query.answer("❌ حساب شما توسط ادمین رد شده است. امکان افزایش موجودی ندارید.", show_alert=True)
        return
    if not user_data.get('verified'):
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("● احراز هویت ●", callback_data="start_verification")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back")
            ]
        ])
        
        await callback_query.message.edit_text(
            "🔒 **برای افزایش موجودی نیاز به احراز هویت دارید**\n\n"
            "📋 **مراحل احراز هویت:**\n"
            "1️⃣ کلیک روی دکمه 'احراز هویت'\n"
            "2️⃣ ارسال عکس از کارت بانکی\n"
            "3️⃣ تایید توسط ادمین\n"
            "4️⃣ افزایش موجودی\n\n"
            "⚠️ **توجه:** اطلاعات حساس (CVV2، تاریخ انقضا) در عکس پوشیده شود",
            reply_markup=keyboard
        )
        return
    else:
        await callback_query.message.edit_text(
            "💰 **افزایش موجودی**\n\n"
            f"💎 **نرخ تبدیل:** هر {COIN_RATE} الماس = 15,000 تومان\n"
            f"💵 **قیمت هر الماس:** {TOMAN_PER_COIN:.0f} تومان\n\n"
            "🔢 **تعداد الماس مورد نظر خود را وارد کنید:**\n"
            "مثال: 1000\n\n"
            "💡 **توجه:** فقط عدد وارد کنید (بدون نقطه یا کاما)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
        )
        
        db.delete("temp_data", f"waiting_coins_{user_id}")
        db.set("temp_data", f"waiting_coins_{user_id}", True)
        await callback_query.answer("✅ لطفا تعداد الماس مورد نظر را وارد کنید")

def main():
    print("● ربات سلف ساز روشن شد ●")
    try: 
        bot.run()
    except KeyboardInterrupt: 
        print("\n🛑 توقف ربات...")
    except Exception as e: 
        print(f"❌ خطا: {e}")
    finally: 
        stop_all_selfbots()
        print("✅ ربات متوقف شد")

if __name__ == "__main__":
    main()