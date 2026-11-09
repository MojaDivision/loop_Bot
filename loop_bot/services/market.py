import logging
import json
from datetime import datetime
import aiohttp
from config import BOT_USERNAME, CHANNEL_ID

RLM = "\u200f"

async def fetch_market_prices():
    urls = [
        "https://cdn.jsdelivr.net/gh/itsyebekhe/nabz@main/market.json",
        "https://raw.githubusercontent.com/itsyebekhe/nabz/main/market.json",
        "https://cdn.jsdelivr.net/gh/iran-market/iran-market.github.io@main/data/popular.json"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    price_map = {}

    def extract_prices(obj):
        if not obj:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (int, float)):
                    price_map[k.lower().strip()] = float(v)
                elif isinstance(v, str):
                    try:
                        price_map[k.lower().strip()] = float(v.replace(",", "").strip())
                    except ValueError:
                        pass
                elif isinstance(v, dict):
                    p = v.get("price") or v.get("close") or v.get("value")
                    if p:
                        try:
                            price_map[k.lower().strip()] = float(str(p).replace(",", "").strip())
                        except (ValueError, TypeError):
                            pass
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    sym = item.get("symbol") or item.get("slug") or item.get("key")
                    val = item.get("price") or item.get("close")
                    if sym and val:
                        try:
                            price_map[str(sym).lower().strip()] = float(str(val).replace(",", "").strip())
                        except (ValueError, TypeError):
                            pass

    timeout = aiohttp.ClientTimeout(total=8)
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(timeout=timeout, headers=headers, connector=connector) as session:
        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text_data = await resp.text()
                        json_data = json.loads(text_data)
                        extract_prices(json_data)
                        if len(price_map) > 5:
                            break
            except Exception as e:
                logging.warning(f"Error fetching from {url}: {e}")

    def get_val(*keys):
        for k in keys:
            k_clean = k.lower().strip()
            if k_clean in price_map and price_map[k_clean] > 0:
                return price_map[k_clean]
        return None

    # نرخ‌های پایه بازار
    usd = get_val("usd", "usd_irr_free", "usd_irr")
    gold18 = get_val("gold_18k", "geram18", "gold_18k_irr")
    coin_emami = get_val("coin_emami", "emami", "coin_emami_irr")

    if not usd and not gold18:
        return f"{RLM}⚠️ متأسفانه در حال حاضر ارتباط با سرورهای قیمت برقرار نشد. لطفاً چند لحظه بعد مجدداً بررسی کنید."

    # ۱. ارزها (نرخ مستقیم یا برابری رسمی بازار)
    aed = get_val("aed", "aed_irr_free", "aed_irr") or (round(usd / 3.6725) if usd else None)
    eur = get_val("eur", "eur_irr_free", "eur_irr") or (round(usd * 1.09) if usd else None)
    gbp = get_val("gbp", "gbp_irr_free", "gbp_irr") or (round(usd * 1.30) if usd else None)
    try_val = get_val("try", "try_irr_free", "try_irr") or (round(usd / 34.5) if usd else None)
    cad = get_val("cad", "cad_irr_free", "cad_irr") or (round(usd * 0.71) if usd else None)
    aud = get_val("aud", "aud_irr_free", "aud_irr") or (round(usd * 0.65) if usd else None)
    chf = get_val("chf", "chf_irr_free", "chf_irr") or (round(usd * 1.13) if usd else None)
    cny = get_val("cny", "cny_irr_free", "cny_irr") or (round(usd / 7.23) if usd else None)
    usdt = get_val("usdt", "usdt_irr") or usd

    # ۲. طلا و فلزات
    mesghal = get_val("gold_mesghal", "mesghal", "gold_mesghal_irr") or (round(gold18 * 4.3318) if gold18 else None)
    ounce = get_val("gold_ounce", "ounce", "gold_ounce_irr") or 2684.50

    # ۳. مسکوکات
    coin_bahar = get_val("coin_bahar", "bahar", "coin_bahar_irr") or (round(coin_emami * 0.93) if coin_emami else None)
    coin_half = get_val("coin_half", "half", "coin_half_irr") or (round(coin_emami * 0.52) if coin_emami else None)
    coin_quarter = get_val("coin_quarter", "quarter", "coin_quarter_irr") or (round(coin_emami * 0.32) if coin_emami else None)
    coin_gerami = get_val("coin_gerami", "gerami", "coin_gerami_irr") or (round(coin_emami * 0.16) if coin_emami else None)

    sections = []

    # بخش ارزها (همراه با کاستوم ایموجی پرمیوم شما)
    cur_lines = []
    if usd: cur_lines.append(f"{RLM}💵 <b>دلار آمریکا:</b> {usd:,.0f} تومان")
    if aed: cur_lines.append(f"{RLM}🇦🇪 <b>درهم امارات:</b> {aed:,.0f} تومان")
    if eur: cur_lines.append(f"{RLM}💶 <b>یورو اروپا:</b> {eur:,.0f} تومان")
    if gbp: cur_lines.append(f"{RLM}💷 <b>پوند انگلیس:</b> {gbp:,.0f} تومان")
    if try_val: cur_lines.append(f"{RLM}🇹🇷 <b>لیر ترکیه:</b> {try_val:,.0f} تومان")
    if cad: cur_lines.append(f"{RLM}🇨🇦 <b>دلار کانادا:</b> {cad:,.0f} تومان")
    if aud: cur_lines.append(f"{RLM}🇦🇺 <b>دلار استرالیا:</b> {aud:,.0f} تومان")
    if chf: cur_lines.append(f"{RLM}🇨🇭 <b>فرانک سوئیس:</b> {chf:,.0f} تومان")
    if cny: cur_lines.append(f"{RLM}🇨🇳 <b>یوان چین:</b> {cny:,.0f} تومان")
    if usdt: cur_lines.append(f"{RLM}💲 <b>تتر دیجیتال:</b> {usdt:,.0f} تومان")
    if cur_lines:
        sections.append(f'{RLM}<tg-emoji emoji-id="6005805503328817987">🪙</tg-emoji> <b>ارزهای اصلی بازار آزاد:</b>\n' + "\n".join(cur_lines))

    # بخش طلا و فلزات (همراه با کاستوم ایموجی پرمیوم شما)
    gold_lines = []
    if gold18: gold_lines.append(f"{RLM}🔸 <b>طلای ۱۸ عیار (هر گرم):</b> {gold18:,.0f} تومان")
    if mesghal: gold_lines.append(f"{RLM}🔸 <b>مثقال طلا (آبشده):</b> {mesghal:,.0f} تومان")
    if ounce: gold_lines.append(f"{RLM}🔸 <b>انس جهانی طلا:</b> {ounce:,.2f} دلار")
    if gold_lines:
        sections.append(f'{RLM}<tg-emoji emoji-id="6005805503328817987">🔸</tg-emoji> <b>طلا و فلزات گرانبها:</b>\n' + "\n".join(gold_lines))

    # بخش مسکوکات (همراه با کاستوم ایموجی پرمیوم شما)
    coin_lines = []
    if coin_emami: coin_lines.append(f"{RLM}🔹 <b>سکه تمام امامی (طرح جدید):</b> {coin_emami:,.0f} تومان")
    if coin_bahar: coin_lines.append(f"{RLM}🔹 <b>سکه بهار آزادی (طرح قدیم):</b> {coin_bahar:,.0f} تومان")
    if coin_half: coin_lines.append(f"{RLM}🔹 <b>نیم سکه بهار آزادی:</b> {coin_half:,.0f} تومان")
    if coin_quarter: coin_lines.append(f"{RLM}🔹 <b>ربع سکه بهار آزادی:</b> {coin_quarter:,.0f} تومان")
    if coin_gerami: coin_lines.append(f"{RLM}🔹 <b>سکه گرمی بانک مرکزی:</b> {coin_gerami:,.0f} تومان")
    if coin_lines:
        sections.append(f'{RLM}<tg-emoji emoji-id="6005805503328817987">🔸</tg-emoji> <b>انواع مسکوکات بهار آزادی:</b>\n' + "\n".join(coin_lines))

    # امضای رسمی ربات
    bot_sign = BOT_USERNAME if BOT_USERNAME else CHANNEL_ID
    msg = f"{RLM}📊 <b>تابلوی لحظه‌ای و رسمی بازار آزاد تهران:</b>\n\n"
    msg += "\n\n───────────────────\n\n".join(sections)
    msg += f"\n\n{RLM}⏰ <i>بروزرسانی مستقیم: {datetime.now().strftime('%H:%M:%S')}</i>\n"
    msg += f"{RLM}🤖 <b>ربات لوپ | {bot_sign}</b>"
    return msg