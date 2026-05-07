#!/usr/bin/env python3
"""Find report evidence leads for a claim. This script does not make the verdict."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def keywords(claim: str) -> list[str]:
    domain_terms = [
        "预制菜",
        "预制",
        "半预制",
        "复热预制",
        "只是加热",
        "加热一下",
        "餐厅现做",
        "门店现做",
        "加工等级",
        "原料来源",
        "原料加工",
        "冷链",
        "配送",
        "制作工艺",
        "做法",
        "营养成分",
        "热量",
        "检测",
        "检验报告",
        "溯源二维码",
        "二维码",
        "扫码",
        "梅菜扣肉",
        "中央厨房",
        "所有菜品",
        "槽头肉",
        "淋巴肉",
        "劣质肉",
        "不新鲜",
        "过期",
        "变质",
        "异物",
        "防腐剂",
        "添加剂",
        "供应商",
        "分量",
        "卫生",
        "投诉",
    ]
    synonyms = {
        "门店现做": ["餐厅现做"],
        "预制菜": ["预制", "半预制", "复热预制"],
        "只是加热": ["复热预制", "餐厅复热"],
        "加热一下": ["复热预制", "餐厅复热"],
        "做法": ["制作工艺", "餐厅操作工艺"],
        "冷链": ["冷链运输", "配送周期"],
        "所有菜品": ["餐厅现做", "半预制", "复热预制"],
        "槽头肉": ["五花肉", "原料来源", "检验报告"],
        "淋巴肉": ["五花肉", "原料来源", "检验报告"],
        "劣质肉": ["原料来源", "供应商", "检验报告"],
        "不新鲜": ["冷链运输", "配送周期", "原料配送"],
        "过期": ["配送周期", "冷链运输", "检验报告"],
        "变质": ["检验报告", "冷链运输", "配送周期"],
        "异物": ["检验报告", "顾客反馈"],
        "防腐剂": ["配料", "检验报告"],
        "添加剂": ["配料", "检验报告"],
        "扫码": ["二维码", "菜品溯源卡", "食材检验报告"],
        "二维码": ["菜品溯源卡", "食材检验报告"],
        "分量": ["顾客反馈", "改善"],
        "卫生": ["顾客反馈", "检验报告"],
        "投诉": ["顾客反馈", "改善"],
    }

    tokens: list[str] = []
    for term in domain_terms:
        if term in claim:
            tokens.append(term)
            tokens.extend(synonyms.get(term, []))

    tokens.extend(re.findall(r"[A-Za-z0-9]+", claim))
    if not tokens:
        tokens = re.findall(r"[\u4e00-\u9fff]{2,4}", claim)

    stop = {"报告", "老乡鸡", "是否", "是不是", "有没有", "可以", "全部", "所有"}
    seen: set[str] = set()
    result: list[str] = []
    for token in tokens:
        if token in stop or token in seen:
            continue
        seen.add(token)
        result.append(token)
    return result[:8]


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: check_claim.py "<claim>"', file=sys.stderr)
        return 2

    claim = sys.argv[1]
    terms = keywords(claim)
    if not terms:
        print("No useful search terms found.")
        return 0

    print("Evidence leads. Review the snippets and decide using references/fact-check-rules.md.\n")
    for term in terms:
        print(f"## Search: {term}", flush=True)
        subprocess.run([sys.executable, str(SCRIPT_DIR / "search_report.py"), term, "--limit", "5"], check=False)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
