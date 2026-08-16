from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CallbackQueryHandler, ContextTypes, InlineQueryHandler, MessageHandler, filters
import logging
import re

TOKEN = "8845956869:AAGSa1koh_30s3LAhe4pRhvqe5OqaIP-Q0Y"

# ============ آیدی ایموجی‌های پریمیوم ============
PREMIUM_EMOJIS = {
    # صفحه 1
    "id": "4999002445444023072",
    "time": "5017179932451668652",
    "photo": "5257974976094412956",
    "backup": "5044472594191876895",
    "font": "5222108309795908493",
    "price": "5258368777350816286",
    "format": "5805523593404095489",
    "spam": "5260535596941582167",
    "enemy": "5258362837411045098",
    "autoreply": "5258152182150077732",
    
    # صفحه 2
    "insult": "5258093637450866522",
    "online": "6269377265348383859",
    "lock": "5258507474729704350",
    "antilogin": "5350619413533958825",
    "reaction": "5352647939472760941",
    "edit": "5258331647358540449",
    "banner": "5208893571599449245",
    "instagram": "5269682734820777950",
    "download": "5814318659929117141",
    "new": "5771816213323714335",
    
    # صفحه 3
    "private": "5195275965470629045",
    "glassy": "5938483969728188084",
    "calculator": "5312198723458054673",
    "forced": "6003670290402384022",
    "translate": "5352625743081775722",
    "profile_view": "5474194650661147876",
    "setup_enemy": "5296320796300426938",
    "action": "4999002445444023072",
    "count": "6219882697884436514",
    "leave_all": "6298335558355651118",
    
    # صفحه 4
    "wing": "5278701899854407936",
    "ai_image": "6379547845376024613",
    "tts": "5958723002383211565",
    "tempmail": "5019626126780138240",
    "gold": "6012769393367327009",
    "wings_list": "6001431873706791348",
    "wing_off": "6046606606014091997",
    "wing_set": "6046344613009037370",
    "meow_meow": "6379547845376024622",  # ایموجی جدید برای میو میو
    
    # دکمه‌های عمومی
    "page1": "5861573955998982554",
    "page2": "5861458167975648646",
    "page3": "5861610622134787546",
    "page4": "5864178329677996349",
    "close": "5447228621183807807",
    "back": "6129870117619634982",
    "reopen": "5019726744978981602",
    "next": "6379547845376024620",
    "prev": "6379547845376024621"
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============ متون راهنمای جدید ============

WINGS_LIST_TEXT = """
🪽 **لیست کامل بال‌های ساعت (۱۹۴ مدل)**

📋 **بال‌های ۱ تا ۳۰:**
1: ❰ ⩇⩇:⩇⩇ ❱
2: ✧ ⩇⩇:⩇⩇ ✧
3: 𓆩 ⩇⩇:⩇⩇ 𓆪
4: ❦ ⩇⩇:⩇⩇ ❦
5: ᥫ᭡ ⩇⩇:⩇⩇ ᥫ᭡
6: ♛ ⩇⩇:⩇⩇ ♛
7: ༒︎ ⩇⩇:⩇⩇ ༒︎
8: ⨺⃝ ⩇⩇:⩇⩇ ⨺⃝
9: ۝ ⩇⩇:⩇⩇ ۝
10: ߷ ⩇⩇:⩇⩇ ߷
11: ཊ ⩇⩇:⩇⩇ ཏ
12: ࿘ ⩇⩇:⩇⩇ ࿘
13: ࿇ ⩇⩇:⩇⩇ ࿇
14: ࿈ ⩇⩇:⩇⩇ ࿈
15: ፠ ⩇⩇:⩇⩇ ፠
16: ☫ ⩇⩇:⩇⩇ ☫
17: ꙮ‌‌‌‌‌‌ ⩇⩇:⩇⩇ ꙮ‌‌‌‌‌‌
18: ▄︻デ ⩇⩇:⩇⩇ ══━一
19: ﷽ ⩇⩇:⩇⩇ ﷽
20: 🝪 ⩇⩇:⩇⩇ 🝪
21: 🜎 ⩇⩇:⩇⩇ 🜎
22: ቿ ⩇⩇:⩇⩇ ቿ
23: ᳇ ⩇⩇:⩇⩇ ᳇
24: ␥ ⩇⩇:⩇⩇
25: ⟬ ⩇⩇:⩇⩇ ⟭
26: ꧁ ⩇⩇:⩇⩇ ꧂
27: ༺ ⩇⩇:⩇⩇ ༻
28: 𓄂 ⩇⩇:⩇⩇ 𓆃
29: ۩ ⩇⩇:⩇⩇ ۩
30: ✞︎ ⩇⩇:⩇⩇ ✞︎

📌 **برای تنظیم بال:** `بال [عدد]`
📌 **برای غیرفعال کردن:** `بال خاموش`
📌 **برای مشاهده ادامه:** `بال لیست`
"""

WINGS_LIST_2 = """
🪽 **ادامه لیست بال‌ها (۳۱ تا ۶۰)**

31: ⨭ ⩇⩇:⩇⩇ ⨮
32: 𓆰 ⩇⩇:⩇⩇ 𓆪
33: 𖤍 ⩇⩇:⩇⩇ 𖤍
34: ❖ ⩇⩇:⩇⩇ ❖
35: 『 ⩇⩇:⩇⩇ 』
36: ʚ ⩇⩇:⩇⩇ ɞ
37: ၄ ⩇⩇:⩇⩇ ၃
38: ⚚ ⩇⩇:⩇⩇ ⚚
39: 𝄃𝄂𝄂𝄃 ⩇⩇:⩇⩇ 𝄃𝄂𝄂??
40: ⁂ ⩇⩇:⩇⩇ ⁂
41: ⫷ ⩇⩇:⩇⩇ ⫸
42: ⦓ ⩇⩇:⩇⩇ ⦔
43: ✤ ⩇⩇:⩇⩇ ✤
44: 𒆜 ⩇⩇:⩇⩇ 𒆜
45: 𓂍 ⩇⩇:⩇⩇ 𓂍
46: ⁘ ⩇⩇:⩇⩇ ⁘
47: ⧰ ⩇⩇:⩇⩇ ⧱
48: ⧼ ⩇⩇:⩇⩇ ⧽
49: ⧪ ⩇⩇:⩇⩇ ⧪
50: ☬ ⩇⩇:⩇⩇ ☬
51: 𒉭 ⩇⩇:⩇⩇ 𒉭
52: ᯤ ⩇⩇:⩇⩇ ᯤ
53: 三 ⩇⩇:⩇⩇ 三
54: 🃜 ⩇⩇:⩇⩇ 🃜
55: 🃚 ⩇⩇:⩇⩇ 🃚
56: 🃖 ⩇⩇:⩇⩇ 🃖
57: 🃁 ⩇⩇:⩇⩇ 🃁
58: 🂭 ⩇⩇:⩇⩇ 🂭
59: 🂺 ⩇⩇:⩇⩇ 🂺
60: 𖤓 ⩇⩇:⩇⩇ 𖤓

📌 **ادامه در صفحه بعد...**
"""

WINGS_LIST_3 = """
🪽 **ادامه لیست بال‌ها (۶۱ تا ۹۰)**

61: ☾ ⩇⩇:⩇⩇ ☾
62: 𐀪 ⩇⩇:⩇⩇ 𐀪
63: ❅ ⩇⩇:⩇⩇ ❅
64: ♡ ⩇⩇:⩇⩇ ♡
65: (◣ ⩇⩇:⩇⩇ ◢)
66: ✯ ⩇⩇:⩇⩇ ✯
67: ❝ ⩇⩇:⩇⩇ ❞
68: ⊱⋆⊳ ⩇⩇:⩇⩇ ⊲⋆⊰
69: 「 ⩇⩇:⩇⩇ 」
70: 𓊈 ⩇⩇:⩇⩇ 𓊉
71: 𓉘 ⩇⩇:⩇⩇ 𓉝
72: 𓊆 ⩇⩇:⩇⩇ 𓊇
73: [ ⩇⩇:⩇⩇ ]
74: ╽ ⩇⩇:⩇⩇ ╿
75: ┞ ⩇⩇:⩇⩇ ┦
76: ┌ ⩇⩇:⩇⩇ ┐
77: ⌜ ⩇⩇:⩇⩇ ⌝
78: 【 ⩇⩇:⩇⩇ 】
79: 〖 ⩇⩇:⩇⩇ 〗
80: ⎰ ⩇⩇:⩇⩇ ⎱
81: ⚟ ⩇⩇:⩇⩇ ⚞
82: ⸦ ⩇⩇:⩇⩇ ⸧
83: ╰ ⩇⩇:⩇⩇ ╯
84: ⦑ ⩇⩇:⩇⩇ ⦒
85: ☾ ⩇⩇:⩇⩇ ☽
86: ⌠ ⩇⩇:⩇⩇ ⌡
87: ⧼ ⩇⩇:⩇⩇ ⧽
88: ⊰ ⩇⩇:⩇⩇ ⊱
89: ཋྀ ⩇⩇:⩇⩇ ཐི
90: ╬ ⩇⩇:⩇⩇ ╬
"""

WINGS_LIST_4 = """
🪽 **ادامه لیست بال‌ها (۹۱ تا ۱۲۰)**

91: 《 ⩇⩇:⩇⩇ 》
92: ★ ⩇⩇:⩇⩇ ★
93: # ⩇⩇:⩇⩇ #
94: Д ⩇⩇:⩇⩇ Д
95: ⑅ ⩇⩇:⩇⩇ ⑅
96: ♪ ⩇⩇:⩇⩇ ♪
97: ♬ ⩇⩇:⩇⩇ ♬
98: ⚕ ⩇⩇:⩇⩇ ⚕
99: ♀ ⩇⩇:⩇⩇ ♀
100: ⋆ ⩇⩇:⩇⩇ ⋆
101: ₊ ⩇⩇:⩇⩇ ₊
102: ꙳ ⩇⩇:⩇⩇ ꙳
103: ࿔ ⩇⩇:⩇⩇ ࿔
104: ❆ ⩇⩇:⩇⩇ ❆
105: ꨄ ⩇⩇:⩇⩇ ꨄ
106: ✚ ⩇⩇:⩇⩇ ✚
107: ✖ ⩇⩇:⩇⩇ ✖
108: ᡣ𐭩 ⩇⩇:⩇⩇ ᡣ𐭩
109: ❰❰ ⩇⩇:⩇⩇ ❱❱
110: ❀ ⩇⩇:⩇⩇ ❀
111: ထ ⩇⩇:⩇⩇ ထ
112: ╭⊰ ⩇⩇:⩇⩇ ⊱╮
113: ࿐| ⩇⩇:⩇⩇ |࿐
114: 𓆩♡𓆪 ⩇⩇:⩇⩇ 𓆩♡𓆪
115: ✦◈ ⩇⩇:⩇⩇ ◈✦
116: ◉⦿◉ ⩇⩇:⩇⩇ ◉⦿◉
117: ✨✨ ⩇⩇:⩇⩇ ✨✨
118: ꧁♢✸ ⩇⩇:⩇⩇ ✸♢꧂
119: ⋆═✩═⋆ ⩇⩇:⩇⩇ ⋆═✩═⋆
120: 一═⌊✦⌋ ⩇⩇:⩇⩇ ⌊✦⌋═一
"""

WINGS_LIST_5 = """
🪽 **ادامه لیست بال‌ها (۱۲۱ تا ۱۵۰)**

121: ⋆˚｡⋆୨✧୧˚ ⩇⩇:⩇⩇ ˚୨✧୧⋆｡˚⋆
122: ▂▃▅▇█▓▒ ⩇⩇:⩇⩇ ▒▓█▇▅▃▂
123: ▁ ▂ ▃ ▅ ▆ ▇ ▌ ⩇⩇:⩇⩇ ▐ ▇ ▆ ▅ ▃ ▂ ▁
124: ★.¸¸.•´¯•.¸¸.★ ⩇⩇:⩇⩇ ★.¸¸.•´¯•.¸¸.★
125: ┗━━━━━━⊱ ⩇⩇:⩇⩇ ⊰━━━━━━┛
126: ˜”°•.¸☆¸.•°”˜ ⩇⩇:⩇⩇ ˜”°•.¸☆¸.•°”˜
127: ✧˚·‌‌‌‌˚‌‌‌‌·‌‌‌‌✧·‌‌‌‌˚‌‌‌‌˚·‌‌‌‌✧ ⩇⩇:⩇⩇ ✧˚·‌‌‌‌˚‌‌‌‌‌‌
128: ˜”°•.¸✦¸.•°”˜ ⩇⩇:⩇⩇ ˜”°•.¸✦¸.•°”˜
129: ꧁✬◦°⋆⋆°◦. ⩇⩇:⩇⩇ ◦°⋆⋆°◦✬꧂
130: ✦▄✦▀✦▄ ⩇⩇:⩇⩇ ▄✦▀✦▄✦
131: ─═✩✧═─ ⩇⩇:⩇⩇ ─═✧✩═─
132: ˜”°•✿•°”˜ ⩇⩇:⩇⩇ ˜”°•✿•°”˜
133: ✦•·.·¯˚·.·• ⩇⩇:⩇⩇ •·.·˚¯·.·•✦
134: ✦⁺₊✩☽⋆ ⩇⩇:⩇⩇ ⋆☾✩⁺₊✦
135: ⌠═❖═⌡ ⩇⩇:⩇⩇ ⌠═❖═⌡
136: ▢▣▢▣ ⩇⩇:⩇⩇ ▣▢▣▢
137: ❚█══ ⩇⩇:⩇⩇ ══█❚
138: ⋆·˚˚°✦ ⩇⩇:⩇⩇ ✦°˚˚·⋆
139: ﮩ٨ـﮩﮩ٨ـ ⩇⩇:⩇⩇ ﮩ٨ـﮩﮩ٨ـ
140: ╭─❖ ⩇⩇:⩇⩇ ❖─╮
141: ╰┈☆ ⩇⩇:⩇⩇ ☆┈╯
142: ▞▞▞ ⩇⩇:⩇⩇ ▞▞▞
143: ⊱❀⊰ ⩇⩇:⩇⩇ ⊱❀⊰
144: -♡´- ⩇⩇:⩇⩇ -♡´-
145: ✧【 ⩇⩇:⩇⩇ 】✧
146: ⌜✺⌟ ⩇⩇:⩇⩇ ⌜✺⌟
147: 𓆏 ⩇⩇:⩇⩇ 𓆏
148: 𓆈 ⩇⩇:⩇⩇ 𓆈
149: 𓄘 ⩇⩇:⩇⩇ 𓄘
150: 𓄻 ⩇⩇:⩇⩇ 𓄻
"""

WINGS_LIST_6 = """
🪽 **ادامه لیست بال‌ها (۱۵۱ تا ۱۹۴)**

151: 𓂀 ⩇⩇:⩇⩇ 𓂀
152: 𓀀 ⩇⩇:⩇⩇ 𓀀
153: 𓆉 ⩇⩇:⩇⩇ 𓆉
154: 𓅃 ⩇⩇:⩇⩇ 𓅃
155: 𓆠 ⩇⩇:⩇⩇ 𓆠
156: 𓅀 ⩇⩇:⩇⩇ 𓅀
157: 𓄎 ⩇⩇:⩇⩇ 𓄎
158: 𓄏 ⩇⩇:⩇⩇ 𓄏
159: 𓅨 ⩇⩇:⩇⩇ 𓅨
160: 𓅳 ⩇⩇:⩇⩇ 𓅳
161: 𓅰 ⩇⩇:⩇⩇ 𓅰
162: 𓆭 ⩇⩇:⩇⩇ 𓆭
163: 𓂧 ⩇⩇:⩇⩇ 𓂧
164: 𓃂 ⩇⩇:⩇⩇ 𓃂
165: 𓅋 ⩇⩇:⩇⩇ 𓅋
166: 𓅅 ⩇⩇:⩇⩇ 𓅅
167: 𓀂 ⩇⩇:⩇⩇ 𓀂
168: 𓀌 ⩇⩇:⩇⩇ 𓀌
169: 𓅀 ⩇⩇:⩇⩇ 𓅀
170: 𓃷 ⩇⩇:⩇⩇ 𓃷
171: 𓅂 ⩇⩇:⩇⩇ 𓅂
172: 𓂝 ⩇⩇:⩇⩇ 𓂝
173: 𓃀 ⩇⩇:⩇⩇ 𓃀
174: 𓆆 ⩇⩇:⩇⩇ 𓆆
175: 𓆁 ⩇⩇:⩇⩇ 𓆁
176: 𓃗 ⩇⩇:⩇⩇ 𓃗
177: 𓄅 ⩇⩇:⩇⩇ 𓄅
178: 𓆢 ⩇⩇:⩇⩇ 𓆢
179: 𓃀 ⩇⩇:⩇⩇ 𓃀
180: 𓃤 ⩇⩇:⩇⩇ 𓃤
181: 𓂘 ⩇⩇:⩇⩇ 𓂘
182: 𓅌 ⩇⩇:⩇⩇ 𓅌
183: 𓂪 ⩇⩇:⩇⩇ 𓂪
184: 𓃪 ⩇⩇:⩇⩇ 𓃪
185: 𓆀 ⩇⩇:⩇⩇ 𓆀
186: 𓈖 ⩇⩇:⩇⩇ 𓈖
187: 𓄸 ⩇⩇:⩇⩇ 𓄸
188: 𓇎 ⩇⩇:⩇⩇ 𓇎
189: 𓅭 ⩇⩇:⩇⩇ 𓅭
190: 𓆜 ⩇⩇:⩇⩇ 𓆜
191: 𓇰 ⩇⩇:⩇⩇ 𓇰
192: 𓈓 ⩇⩇:⩇⩇ 𓈓
193: 𓉀 ⩇⩇:⩇⩇ 𓉀
194: 𓇑 ⩇⩇:⩇⩇ 𓇑

📌 **برای تنظیم بال:** `بال [عدد]`
📌 **برای غیرفعال کردن:** `بال خاموش`
"""

# ============ متون راهنمای قبلی ============

HELP_TEXTS = {
    # ============ صفحه 1 ============
    "time": """
⏰ <b>مدیریت تایم</b>

<b>دستورات قابل کپی:</b>
<code>تایم روشن</code>
<code>تایم خاموش</code>

<b>کاربرد:</b>
نمایش زمان کنار نام کاربری
آپدیت خودکار هر دقیقه
فونت‌های مختلف برای زمان

<b>فونت‌های موجود:</b>
𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗 - فونت 1
𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 - فونت 2  
０１２３４５６７８９ - فونت 3
𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫 - فونت 4
𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡 - فونت 5
0҉1҉2҉3҉4҉5҉6҉7҉8҉9҉ - فونت 6
""",

    "instagram": """
📥 <b>دانلودر اینستاگرام</b>

<b>دستور قابل کپی:</b>
<code>اینستا لینک_پست</code>

<b>مثال‌ها:</b>
<code>اینستا https://www.instagram.com/reel/DOkym3fCFqg/</code>
<code>اینستا https://www.instagram.com/p/CzuF4KQqJ7q/</code>
<code>اینستا https://www.instagram.com/tv/Cxxxxxxxx/</code>

<b>کاربرد:</b>
• دانلود پست‌های اینستاگرام
• دانلود ریل‌ ها و ویدیو ها
• دانلود عکس‌های پست

<b>قابلیت‌ها:</b>
✅ دانلود با کیفیت اصلی
✅ نمایش توضیحات پست
✅ نمایش اطلاعات کاربر
✅ آپلود در همان چت
""",

    "id": """
🆔 <b>سیستم آیدی پیشرفته</b>

<b>دستور قابل کپی:</b>
<code>ایدی</code>

<b>دو حالت استفاده:</b>

1️⃣ <b>بدون ریپلای:</b>
<code>ایدی</code>
• نمایش اطلاعات خودتان
• نمایش اطلاعات چت فعلی
• نمایش آیدی عددی

2️⃣ <b>با ریپلای:</b>
<code>ایدی</code> (روی پیام کاربر ریپلای)
• نمایش اطلاعات کامل کاربر
• نمایش گروه‌های مشترک  
• نمایش آیدی و یوزرنیم

<b>اطلاعات نمایش داده شده:</b>
✅ آیدی عددی کاربر
✅ یوزرنیم و نام کامل
✅ وضعیت پریمیوم
✅ تعداد عکس‌های پروفایل
✅ آیدی چت و عنوان
✅ تعداد اعضا (در گروه)
✅ گروه‌های مشترک (در صورت وجود)

<b>مثال خروجی:</b>
• اطلاعات شما + چت فعلی
• یا اطلاعات کاربر ریپلای شده
""",

    "photo": """
📸 <b>ذخیره عکس تایمدار</b>

<b>دستور قابل کپی:</b>
<code>عکس سیو</code> (ریپلای روی عکس)

<b>کاربرد:</b>
ذخیره دستی عکس‌های تایمدار
ارسال اطلاعات کامل کاربر

<b>نکته:</b>
فقط روی عکس‌های تایمدار کار می‌کند
عکس معمولی قابل ذخیره نیست
""",

    "backup": """
💾 <b>پشتیبان‌گیری</b>

<b>دستور قابل کپی:</b>
<code>سیو @یوزرنیم</code>

<b>مثال:</b>
<code>سیو @username</code>

<b>کاربرد:</b>
ذخیره تاریخچه چت در فایل متنی
ارسال فایل به پیام‌های ذخیره شده
""",

    "font": """
🔤 <b>مدیریت فونت</b>

<b>دستورات قابل کپی:</b>
<code>لیست فونت</code>
<code>تنظیم فونت 1</code> تا <code>تنظیم فونت 6</code>

<b>کاربرد:</b>
تغییر فونت نمایش زمان
پیش‌نمایش فونت‌های مختلف
اعمال فونت روی زمان به صورت زنده
""",

    "price": """
💱 <b>قیمت ارز</b>

<b>دستور قابل کپی:</b>
<code>قیمت ارز</code>

<b>مثال‌ها:</b>
<code>قیمت BTC</code>
<code>قیمت ETH</code>
<code>قیمت TON</code>

<b>کاربرد:</b>
نمایش قیمت لحظه‌ای ارزهای دیجیتال
نمایش قیمت تومانی و دلاری
نمایش تغییرات 24 ساعته
میتوانید اسم ارزو رو به فارسی بزارید
""",

    "spam": """
🔁 <b>ارسال اسپم</b>

<b>دستور قابل کپی:</b>
<code>اسپم تعداد متن</code>

<b>مثال‌ها:</b>
<code>اسپم 10 سلام</code>
<code>اسپم 5 تست</code>

<b>کاربرد:</b>
ارسال پیام تکراری
حداکثر 50 پیام در یک دستور
قابلیت ریپلای روی پیام
""",

    "format": """
🎨 <b>سیستم فرمت خودکار HTML</b>

<b>دستورات قابل کپی:</b>
<code>فرمت بولد روشن</code>
<code>فرمت بولد خاموش</code>
<code>فرمت ایتالیک روشن</code>
<code>فرمت ایتالیک خاموش</code>
<code>فرمت زیرخط روشن</code>
<code>فرمت زیرخط خاموش</code>
<code>فرمت خط‌خورده روشن</code>
<code>فرمت خط‌خورده خاموش</code>
<code>فرمت اسپویلر روشن</code>
<code>فرمت اسپویلر خاموش</code>
<code>فرمت کد روشن</code>
<code>فرمت کد خاموش</code>
<code>فرمت پیش‌فرمت روشن</code>
<code>فرمت پیش‌فرمت خاموش</code>
<code>فرمت نقل‌قول روشن</code>
<code>فرمت نقل‌قول خاموش</code>
<code>فرمت وضعیت</code>
<code>فرمت ریست</code>

<b>کاربرد:</b>
تبدیل خودکار پیام‌ ها به فرمت‌ های مختلف
پشتیبانی از تمام تگ‌های HTML تلگرام
امکان استفاده همزمان از چندین فرمت

<b>فرمت‌های پشتیبانی شده:</b>
• <b>بولد</b> - <b>متن بولد</b>
• <i>ایتالیک</i> - <i>متن ایتالیک</i>
• <u>زیرخط</u> - <u>متن زیرخط دار</u>
• <s>خط‌خورده</s> - <s>متن خط خورده</s>
• <code>کد</code> - <code>متن کد</code>
• <pre>پیش‌فرمت</pre> - <pre>متن پیش‌فرمت</pre>
• <blockquote>نقل‌قول</blockquote> - <blockquote>متن نقل قول</blockquote>
""",

    "enemy": """
👿 <b>مدیریت دشمنان</b>

<b>دستورات قابل کپی:</b>
<code>دشمن</code> (ریپلای روی پیام کاربر)
<code>حذف دشمن</code> (ریپلای روی پیام کاربر)
<code>لیست دشمن</code>
<code>دشمنان</code>
<code>پاک کردن دشمنان</code>

<b>کاربرد:</b>
افزودن کاربر به لیست دشمنان
ارسال خودکار فحش رندوم به دشمنان
مدیریت لیست دشمنان
نمایش اطلاعات کامل دشمنان
حذف دشمن از لیست""",

    "autoreply": """
🤖 <b>پاسخ خودکار</b>

<b>دستورات قابل کپی:</b>
<code>پاسخ افزودن سلام|سلام چطوری</code>
<code>پاسخ حذف سلام</code>
<code>پاسخ لیست</code>

<b>مثال‌ها:</b>
<code>پاسخ افزودن سلا|سلام عزیزم</code>
<code>پاسخ افزودن چطوری|خوبم ممنون</code>
<code>پاسخ حذف سلا</code>

<b>کاربرد:</b>
تنظیم پاسخ خودکار برای کلمات خاص
لیست پاسخ‌ های تنظیم شده
""",

    # ============ صفحه 2 ============
    "insult": """
💢 <b>مدیریت فحش‌ها</b>

<b>دستورات قابل کپی:</b>
<code>فحش افزودن متن فحش</code>
<code>فحش حذف متن فحش</code>

<b>مثال‌ها:</b>
<code>فحش افزودن تو احمقی</code>
<code>فحش افزودن برو گمشو</code>
<code>فحش حذف تو احمقی</code>

<b>کاربرد:</b>
افزودن فحش‌های جدید به لیست
حذف فحش ‌های موجود
ارسال رندوم فحش به دشمنان
""",

    "online": """
🌐 <b>حالت همیشه آنلاین</b>

<b>دستورات قابل کپی:</b>
<code>آنلاین روشن</code>
<code>آنلاین خاموش</code>

<b>کاربرد:</b>
فعال کردن حالت همیشه آنلاین
نمایش آنلاین دائمی در تلگرام
مناسب برای نشان دادن فعالیت دائمی
""",

    "lock": """
🔒 <b>سیستم قفل پیوی</b>

<b>دستورات قابل کپی:</b>
<code>همه روشن</code>
<code>همه خاموش</code>
<code>مدیا روشن</code>
<code>مدیا خاموش</code>
<code>استیکر روشن</code>
<code>استیکر خاموش</code>
<code>فوروارد روشن</code>
<code>فوروارد خاموش</code>
<code>وویس روشن</code>
<code>وویس خاموش</code>
<code>پیام روشن</code>
<code>پیام خاموش</code>
<code>فایل روشن</code>
<code>فایل خاموش</code>
<code>وضعیت قفل</code>
<code>ریست قفل</code>
<code>راهنمای قفل</code>

<b>کاربرد:</b>
محدود کردن ارسال انواع پیام در پیوی
حذف خودکار پیام‌های غیرمجاز
مدیریت دسترسی ‌های کاربران
نمایش وضعیت قفل ‌ها
""",

    "antilogin": """
🛡️ <b>سیستم انتی لاگین</b>

<b>دستورات قابل کپی:</b>
<code>انتی لاگین روشن</code>
<code>انتی لاگین خاموش</code>
<code>انتی لاگین</code>

<b>کاربرد:</b>
منقضی کردن کد اتوماتیک
جلوگیری از ورود به اکانت
""",

    "reaction": """
🎭 <b>سیستم ریکشن خودکار</b>

<b>دستورات قابل کپی:</b>
<code>ریکت ایموجی</code> (ریپلای روی کاربر)
<code>حذف ریکت</code> (ریپلای روی کاربر)
<code>لیست ریکت</code>
<code>پاکسازی ریکت</code>

<b>مثال‌ها:</b>
<code>ریکت 🚀</code> (ریپلای)
<code>ریکت ❤️</code> (ریپلای)
<code>حذف ریکت</code> (ریپلای)

<b>کاربرد:</b>
تنظیم ریکشن خودکار برای کاربران خاص
اعمال ریکشن روی تمام پیام‌ های کاربر
مدیریت لیست ریکشن‌ ‌ها
حذف ریکشن کاربران
""",

    "edit": """
✏️ <b>ویرایش سریع پیام</b>

<b>دستور قابل کپی:</b>
<code>ویرایش کلمه_قدیمی به کلمه_جدید</code> (ریپلای)

<b>مثال‌ها:</b>
<code>ویرایش سلان به سلام</code>
<code>ویرایش احمق به عزیز</code>
<code>ویرایش بد به خوب</code>

<b>کاربرد:</b>
جایگزینی سریع کلمه در پیام
ریپلای روی پیام مورد نظر
حذف خودکار پیام دستور
جایگزینی فقط کلمه مشخص شده
""",

    "banner": """
📢 <b>سیستم مدیریت بنر</b>

<b>دستورات قابل کپی:</b>
<code>تنظیم بنر</code> (ریپلای روی پیام)
<code>بنر همگانی کد</code>
<code>لیست بنرها</code>
<code>بنر همگانی خاموش</code>
<code>بنر ارسال کد</code>
<code>زمان بنر دقیقه</code>

<b>مثال‌ها:</b>
<code>تنظیم بنر</code> (ریپلای)
<code>بنر همگانی 1</code>
<code>بنر ارسال 1</code>
<code>زمان بنر 5</code>

<b>کاربرد:</b>
ثبت پیام به عنوان بنر
ارسال همگانی به گروه‌ها و سوپرگروه ‌ها
مدیریت بنرهای ثبت شده
تنظیم زمان بین ارسال‌ ها
ارسال فوری بنر
""",

    "download": """
📥 <b>دانلودر تلگرام</b>

<b>دستور قابل کپی:</b>
<code>دانلود لینک_پست</code>

<b>مثال‌ها:</b>
<code>دانلود https://t.me/channel/123</code>
<code>دانلود https://t.me/username/456</code>
<code>دانلود https://t.me/c/channel_id/post_id</code>

💡 <b>کاربرد اصلی:</b>
دانلود پست کانال های اسکم یا گروه ها
""",

    "new": """
🆕 <b>دستورات مربوط به کانال و گروه</b>

<b>دستورات قابل کپی:</b>
<code>پینگ</code>
<code>تعداد کانال ها</code>
<code>تعداد گروه ها</code>
<code>خروج همه کانال</code>
<code>خروج همه گروه</code>

<b>کاربرد:</b>
• <code>پینگ</code> - بررسی سرعت ربات
• <code>تعداد کانال ها</code> - نمایش آمار دقیق کانال‌ها
• <code>تعداد گروه ها</code> - نمایش آمار دقیق گروه‌ها
• <code>خروج همه کانال</code> - خروج از تمام کانال‌ها با تاخیر
• <code>خروج همه گروه</code> - خروج از تمام گروه‌ها با تاخیر

<b>نکته:</b>
تاخیر 4 ثانیه‌ ای برای جلوگیری از محدودیت
""",

    # ============ صفحه 3 ============
    "private": """
🕵️ <b>دانلود از کانال‌های خصوصی (پرایوت)</b>

<b>دستور قابل کپی:</b>
<code>پرایوت لینک_پست</code>

<b>مثال‌ها:</b>
<code>پرایوت https://t.me/private_channel/123</code>
<code>پرایوت https://t.me/c/123456789/100</code>

<b>کاربرد:</b>
• دانلود پست‌ها از کانال‌های خصوصی
• کپی خودکار به پیام‌های ذخیره شده
• پشتیبانی از تمام انواع مدیا

<b>قابلیت‌ها:</b>
✅ کار با کانال‌های خصوصی و عمومی
✅ کپی مستقیم به Saved Messages
✅ دانلود خودکار مدیا
✅ نمایش اطلاعات کامل پست
✅ مدیریت خطا و محدودیت
""",

    "glassy": """
🔮 <b>جلوه شیشه‌ای (Glassy Effect)</b>

<b>دستورات قابل کپی:</b>
<code>شیشه متن</code>
<code>شیشه مات متن</code>
<code>شیشه رنگی متن</code>
<code>شیشه الماس متن</code>

<b>مثال‌ها:</b>
<code>شیشه سلام دنیا!</code>
<code>شیشه مات این یک متن شیشه‌ای است</code>
<code>شیشه الماس ✨ متن خاص</code>

<b>انواع شیشه:</b>
🔹 <b>شیشه</b> - ساده و شفاف
🔹 <b>شیشه مات</b> - مات و مرموز
🔹 <b>شیشه رنگی</b> - رنگی و جذاب
🔹 <b>شیشه الماس</b> - ویژه و لوکس

<b>کاربرد:</b>
ارسال متن با جلوه‌های بصری زیبا
مناسب برای استایل دهی به پیام‌ها
ایجاد پیام‌های خاص و متفاوت
""",

    "calculator": """
🧮 <b>ماشین حساب پیشرفته</b>

<b>دستور قابل کپی:</b>
<code>حساب عبارت_ریاضی</code>

<b>مثال‌ها:</b>
<code>حساب 2 + 2</code>
<code>حساب 10 * 5 + 3</code>
<code>حساب 2 ^ 10</code>
<code>حساب (5 + 3) * 2</code>
<code>حساب 100 / 4</code>
<code>حساب 15 % 4</code>

<b>عملیات پشتیبانی شده:</b>
➕ ➖ ✖️ ➗ ^ % ** //

<b>توابع ریاضی:</b>
sqrt, sin, cos, tan, log, log10, abs, round, max, min

<b>کاربرد:</b>
محاسبات سریع و دقیق
مناسب برای معادلات پیچیده
""",

    "forced": """
🔒 <b>عضویت اجباری</b>

<b>دستورات قابل کپی:</b>
<code>عضویت روشن لینک_کانال</code>
<code>عضویت خاموش</code>
<code>عضویت وضعیت</code>

<b>مثال‌ها:</b>
<code>عضویت روشن https://t.me/my_channel</code>
<code>عضویت خاموش</code>
<code>عضویت وضعیت</code>

<b>کاربرد:</b>
اجبار کاربران به عضویت در کانال/گروه
قبل از ارسال پیام به شما

<b>قابلیت‌ها:</b>
✅ بررسی خودکار عضویت
✅ حذف پیام کاربران غیرعضو
✅ ارسال پیام راهنما
✅ نمایش وضعیت فعال/غیرفعال
""",

    "translate": """
🌐 <b>ترجمه پیشرفته</b>

<b>دستورات قابل کپی:</b>
<code>ترجمه متن</code> (ترجمه به فارسی)
<code>ترجمه زبان متن</code>
<code>ترجمه</code> (ریپلای روی پیام)

<b>مثال‌ها:</b>
<code>ترجمه انگلیسی Hello world</code>
<code>ترجمه سلام دنیا</code>
<code>ترجمه ترکی Merhaba dünya</code>

<b>زبان‌های پشتیبانی شده:</b>
• فارسی (fa) • انگلیسی (en)
• ترکی (tr) • عربی (ar)
• فرانسوی (fr) • آلمانی (de)
• اسپانیایی (es) • روسی (ru)
• ژاپنی (ja) • کرهای (ko)
• چینی (zh-CN) • ایتالیایی (it)
• پرتغالی (pt) • هندی (hi)
• اردو (ur)

<b>قابلیت‌ها:</b>
✅ تشخیص خودکار زبان
✅ ترجمه با کیفیت بالا
✅ نمایش متن اصلی و ترجمه
✅ پشتیبانی از ۱۵ زبان
""",

    "profile_view": """
👁️ <b>فضول پروفایل</b>

<b>دستورات قابل کپی:</b>
<code>فضول روشن</code>
<code>فضول خاموش</code>
<code>فضول وضعیت</code>
<code>فضول پاک</code>

<b>کاربرد:</b>
ردیابی افرادی که پروفایل شما را می‌بینند

<b>قابلیت‌ها:</b>
✅ ثبت خودکار بازدیدکنندگان
✅ نمایش نام و یوزرنیم
✅ نمایش زمان آخرین بازدید
✅ مشاهده آخرین ۱۰ بازدیدکننده
✅ پاک کردن لیست بازدیدها

<b>اطلاعات ذخیره شده:</b>
• نام کاربری
• یوزرنیم
• آیدی عددی
• زمان آخرین بازدید
""",

    "setup_enemy": """
👿 <b>تنظیم دشمن (پیشرفته)</b>

<b>دستور قابل کپی:</b>
<code>تنظیم دشمن</code> (ریپلای روی پیام کاربر)

<b>کاربرد:</b>
افزودن کاربر به لیست دشمنان با فحش‌های جدید

<b>قابلیت‌ها:</b>
✅ افزودن خودکار ۲۰۰+ فحش جدید
✅ ارسال فحش رندوم به دشمنان
✅ مدیریت کامل لیست دشمنان
✅ نمایش اطلاعات دشمن
✅ امکان حذف از لیست
""",

    "action": """
🎭 <b>سیستم اکشن خودکار</b>

<b>دستورات قابل کپی:</b>
<code>اکشن لیست</code>
<code>اکشن تایپ روشن</code>
<code>اکشن تایپ خاموش</code>
<code>اکشن اپلود عکس روشن</code>
<code>اکشن اپلود عکس خاموش</code>
<code>اکشن ضبط ویس روشن</code>
<code>اکشن ضبط ویس خاموش</code>
<code>اکشن اپلود ویدیو روشن</code>
<code>اکشن اپلود ویدیو خاموش</code>
<code>اکشن اپلود فایل روشن</code>
<code>اکشن اپلود فایل خاموش</code>
<code>اکشن بازی روشن</code>
<code>اکشن بازی خاموش</code>
<code>اکشن وضعیت</code>
<code>اکشن ریست</code>

<b>کاربرد:</b>
نمایش اکشن‌های مختلف هنگام دریافت پیام

<b>اکشن‌های موجود:</b>
⌨️ تایپ - 📸 اپلود عکس
🎤 ضبط ویس - 🎥 اپلود ویدیو
📄 اپلود فایل - 🎵 اپلود ویس
🎮 بازی - 👤 انتخاب مخاطب
📍 پیدا کردن موقعیت - 🎨 انتخاب استیکر
""",

    "leave_all": """
🚪 <b>خروج از همه گروه‌ها و کانال‌ها</b>

<b>دستورات قابل کپی:</b>
<code>خروج همه کانال</code>
<code>خروج همه گروه</code>

<b>کاربرد:</b>
خروج از تمام کانال‌ها یا گروه‌ها با تاخیر

<b>قابلیت‌ها:</b>
✅ خروج ایمن با تاخیر ۴ ثانیه‌ای
✅ نمایش پیشرفت عملیات
✅ نمایش تعداد موفق و ناموفق
✅ جلوگیری از محدودیت

<b>نکته:</b>
از این دستورات با احتیاط استفاده کنید!
""",

    "count": """
📊 <b>آمار گروه‌ها و کانال‌ها</b>

<b>دستورات قابل کپی:</b>
<code>تعداد کانال ها</code>
<code>تعداد گروه ها</code>

<b>کاربرد:</b>
نمایش آمار دقیق کانال‌ها و گروه‌ها

<b>اطلاعات نمایش داده شده:</b>
✅ تعداد کل کانال‌ها
✅ تعداد کل گروه‌ها
✅ تعداد سوپرگروه‌ها
✅ لیست کامل کانال‌ها
✅ لیست کامل گروه‌ها

<b>نکته:</b>
تا ۲۰ آیتم اول نمایش داده می‌شود
""",

    # ============ صفحه 4 ============
    "wing": """
🪽 <b>سیستم بال‌های ساعت</b>

<b>دستورات قابل کپی:</b>
<code>بال [عدد]</code>
<code>بال خاموش</code>
<code>بال لیست</code>

<b>مثال‌ها:</b>
<code>بال 1</code>  → ❰ ⩇⩇:⩇⩇ ❱
<code>بال 26</code> → ꧁ ⩇⩇:⩇⩇ ꧂
<code>بال 35</code> → 『 ⩇⩇:⩇⩇ 』
<code>بال 114</code> → 𓆩♡𓆪 ⩇⩇:⩇⩇ 𓆩♡𓆪

<b>کاربرد:</b>
اضافه کردن بال‌های فانتزی دور ساعت
۱۹۴ مدل بال مختلف
هماهنگ با تایم و فونت

<b>بال‌های محبوب:</b>
• بال 1: ❰ ⩇⩇:⩇⩇ ❱
• بال 26: ꧁ ⩇⩇:⩇⩇ ꧂
• بال 35: 『 ⩇⩇:⩇⩇ 』
• بال 114: 𓆩♡𓆪 ⩇⩇:⩇⩇ 𓆩♡𓆪
""",

    "ai_image": """
📸 <b>ساخت عکس با هوش مصنوعی</b>

<b>دستور قابل کپی:</b>
<code>ساخت عکس [پرامپت]</code>

<b>مثال‌ها:</b>
<code>ساخت عکس یک اسب سفید در کنار رودخانه</code>
<code>ساخت عکس یک گربه نارنجی با کلاه جادوگر</code>
<code>ساخت عکس منظره کوهستانی با نور طلایی</code>

<b>کاربرد:</b>
ساخت عکس با استفاده از هوش مصنوعی
هرچه پرامپت دقیق‌تر باشد، خروجی بهتر است

<b>قابلیت‌ها:</b>
✅ تولید عکس با کیفیت بالا
✅ پشتیبانی از پرامپت‌های پیچیده
✅ ارسال مستقیم عکس در چت
✅ نمایش پرامپت در کپشن
""",

    "tts": """
🔊 <b>تبدیل متن به گفتار (TTS)</b>

<b>دستور قابل کپی:</b>
<code>گفتار [متن]</code>

<b>مثال‌ها:</b>
<code>گفتار سلام به همه دوستان عزیز</code>
<code>گفتار این یک تست صوتی است</code>

<b>کاربرد:</b>
تبدیل متن به صدای طبیعی
ارسال فایل MP3 در چت

<b>قابلیت‌ها:</b>
✅ صدای زن با کیفیت بالا
✅ پشتیبانی از متن‌های بلند
✅ ارسال به صورت فایل صوتی
✅ نمایش متن در کپشن
""",

    "tempmail": """
📧 <b>ایمیل فیک موقت</b>

<b>دستورات قابل کپی:</b>
<code>ایمیل جدید</code>
<code>ایمیل دریافت</code>

<b>مثال‌ها:</b>
<code>ایمیل جدید</code>
<code>ایمیل دریافت</code>

<b>کاربرد:</b>
ساخت ایمیل موقت برای دریافت پیام‌ها
مناسب برای ثبت‌نام در سایت‌ها

<b>قابلیت‌ها:</b>
✅ ساخت ایمیل جدید در لحظه
✅ دریافت پیام‌های صندوق ورود
✅ اعتبار ۱ ساعته
✅ نمایش فرستنده و موضوع
""",

    "gold": """
💰 <b>قیمت لحظه‌ای طلا</b>

<b>دستور قابل کپی:</b>
<code>قیمت طلا</code>

<b>کاربرد:</b>
دریافت قیمت لحظه‌ای طلا

<b>اطلاعات نمایش داده شده:</b>
✅ قیمت طلای ۱۸ عیار (تومانی و دلاری)
✅ قیمت طلای ۲۴ عیار (تومانی و دلاری)
✅ تغییرات قیمت
✅ تاریخ و زمان به‌روزرسانی

<b>قابلیت‌ها:</b>
✅ نمایش قیمت به تومان و دلار
✅ نمایش تغییرات روزانه
✅ آپدیت لحظه‌ای
""",

    # ============ میو میو ============
    "meow_meow": """
🐱 <b>سیستم میو میو</b>

<b>دستورات قابل کپی:</b>
<code>میو میو روشن</code>
<code>میو میو خاموش</code>
<code>میو میو وضعیت</code>

<b>کاربرد:</b>
فعال کردن قابلیت میو میو

<b>قابلیت‌ها:</b>
✅ فعال کردن 🟢
✅ غیرفعال کردن 🔴
✅ مشاهده وضعیت 📊
""",

    # ============ لیست بال‌ها ============
    "wings_list": WINGS_LIST_TEXT,
    "wings_list_2": WINGS_LIST_2,
    "wings_list_3": WINGS_LIST_3,
    "wings_list_4": WINGS_LIST_4,
    "wings_list_5": WINGS_LIST_5,
    "wings_list_6": WINGS_LIST_6,
}

# ============ استایل رنگی دکمه‌ها ============
BUTTON_STYLES = {
    # عملیات/قابلیت‌های عادی
    "id": "primary",
    "time": "success",
    "photo": "primary",
    "backup": "success",
    "font": "primary",
    "price": "success",
    "format": "primary",
    "spam": "danger",
    "enemy": "danger",
    "autoreply": "success",

    # صفحه 2
    "insult": "danger",
    "online": "success",
    "lock": "danger",
    "antilogin": "danger",
    "reaction": "success",
    "edit": "primary",
    "banner": "primary",
    "instagram": "primary",
    "download": "success",
    "new": "primary",

    # صفحه 3
    "private": "primary",
    "glassy": "primary",
    "calculator": "success",
    "forced": "success",
    "translate": "primary",
    "profile_view": "primary",
    "setup_enemy": "danger",
    "action": "success",
    "count": "primary",
    "leave_all": "danger",

    # صفحه 4
    "wing": "primary",
    "ai_image": "success",
    "tts": "success",
    "tempmail": "primary",
    "gold": "success",
    "wings_list": "primary",
    "meow_meow": "success",

    # ناوبری
    "page1": "primary",
    "page2": "primary",
    "page3": "primary",
    "page4": "primary",
    "back": "primary",
    "next": "success",
    "prev": "primary",
    "reopen": "success",
    "close": "danger",
}

def premium_button(text, callback_data, emoji_key, style=None):
    """ساخت دکمه با Custom Emoji + استایل رنگی جدید تلگرام."""
    emoji_id = PREMIUM_EMOJIS.get(emoji_key)
    button_style = style or BUTTON_STYLES.get(emoji_key, "primary")

    kwargs = {
        "text": text,
        "callback_data": callback_data,
        "style": button_style,
    }

    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id

    return InlineKeyboardButton(**kwargs)

# ============ صفحه 1 ============
def get_main_menu_page1(user_id):
    keyboard = [
        [
            premium_button(" ایدی", f"help_id_{user_id}_1", "id"),
            premium_button(" تایم", f"help_time_{user_id}_1", "time")
        ],
        [
            premium_button(" عکس تایمدار", f"help_photo_{user_id}_1", "photo"),
        ],
        [
            premium_button(" پشتیبان‌گیری", f"help_backup_{user_id}_1", "backup"),
            premium_button(" مدیریت فونت", f"help_font_{user_id}_1", "font")
        ],
        [
            premium_button(" قیمت ارز", f"help_price_{user_id}_1", "price"),
        ],
        [
            premium_button(" فرمت متن", f"help_format_{user_id}_1", "format"),
            premium_button(" اسپم", f"help_spam_{user_id}_1", "spam")
        ],
        [
            premium_button(" مدیریت دشمنان", f"help_enemy_{user_id}_1", "enemy"),
        ],
        [
            premium_button(" پاسخ خودکار", f"help_autoreply_{user_id}_1", "autoreply"),
        ],
        [
            premium_button(" صفحه", f"help_page2_{user_id}", "page2"),
            premium_button(" بست", f"help_close_{user_id}", "close")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ صفحه 2 ============
def get_main_menu_page2(user_id):
    keyboard = [
        [
            premium_button(" سیستم فحش", f"help_insult_{user_id}_2", "insult"),
            premium_button(" همیشه آنلاین", f"help_online_{user_id}_2", "online")
        ],
        [
            premium_button(" قفل پیوی", f"help_lock_{user_id}_2", "lock"),
        ],
        [
            premium_button(" انتی لاگین", f"help_antilogin_{user_id}_2", "antilogin"),
            premium_button(" ریکشن خودکار", f"help_reaction_{user_id}_2", "reaction")
        ],
        [
            premium_button(" ویرایش سریع", f"help_edit_{user_id}_2", "edit"),
        ],
        [
            premium_button(" سیستم بنر", f"help_banner_{user_id}_2", "banner"),
            premium_button(" اینستاگرام", f"help_instagram_{user_id}_2", "instagram")
        ],
        [
            premium_button(" دانلود تلگرام", f"help_download_{user_id}_2", "download"),
        ],
        [
            premium_button(" مدیریت گروه/کانال", f"help_new_{user_id}_2", "new"),
        ],
        [
            premium_button(" صفحه ", f"help_page1_{user_id}", "page1"),
            premium_button(" صفحه ", f"help_page3_{user_id}", "page3"),
            premium_button(" بستن", f"help_close_{user_id}", "close")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ صفحه 3 ============
def get_main_menu_page3(user_id):
    keyboard = [
        [
            premium_button(" پرایوت دانلود", f"help_private_{user_id}_3", "private"),
            premium_button(" شیشه", f"help_glassy_{user_id}_3", "glassy")
        ],
        [
            premium_button(" ماشین حساب", f"help_calculator_{user_id}_3", "calculator"),
            premium_button(" عضویت اجباری", f"help_forced_{user_id}_3", "forced")
        ],
        [
            premium_button(" ترجمه", f"help_translate_{user_id}_3", "translate"),
            premium_button(" فضول پروفایل", f"help_profile_view_{user_id}_3", "profile_view")
        ],
        [
            premium_button(" تنظیم دشمن", f"help_setup_enemy_{user_id}_3", "setup_enemy"),
            premium_button(" اکشن", f"help_action_{user_id}_3", "action")
        ],
        [
            premium_button(" آمار", f"help_count_{user_id}_3", "count"),
            premium_button(" خروج گروه", f"help_leave_all_{user_id}_3", "leave_all")
        ],
        [
            premium_button(" صفحه ", f"help_page2_{user_id}", "page2"),
            premium_button(" صفحه ", f"help_page4_{user_id}", "page4"),
            premium_button("بستن", f"help_close_{user_id}", "close")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ صفحه 4 ============
def get_main_menu_page4(user_id):
    keyboard = [
        [
            premium_button(" بال‌های ساعت", f"help_wing_{user_id}_4", "wing"),
            premium_button(" ساخت عکس AI", f"help_ai_image_{user_id}_4", "ai_image")
        ],
        [
            premium_button(" متن به گفتار", f"help_tts_{user_id}_4", "tts"),
            premium_button(" ایمیل فیک", f"help_tempmail_{user_id}_4", "tempmail")
        ],
        [
            premium_button(" قیمت طلا", f"help_gold_{user_id}_4", "gold"),
            premium_button(" میو میو", f"help_meow_meow_{user_id}_4", "meow_meow")
        ],
        [
            premium_button(" لیست کامل بال‌ها", f"help_wings_list_{user_id}_4", "wings_list"),
        ],
        [
            premium_button(" صفحه ", f"help_page3_{user_id}", "page3"),
            premium_button(" بستن", f"help_close_{user_id}", "close")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ دکمه‌های بال ============
def get_wings_navigation_buttons(user_id, page):
    """دکمه‌های ناوبری برای لیست بال‌ها"""
    buttons = []
    
    if page > 1:
        buttons.append(premium_button(" قبلی", f"help_wings_prev_{user_id}_{page-1}", "prev"))
    
    if page < 6:
        buttons.append(premium_button(" بعدی", f"help_wings_next_{user_id}_{page+1}", "next"))
    
    buttons.append(premium_button(" بازگشت", f"help_page4_{user_id}", "back"))
    
    return InlineKeyboardMarkup([buttons])

# ============ دکمه بازگشت ============
def get_back_button(user_id, from_page=1):
    if from_page == 4:
        return InlineKeyboardMarkup([
            [premium_button(" بازگشت به صفحه 4", f"help_page4_{user_id}", "back")]
        ])
    elif from_page == 3:
        return InlineKeyboardMarkup([
            [premium_button(" بازگشت به صفحه 3", f"help_page3_{user_id}", "back")]
        ])
    elif from_page == 2:
        return InlineKeyboardMarkup([
            [premium_button(" بازگشت به صفحه 2", f"help_page2_{user_id}", "back")]
        ])
    return InlineKeyboardMarkup([
        [premium_button(" بازگشت", f"help_back_{user_id}_{from_page}", "back")]
    ])

# ============ دکمه باز کردن مجدد ============
def get_reopen_button(user_id):
    return InlineKeyboardMarkup([
        [premium_button(" بازکردن پنل", f"help_reopen_{user_id}", "reopen")]
    ])

# ============ هندلر پیام ============
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
    await update.message.reply_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')

# ============ هندلر اینلاین ============
async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip().lower()
    
    if query == "panel":
        user_id = update.inline_query.from_user.id
        
        results = [
            InlineQueryResultArticle(
                id="1",
                title="🎛 پنل مدیریت سلف - صفحه 1",
                description="10 قابلیت اصلی - مدیریت کامل",
                input_message_content=InputTextMessageContent(
                    message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>",
                    parse_mode='HTML'
                ),
                reply_markup=get_main_menu_page1(user_id)
            ),
            InlineQueryResultArticle(
                id="2",
                title="🎛 پنل مدیریت سلف - صفحه 2",
                description="10 قابلیت تکمیلی - ابزارهای پیشرفته",
                input_message_content=InputTextMessageContent(
                    message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 10 قابلیت تکمیلی</i>",
                    parse_mode='HTML'
                ),
                reply_markup=get_main_menu_page2(user_id)
            ),
            InlineQueryResultArticle(
                id="3",
                title="🎛 پنل مدیریت سلف - صفحه 3",
                description="10 قابلیت جدید - امکانات ویژه",
                input_message_content=InputTextMessageContent(
                    message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه سوم - 10 قابلیت جدید</i>",
                    parse_mode='HTML'
                ),
                reply_markup=get_main_menu_page3(user_id)
            ),
            InlineQueryResultArticle(
                id="4",
                title="🎛 پنل مدیریت سلف - صفحه 4",
                description="5 قابلیت جدید + لیست بال‌ها",
                input_message_content=InputTextMessageContent(
                    message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه چهارم - 5 قابلیت جدید + لیست بال‌ها</i>",
                    parse_mode='HTML'
                ),
                reply_markup=get_main_menu_page4(user_id)
            )
        ]
        await update.inline_query.answer(results, cache_time=300, is_personal=True)

# ============ هندلر کالبک ============
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    if not f"_{user_id}" in data:
        await query.answer("دسترسی denied!", show_alert=True)
        return
    
    parts = data.split("_")
    if len(parts) >= 3:
        action = parts[1]
        if len(parts) >= 4 and parts[-1].isdigit():
            page_num = int(parts[-1])
        else:
            page_num = 1 
    else:
        await query.answer("داده نامعتبر!", show_alert=True)
        return
    
    # ============ بستن پنل ============
    if action == "close":
        text = "✅ <b>پنل بسته شد</b>\n\n💡 برای باز کردن مجدد:\n<code>@BotUsername panel</code>"
        await query.edit_message_text(text, reply_markup=get_reopen_button(user_id), parse_mode='HTML')
        return
    
    # ============ باز کردن مجدد ============
    if action == "reopen":
        text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
        await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
        return
    
    # ============ صفحه 1 ============
    if action == "page1":
        text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
        await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
        return
    
    # ============ صفحه 2 ============
    if action == "page2":
        text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 10 قابلیت تکمیلی</i>"
        await query.edit_message_text(text, reply_markup=get_main_menu_page2(user_id), parse_mode='HTML')
        return
    
    # ============ صفحه 3 ============
    if action == "page3":
        text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه سوم - 10 قابلیت جدید</i>"
        await query.edit_message_text(text, reply_markup=get_main_menu_page3(user_id), parse_mode='HTML')
        return
    
    # ============ صفحه 4 ============
    if action == "page4":
        text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه چهارم - 5 قابلیت جدید + لیست بال‌ها</i>"
        await query.edit_message_text(text, reply_markup=get_main_menu_page4(user_id), parse_mode='HTML')
        return
    
    # ============ ناوبری بال‌ها ============
    if action == "wings_next":
        page = int(parts[3]) if len(parts) > 3 else 2
        if page <= 6:
            wings_key = f"wings_list{'' if page == 1 else f'_{page}'}"
            text = HELP_TEXTS.get(wings_key, WINGS_LIST_TEXT)
            await query.edit_message_text(text, reply_markup=get_wings_navigation_buttons(user_id, page), parse_mode='HTML')
        return
    
    if action == "wings_prev":
        page = int(parts[3]) if len(parts) > 3 else 1
        if page >= 1:
            wings_key = f"wings_list{'' if page == 1 else f'_{page}'}"
            text = HELP_TEXTS.get(wings_key, WINGS_LIST_TEXT)
            await query.edit_message_text(text, reply_markup=get_wings_navigation_buttons(user_id, page), parse_mode='HTML')
        return
    
    # ============ بازگشت ============
    if action == "back":
        if page_num == 4:
            text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه چهارم - 5 قابلیت جدید + لیست بال‌ها</i>"
            await query.edit_message_text(text, reply_markup=get_main_menu_page4(user_id), parse_mode='HTML')
        elif page_num == 3:
            text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه سوم - 10 قابلیت جدید</i>"
            await query.edit_message_text(text, reply_markup=get_main_menu_page3(user_id), parse_mode='HTML')
        elif page_num == 2:
            text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 10 قابلیت تکمیلی</i>"
            await query.edit_message_text(text, reply_markup=get_main_menu_page2(user_id), parse_mode='HTML')
        else:
            text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
            await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
        return
    
    # ============ نمایش راهنما ============
    if action in HELP_TEXTS:
        text = HELP_TEXTS.get(action, "راهنمای این بخش آماده نیست.")
        if page_num == 4:
            if action == "wings_list":
                await query.edit_message_text(text, reply_markup=get_wings_navigation_buttons(user_id, 1), parse_mode='HTML')
            else:
                await query.edit_message_text(text, reply_markup=get_back_button(user_id, 4), parse_mode='HTML')
        elif page_num == 3:
            await query.edit_message_text(text, reply_markup=get_back_button(user_id, 3), parse_mode='HTML')
        elif page_num == 2:
            await query.edit_message_text(text, reply_markup=get_back_button(user_id, 2), parse_mode='HTML')
        else:
            await query.edit_message_text(text, reply_markup=get_back_button(user_id, page_num), parse_mode='HTML')
    else:
        await query.answer(f"این بخش ({action}) آماده نیست!", show_alert=True)

# ============ مدیریت خطا ============
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

# ============ اجرای اصلی ============
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, show_menu))
    app.add_handler(InlineQueryHandler(handle_inline_query))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)
    
    print("🤖 ربات هلپر اجرا شد")
    print("=" * 55)
    print("🎨 تمام دکمه‌ها دارای ایموجی پریمیوم هستند")
    print("")
    print("📋 قابلیت‌های موجود:")
    print("")
    print("📄 صفحه 1 - 10 قابلیت اصلی:")
    print("   🆔 ایدی (پریمیوم)")
    print("   ⏰ تایم (پریمیوم)")
    print("   📸 عکس تایمدار (پریمیوم)")
    print("   💾 پشتیبان‌گیری (پریمیوم)")
    print("   🔤 مدیریت فونت (پریمیوم)")
    print("   💱 قیمت ارز (پریمیوم)")
    print("   🎨 فرمت متن (پریمیوم)")
    print("   🔁 اسپم (پریمیوم)")
    print("   👿 مدیریت دشمنان (پریمیوم)")
    print("   🤖 پاسخ خودکار (پریمیوم)")
    print("")
    print("📄 صفحه 2 - 10 قابلیت تکمیلی:")
    print("   💢 سیستم فحش (پریمیوم)")
    print("   🌐 همیشه آنلاین (پریمیوم)")
    print("   🔒 قفل پیوی (پریمیوم)")
    print("   🛡️ انتی لاگین (پریمیوم)")
    print("   🎭 ریکشن خودکار (پریمیوم)")
    print("   ✏️ ویرایش سریع (پریمیوم)")
    print("   📢 سیستم بنر (پریمیوم)")
    print("   📥 اینستاگرام (پریمیوم)")
    print("   📥 دانلود تلگرام (پریمیوم)")
    print("   🆕 مدیریت گروه/کانال (پریمیوم)")
    print("")
    print("📄 صفحه 3 - 10 قابلیت جدید:")
    print("   🕵️ پرایوت دانلود (پریمیوم)")
    print("   🔮 شیشه (پریمیوم)")
    print("   🧮 ماشین حساب (پریمیوم)")
    print("   🔒 عضویت اجباری (پریمیوم)")
    print("   🌐 ترجمه (پریمیوم)")
    print("   👁️ فضول پروفایل (پریمیوم)")
    print("   👿 تنظیم دشمن (پریمیوم)")
    print("   🎭 اکشن (پریمیوم)")
    print("   📊 آمار (پریمیوم)")
    print("   🚪 خروج گروه (پریمیوم)")
    print("")
    print("📄 صفحه 4 - 5 قابلیت جدید + لیست بال‌ها:")
    print("   🪽 بال‌های ساعت (پریمیوم)")
    print("   📸 ساخت عکس AI (پریمیوم)")
    print("   🔊 متن به گفتار (پریمیوم)")
    print("   📧 ایمیل فیک (پریمیوم)")
    print("   💰 قیمت طلا (پریمیوم)")
    print("   🐱 میو میو (پریمیوم)")
    print("   📋 لیست کامل 194 بال (پریمیوم)")
    print("")
    print("=" * 55)
    print("💡 مجموع: 36 قابلیت در 4 صفحه")
    print("✨ هر 36 دکمه دارای ایموجی پریمیوم جداگانه")
    print("🎨 دکمه‌ها به صورت خودکار رنگی هستند")
    print("🪽 194 مدل بال برای ساعت")
    print("🐱 قابلیت میو میو اضافه شد")
    app.run_polling()

if __name__ == "__main__":
    main()