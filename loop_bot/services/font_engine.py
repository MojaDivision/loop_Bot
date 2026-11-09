import re

ASCII_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def generate_english_fonts():
    fonts = {}
    fonts['𝗕𝗼𝗹𝗱 𝗦𝗮𝗻𝘀 (بولد مدرن)'] = (
        ''.join(chr(0x1D5D4 + i) for i in range(26)) + 
        ''.join(chr(0x1D5EE + i) for i in range(26))
    )
    fonts['𝘚𝘢𝘯𝘴 𝘐𝘵𝘢𝘭𝘪𝓬 (ایتالیک روان)'] = (
        ''.join(chr(0x1D608 + i) for i in range(26)) + 
        ''.join(chr(0x1D622 + i) for i in range(26))
    )
    fonts['𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘 (بولد کج)'] = (
        ''.join(chr(0x1D63C + i) for i in range(26)) + 
        ''.join(chr(0x1D656 + i) for i in range(26))
    )
    fonts['𝓒𝓾𝓻𝓼𝓲𝓿𝓮 (خطی و فانتزی)'] = (
        ''.join(chr(0x1D4D0 + i) for i in range(26)) + 
        ''.join(chr(0x1D4EA + i) for i in range(26))
    )
    fonts['𝕲𝖔𝖙𝖍𝖎𝖈 (گوتیک و سنگین)'] = (
        ''.join(chr(0x1D56C + i) for i in range(26)) + 
        ''.join(chr(0x1D586 + i) for i in range(26))
    )
    fonts['𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎 (کدنویسی)'] = (
        ''.join(chr(0x1D670 + i) for i in range(26)) + 
        ''.join(chr(0x1D68A + i) for i in range(26))
    )
    fonts['ⓑⓤⓑⓑⓛⓔ (حبابی گرد)'] = (
        ''.join(chr(0x24B6 + i) for i in range(26)) + 
        ''.join(chr(0x24D0 + i) for i in range(26))
    )
    box = ''.join(chr(0x1F130 + i) for i in range(26))
    fonts['🅂🅀🅄🄰🅁🄴 (کادری مربعی)'] = box + box
    
    # اصلاح باگ ایموجی پرچم در حروف کوچک مینیاتوری
    sm_lower = 'ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ'
    fonts['Sᴍᴀʟʟ Cᴀᴘs (مینیاتوری)'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + sm_lower
    return fonts

FONT_STYLES_EN = generate_english_fonts()

def get_persian_styles(text: str):
    kasheedeh = re.sub(r'([بپتثجچحخدذرزژسشصضطظعغفقکگلمنهی])', r'\1ـــ', text)
    spaced = ' '.join(list(text.replace(' ', '')))
    return [
        ('👑 اساطیری و شاهانه', f'꧁༺ {text} ༻꧂'),
        ('亗 گنگ و کلنی', f'亗『 {text} 』亗'),
        ('☬ تیره و نمادین', f'☬ {text} ☬'),
        ('🌸 فانتزی گلدار', f'╰⊰⊹✿ {text} ✿⊹⊱╮'),
        ('★ ستاره‌ای استایلیش', f'★彡 {text} 彡★'),
        ('♡ قلبی و رمانتیک', f'•.¸♡ {text} ♡¸.•'),
        ('【 کادر ژاپنی 】', f'【 {text} 】'),
        ('𓊈 بال‌دار خاص 𓊉', f'𓊈 {text} 𓊉'),
        ('💎 الماس درخشان', f'✦ {text} ✦'),
        ('〰️ کشیده مجلسی', kasheedeh),
        ('➖ فاصله‌دار مدرن', spaced),
    ]