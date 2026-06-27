# -*- coding: utf-8 -*-
"""
批量生成.py —— 一次性批量生成多条漫剧脚本（"系统化量产"的核心）

工作原理：
    读取 任务清单.txt  →  逐行调用 DeepSeek 生成脚本  →  每条存成一个文件

运行方式：在 PyCharm 里打开本文件，点绿三角 ▶ 即可。
"""

import os
import sys
import re
import datetime

# Windows 控制台编码兜底，避免 emoji 报错
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import ai_writer          # 复用我们写好的"调用 DeepSeek"函数
import main               # 复用 main.py 里的"读取密钥"函数（import 不会触发它运行）

清单文件 = "任务清单.txt"


def 读取任务清单(路径):
    """
    把 任务清单.txt 读成一个任务列表。
    每行格式：题材 | 主角设定 | 剧情 | 分镜数
    用竖线 | 分隔；以 # 开头的行当成注释跳过。
    """
    任务们 = []
    with open(路径, "r", encoding="utf-8") as f:
        # enumerate 让我们一边读行、一边拿到行号（方便报错提示）
        for 行号, 原始行 in enumerate(f, start=1):
            行 = 原始行.strip()                 # 去掉行尾换行和首尾空格
            if not 行 or 行.startswith("#"):     # 空行、注释行 → 跳过
                continue
            字段 = 行.split("|")                 # 用 | 切成几段
            if len(字段) < 4:
                print(f"⚠️ 第 {行号} 行格式不对（需要4段，用 | 隔开），已跳过：{行}")
                continue
            题材 = 字段[0].strip()
            主角设定 = 字段[1].strip()
            剧情 = 字段[2].strip()
            数量原文 = 字段[3].strip()
            数量 = int(数量原文) if 数量原文.isdigit() else 6
            # 把一个任务打包成"元组"放进列表
            任务们.append((题材, 主角设定, 剧情, 数量))
    return 任务们


def 保存(内容, 题材, 序号):
    """每条脚本存一个文件，文件名前面加序号，保证不重名。"""
    安全题材 = re.sub(r'[\\/:*?"<>|\s]', "", 题材)[:20] or "脚本"
    时间 = datetime.datetime.now().strftime("%m%d_%H%M%S")
    os.makedirs("output", exist_ok=True)
    # {序号:02d} 表示两位数字、不足补0：1 → 01，2 → 02
    文件名 = f"output/{序号:02d}_{安全题材}_{时间}.txt"
    with open(文件名, "w", encoding="utf-8") as f:
        f.write(内容)
    return 文件名


def 批量跑():
    # 1) 检查密钥
    api_key = main.读取api_key()
    if not api_key:
        print("❌ 没读到 DeepSeek 密钥，请先配置好 config.py 再来。")
        return

    # 2) 检查清单文件
    if not os.path.exists(清单文件):
        print(f"❌ 找不到 {清单文件}，请先在同目录创建这个文件。")
        return

    # 3) 读取所有任务
    任务们 = 读取任务清单(清单文件)
    总数 = len(任务们)
    if 总数 == 0:
        print("⚠️ 任务清单是空的（或全是注释），没东西可生成。")
        return

    print(f"📋 共读到 {总数} 个任务，开始批量生成...\n")

    # 4) 核心：一个 for 循环，逐个生成
    成功 = 0
    for i, (题材, 主角设定, 剧情, 数量) in enumerate(任务们, start=1):
        print(f"[{i}/{总数}] 正在生成：{题材} ...", end=" ", flush=True)
        try:
            结果 = ai_writer.用AI生成脚本(api_key, 题材, 主角设定, 剧情, 数量)
            路径 = 保存(结果, 题材, i)
            print(f"✅ 已存 {路径}")
            成功 += 1
        except Exception as e:
            # 单条失败不影响其他条继续跑
            print(f"❌ 失败：{e}")

    print(f"\n🎉 全部完成！成功 {成功}/{总数} 条，文件都在 output 文件夹里。")


if __name__ == "__main__":
    批量跑()
