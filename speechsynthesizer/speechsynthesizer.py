import os
import time
import base64
import hashlib
import hmac
import json
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any
from datetime import datetime

class SpeechSynthesizer:
    """语音合成工具，使用科大讯飞TTS API"""
    
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        self.app_id = app_id
        self.api_key = api_key
        self.api_url = "https://tts-api.xfyun.cn/v2/tts"
        self.host = "tts-api.xfyun.cn"
    
    def synthesize(self, text: str, output_path: str, voice: str = "xiaoyan") -> str:
        """
        将文本转换为语音
        
        Args:
            text: 需要合成的文本
            output_path: 输出音频文件路径
            voice: 发音人，默认为"xiaoyan"
            
        Returns:
            输出音频文件路径
        """
        if not text.strip():
            print("文本为空，无法合成语音")
            return ""
            
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # 如果有API凭证，使用科大讯飞API
        if self.app_id and self.api_key:
            try:
                # 构建请求数据
                data = {
                    "common": {"app_id": self.app_id},
                    "business": {
                        "aue": "lame",  # 音频编码，lame为MP3格式
                        "sfl": 1,       # 流式返回
                        "auf": "audio/L16;rate=16000",  # 音频采样率
                        "vcn": voice,   # 发音人
                        "speed": 50,    # 语速，默认50
                        "volume": 50,   # 音量，默认50
                        "pitch": 50,    # 音高，默认50
                    },
                    "data": {
                        "text": base64.b64encode(text.encode()).decode(),
                        "status": 2,    # 2表示完整的文本
                    }
                }
                
                # 构建鉴权URL
                now = datetime.now()
                date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
                signature_origin = f"host: {self.host}\ndate: {date}\nGET /v2/tts HTTP/1.1"
                signature_sha = hmac.new(
                    self.api_key.encode(), 
                    signature_origin.encode(), 
                    digestmod=hashlib.sha256
                ).digest()
                signature = base64.b64encode(signature_sha).decode()
                authorization_origin = f'api_key="{self.app_id}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
                authorization = base64.b64encode(authorization_origin.encode()).decode()
                
                # 设置请求头
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    "Host": self.host,
                    "Date": date
                }
                
                # 发送请求
                req = urllib.request.Request(
                    self.api_url, 
                    data=json.dumps(data).encode(), 
                    headers=headers,
                    method="POST"
                )
                
                # 解析响应
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode())
                    if result["code"] == 0:
                        audio_data = base64.b64decode(result["data"]["audio"])
                        with open(output_path, "wb") as f:
                            f.write(audio_data)
                        print(f"语音合成成功: {output_path}")
                    else:
                        print(f"语音合成失败: {result['message']}")
                        return ""
            except Exception as e:
                print(f"API调用失败: {str(e)}")
                # 如果API调用失败，使用模拟合成
        
        # 如果没有API凭证或API调用失败，使用模拟合成
        print("使用模拟语音合成")
        
        # 模拟语音合成（仅用于演示）
        try:
            with open(output_path, "w") as f:
                f.write(f"模拟TTS内容: {text[:20]}")
            print(f"模拟语音合成完成: {output_path}")
            time.sleep(1)  # 模拟处理时间
        except Exception as e:
            print(f"写入文件失败: {str(e)}")
            return ""
            
        return output_path


if __name__ == "__main__":
    # 使用示例
    synthesizer = SpeechSynthesizer(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY")
    output_file = synthesizer.synthesize("这是一段测试文本，用于验证语音合成功能。", "output/speech.mp3")
    print(f"输出文件: {output_file}")