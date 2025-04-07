import os
import json
import hashlib
import random
import requests
from typing import Optional, Dict, Any

class TextTranslator:
    """文本翻译工具，使用百度翻译API"""
    
    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    
    def translate(self, text: str, from_lang: str = "jp", to_lang: str = "zh") -> str:
        """
        翻译文本
        
        Args:
            text: 需要翻译的文本
            from_lang: 源语言，默认日语
            to_lang: 目标语言，默认中文
            
        Returns:
            翻译后的文本
        """
        if not text.strip():
            return ""
            
        # 如果有API凭证，使用百度翻译API
        if self.app_id and self.app_key:
            try:
                salt = str(random.randint(32768, 65536))
                sign = hashlib.md5((self.app_id + text + salt + self.app_key).encode()).hexdigest()
                
                payload = {
                    'appid': self.app_id,
                    'q': text,
                    'from': from_lang,
                    'to': to_lang,
                    'salt': salt,
                    'sign': sign
                }
                
                response = requests.post(self.api_url, params=payload)
                result = response.json()
                
                if 'trans_result' in result:
                    return '\n'.join(item['dst'] for item in result['trans_result'])
                else:
                    print(f"翻译错误: {result.get('error_msg', '未知错误')}")
                    return ""
            except Exception as e:
                print(f"API调用失败: {str(e)}")
        
        # 如果没有API凭证或API调用失败，使用模拟翻译
        print("使用模拟翻译")
        
        # 模拟翻译结果（仅用于演示）
        if from_lang == "jp" and to_lang == "zh":
            if "日本語" in text:
                return "这是日语语音样本。这是语音识别测试。"
            return "模拟翻译：" + text[:10] + "..."
        else:
            return "模拟翻译结果"
    
    @staticmethod
    def get_language_code(language: str) -> str:
        """将语言名称转换为百度API支持的语言代码"""
        language_map = {
            "中文": "zh",
            "英语": "en",
            "日语": "jp",
            "韩语": "kor",
            "法语": "fra",
            "西班牙语": "spa",
            "俄语": "ru",
            "德语": "de"
        }
        return language_map.get(language, language)


if __name__ == "__main__":
    # 使用示例
    translator = TextTranslator(app_id="YOUR_APP_ID", app_key="YOUR_APP_KEY")
    result = translator.translate("これは日本語の音声サンプルです。音声認識テストです。")
    print(f"翻译结果: {result}")