"""Pyzh2en
外交部中文名字轉拼音
"""

__version__ = "1.0"

import requests
import unicodedata
from pyquery import PyQuery


def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')


def _get_ch2en(name):
    payload = {
        "SN": name,
        "sound": 2,
    }
    url = "https://crptransfer.moe.gov.tw/index.jsp"
    res = requests.get(url, params=payload)
    S = PyQuery(res.text)
    
    # 找到包含威妥瑪拼音的行
    pinyin_row = S('th:contains("威妥瑪拼音")').closest('tr')
    
    # 確保找到了對應的行
    if pinyin_row:
        # 獲取拼音的span元素
        spans = pinyin_row.find('span.long')
        try:
            # 將每個span中的拼音文本提取出來
            pinyin_text = spans[0].text.upper()
            if len(spans) > 1:
                for span in spans[1:]:
                    # 將連接後的文本中的逗號與連字符合併
                    pinyin_text += "," + span.text.upper()
                # 將第二個span和第三個span中的拼音用連字符連接
                pinyin_text = pinyin_text.replace(",", "-", 0)
                # 將最後一個逗號轉換為連字符
                pinyin_text = pinyin_text.rsplit(",", 1)[0] + "-" + pinyin_text.rsplit(",", 1)[1]
                # 標準化
                pinyin_text = normalize_text(pinyin_text)
                return pinyin_text.replace("'", "")
            else:
                
                pinyin_text = normalize_text(pinyin_text)
                return pinyin_text.replace("'", "")
        except IndexError:
            return "No pinyin data found for the specified name."
    else:
        return "No pinyin data found for the specified name."


def ch2en(name, encode="威妥瑪拼音"):
    pinyin_text = _get_ch2en(name)
    if pinyin_text:
        return pinyin_text
    else:
        return "No pinyin data found for the specified name."
    
