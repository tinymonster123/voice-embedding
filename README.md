# Voice Embedding(苦逼学生版)

``BangDream It's mygo!!!!!``实在是太豪看了。因为难掩对``soyorin``的喜爱，所以想做一个``soyorin``的语音模型，但是感觉只是训练一个语音模型实在是太无聊了，于是就想着能不能做一点有趣的东西

```bash
graph TD
    A[用户视频] --> B(MCP网关)
    B --> C[音频分离工具]
    B --> D[语音识别工具]
    B --> E[机器翻译工具]
    B --> F[语音合成工具]
    B --> G[口型同步工具]
    B --> H[视频合成工具]
    C -->|分离后音频| D
    D -->|日文文本| E
    E -->|中文文本| F
    F -->|中文音频| G
    G -->|带口型数据| H
    H --> I[最终视频]
```