# -*- coding: utf-8 -*-
"""
ai_writer.py —— 调用 DeepSeek，让 AI 真正帮你写漫剧分镜脚本

这一版是"升级款"：模板模式只是随机填空，AI 模式才能写出有逻辑的剧情。
DeepSeek 的接口和 OpenAI 完全兼容，所以用 openai 这个库就能调。
"""

from openai import OpenAI


def 用AI生成脚本(api_key, 题材, 主角设定, 剧情梗概, 分镜数量):
    """
    把你的要求发给 DeepSeek，返回它写好的分镜脚本（一段文字）。

    参数说明：
        api_key     —— 你的 DeepSeek 密钥
        题材        —— 比如 "重生复仇 / 霸总 / 古风甜宠"
        主角设定    —— 比如 "女主：被家族抛弃的天才；男主：腹黑总裁"
        剧情梗概    —— 一句话剧情
        分镜数量    —— 想生成几个分镜
    """

    # 1) 创建客户端：base_url 指向 DeepSeek（这一行就是"连上 DeepSeek"）
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # 2) 写"提示词"——这是 AI 生成质量的关键，相当于给编剧的工作要求
    系统提示 = (
        "你是一名专业的短剧/漫剧编剧，擅长写节奏快、有反转、适合竖屏短视频的分镜脚本。"
        "你的脚本要能直接拿去做 AI 漫剧：每个分镜都要有【画面描述】（用于AI绘画）和【对白】（用于AI配音）。"
    )
    用户要求 = f"""请根据以下设定，写一份 {分镜数量} 个分镜的竖屏漫剧脚本。

题材：{题材}
主角设定：{主角设定}
剧情梗概：{剧情梗概}

【输出格式要求】严格按下面格式，每个分镜之间空一行：
【分镜 序号】
场景：xxx
画面：xxx（要具体、有画面感，方便AI绘画）
人物：xxx
对白：xxx（口语化、有冲突、能勾人）
情绪：xxx
"""

    # 3) 发请求给 DeepSeek（deepseek-chat 是它的对话模型）
    回复 = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": 系统提示},
            {"role": "user", "content": 用户要求},
        ],
        temperature=1.0,  # 1.0 比较稳；之前 1.3 太放飞，剧情会写得很"飘"
        stream=False,
    )

    # 4) 取出 AI 写好的正文返回
    return 回复.choices[0].message.content
