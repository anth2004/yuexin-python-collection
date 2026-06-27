# -*- coding: utf-8 -*-
"""
main.py —— 主程序，运行的就是这个文件

运行方式（在这个文件夹里打开 Git Bash 或终端）：
    py main.py

它会让你选两种模式：
    1) 模板模式 —— 不花钱，随机填空，用来理解"可替换内容"的原理
    2) AI 模式  —— 用你的 DeepSeek 真生成剧情（需要先配置好 config.py）
"""

import os
import sys
import re
import random
import datetime

# 【Windows 必加】控制台默认是 GBK 编码，打印 emoji/特殊字符会报错。
# 这行强制用 UTF-8 输出，避免 UnicodeEncodeError 崩溃。
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 从我们自己写的两个文件里，把需要的函数导入进来
import templates
import ai_writer


def 读取api_key():
    """
    尝试读取 DeepSeek 密钥：优先读 config.py，没有就返回 None。
    （这样即使你还没配置 key，模板模式也能正常用。）
    """
    try:
        import config
        key = config.DEEPSEEK_API_KEY
        if key and key.startswith("sk-"):
            return key
        return None
    except ImportError:
        return None


def 保存到文件(内容, 题材):
    """把生成结果存成一个 .txt 文件，放进 output 文件夹。"""
    # 【健壮性】绝不能直接拿用户输入当文件名！
    # Windows 文件名里不允许出现 \ / : * ? " < > | 这些字符，空白也清掉，
    # 再截断到 20 个字，避免名字过长或非法导致 open() 报错。
    安全题材 = re.sub(r'[\\/:*?"<>|\s]', "", 题材)[:20]
    if not 安全题材:
        安全题材 = "脚本"
    时间 = datetime.datetime.now().strftime("%m%d_%H%M%S")
    文件名 = f"output/{安全题材}_{时间}.txt"
    # 确保 output 文件夹存在
    os.makedirs("output", exist_ok=True)
    with open(文件名, "w", encoding="utf-8") as f:
        f.write(内容)
    return 文件名


def 模板模式():
    """不花钱：从词库随机抽内容，按模板拼出一份分镜骨架。"""
    print("\n=== 模板模式（随机生成骨架，不花钱）===")
    题材 = input("题材（直接回车用默认'重生复仇'）：").strip() or "重生复仇"
    数量 = input("生成几个分镜（直接回车用默认 5）：").strip()
    数量 = int(数量) if 数量.isdigit() else 5

    全部分镜 = []
    for i in range(1, 数量 + 1):
        一个分镜 = templates.用模板做一个分镜(
            镜号=i,
            场景=random.choice(templates.词库["场景"]),
            画面描述=random.choice(templates.词库["画面描述"]),
            人物="女主、男主",
            对白="（这里填台词，模板模式只给骨架）",
            情绪=random.choice(templates.词库["情绪"]),
        )
        全部分镜.append(一个分镜)

    结果 = f"题材：{题材}\n" + "\n".join(全部分镜)
    print("\n" + 结果)
    路径 = 保存到文件(结果, 题材)
    print(f"\n✅ 已保存到：{路径}")


def ai模式(api_key):
    """用 DeepSeek 真生成剧情。"""
    print("\n=== AI 模式（DeepSeek 真生成）===")
    题材 = input("题材（如 重生复仇/霸总/古风甜宠）：").strip() or "重生复仇"
    主角设定 = input("主角设定（如 女主被家族抛弃的天才，男主腹黑总裁）：").strip() or "女主：被退婚的落魄千金；男主：深藏不露的商业大佬"
    剧情梗概 = input("一句话剧情：").strip() or "女主重生回到被退婚那天，誓要让所有人付出代价"
    数量 = input("生成几个分镜（默认 6）：").strip()
    数量 = int(数量) if 数量.isdigit() else 6

    print("\n⏳ 正在让 DeepSeek 写脚本，请稍等...")
    try:
        结果 = ai_writer.用AI生成脚本(api_key, 题材, 主角设定, 剧情梗概, 数量)
    except Exception as e:
        print(f"\n❌ 调用失败：{e}")
        print("常见原因：key填错了 / 账户没余额 / 没联网。")
        return

    print("\n" + 结果)
    路径 = 保存到文件(结果, 题材)
    print(f"\n✅ 已保存到：{路径}")


def main():
    print("=" * 40)
    print("    🎬 漫剧分镜脚本生成器 v1")
    print("=" * 40)

    api_key = 读取api_key()
    if api_key:
        print("✓ 已检测到 DeepSeek 密钥，两种模式都能用。")
    else:
        print("ⓘ 没检测到密钥，先用模板模式（配置 config.py 后可解锁 AI 模式）。")

    print("\n请选择：")
    print("  1 = 模板模式（不花钱）")
    print("  2 = AI 模式（DeepSeek 真生成）")
    选择 = input("输入 1 或 2：").strip()

    if 选择 == "2":
        if api_key:
            ai模式(api_key)
        else:
            print("\n⚠️ 还没配置密钥，没法用 AI 模式。先去复制 config_example.py 成 config.py 填上 key。")
    else:
        模板模式()


# 这一行是 Python 的固定写法：表示"直接运行本文件时，执行 main()"
if __name__ == "__main__":
    main()
