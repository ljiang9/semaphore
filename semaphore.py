#!/usr/bin/env python3
"""semaphore: 把文本编码成旗语(Flag Semaphore)的 ASCII 示意图。

每个字母对应两只手臂的 8 个标准位置之一(45 度一档)。
位置编号采用发信人视角: 1=下, 2=左下, 3=左, 4=左上,
5=上, 6=右上, 7=右, 8=右下; 从 1 到 8 按"面对发信人"
的顺时针方向排列。示意图按面对发信人的视角绘制。
"""

import argparse
import sys

# 8 个标准手臂位置(发信人视角)
POSITIONS = {
    1: "下",
    2: "左下",
    3: "左",
    4: "左上",
    5: "上",
    6: "右上",
    7: "右",
    8: "右下",
}

# 标准旗语字母表。
# 规律: 字母按 (1,2)->(1,8), (2,3)->(2,8), ... 的顺序排列,
# 但 J、V、Y 三个字母打破规律(经公开旗语资料交叉核对):
#   J=(5,7)(兼作"字母模式"信号), V=(5,8), Y=(4,7);
#   (5,6)="数字模式", (4,8)="取消", 本工具只编码 A-Z。
LETTERS = {
    "A": (1, 2), "B": (1, 3), "C": (1, 4), "D": (1, 5),
    "E": (1, 6), "F": (1, 7), "G": (1, 8),
    "H": (2, 3), "I": (2, 4),
    "K": (2, 5), "L": (2, 6), "M": (2, 7), "N": (2, 8),
    "O": (3, 4), "P": (3, 5), "Q": (3, 6), "R": (3, 7),
    "S": (3, 8),
    "T": (4, 5), "U": (4, 6), "Y": (4, 7),
    "J": (5, 7), "V": (5, 8),
    "W": (6, 7), "X": (6, 8),
    "Z": (7, 8),
}

# 每个位置在 5x5 示意图(面对发信人视角)中的落点:
# (行, 列, 笔画)。对角线只画端点, 上下左右画两格。
_ARM_DRAW = {
    1: ((4, 2, "|"), (3, 2, "|")),
    2: ((3, 3, "\\"),),
    3: ((2, 4, "-"), (2, 3, "-")),
    4: ((1, 3, "/"),),
    5: ((0, 2, "|"), (1, 2, "|")),
    6: ((1, 1, "\\"),),
    7: ((2, 0, "-"), (2, 1, "-")),
    8: ((3, 1, "/"),),
}

_DIAGRAM_W = 5
_DIAGRAM_H = 5
_GAP = "  "


def render_letter(ch):
    """把单个字母渲染成 5 行 ASCII 小人, 返回行列表。"""
    pair = LETTERS[ch]
    grid = [[" "] * _DIAGRAM_W for _ in range(_DIAGRAM_H)]
    grid[2][2] = "o"  # 头/身体
    for pos in pair:
        for r, c, mark in _ARM_DRAW[pos]:
            grid[r][c] = mark
    return ["".join(row) for row in grid]


def blank_diagram():
    """空格: 5 行空白, 宽度与其他图一致。"""
    return [" " * _DIAGRAM_W for _ in range(_DIAGRAM_H)]


def render_text(text):
    """把文本渲染成横向排列的示意图, 每图下方标注字母。"""
    diagrams = []
    labels = []
    for ch in text:
        if ch == " ":
            diagrams.append(blank_diagram())
            labels.append(" " * _DIAGRAM_W)
        else:
            diagrams.append(render_letter(ch))
            labels.append(ch.center(_DIAGRAM_W))
    lines = []
    for row in range(_DIAGRAM_H):
        lines.append(_GAP.join(d[row] for d in diagrams))
    lines.append(_GAP.join(labels))
    return "\n".join(lines)


def print_table():
    """打印字母 -> (位置一, 位置二) 对照表。"""
    print("字母  手臂位置一  手臂位置二")
    print("-" * 30)
    for ch in sorted(LETTERS):
        p1, p2 = LETTERS[ch]
        print(f"  {ch}      {p1}({POSITIONS[p1]})      {p2}({POSITIONS[p2]})")


def parse_text(raw):
    """清洗输入: 转大写, 只允许 A-Z 和空格。"""
    text = " ".join(raw.upper().split())
    bad = sorted({ch for ch in text if ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ "})
    if bad:
        shown = "".join(bad[:5])
        raise ValueError(f"不支持的字符 {shown!r}, 只支持 A-Z 字母和空格")
    if not text:
        raise ValueError("输入为空, 请提供要编码的文本")
    return text


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="semaphore",
        description="把文本编码成旗语(Flag Semaphore)ASCII 示意图。",
    )
    ap.add_argument("text", nargs="?", help="要编码的文本(省略则从 stdin 读取)")
    ap.add_argument("--table", action="store_true", help="打印字母-手臂位置对照表")
    args = ap.parse_args(argv)

    if args.table:
        print_table()
        return 0

    raw = args.text
    if raw is None:
        raw = sys.stdin.read()
    try:
        text = parse_text(raw)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(render_text(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
