"""
用 matplotlib 画 4 张架构图（不依赖 drawio）
输出: figures/3-1-arch.png, 3-2-usecase.png, 4-1-dataflow.png, 4-2-kg.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np

ROOT = r"C:\Users\a1442\Desktop\创新思维大作业\_work"
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

# 中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 配色
COLORS = {
    "blue": "#4A90E2",
    "green": "#50C878",
    "orange": "#F5A623",
    "red": "#E94B3C",
    "purple": "#9013FE",
    "gray": "#9B9B9B",
    "light_blue": "#D5E5F5",
    "light_green": "#D5F0DD",
    "light_orange": "#FCE5C5",
    "light_red": "#F8D7D2",
    "light_purple": "#E5D5F5",
    "light_gray": "#E5E5E5",
}

def draw_box(ax, x, y, w, h, text, fc="#4A90E2", ec="#2A5A92", tc="white", fs=11, bold=True):
    """画带圆角的矩形框"""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02",
        linewidth=1.5, edgecolor=ec, facecolor=fc
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text,
            ha="center", va="center",
            fontsize=fs, color=tc, weight="bold" if bold else "normal",
            wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color="#666", lw=1.5, style="->"):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=15,
        color=color, linewidth=lw
    )
    ax.add_patch(arrow)

# ============================================================
# 图 3.1 系统架构图
# ============================================================
print("[1/4] 图 3.1 系统架构图 ...")
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_aspect("equal")
ax.axis("off")

# 4 层 (从下到上: 数据层 → 算法层 → 应用层 → 表现层)
layers = [
    ("L1 表现层  Vue 3 + ECharts", 4.5, COLORS["blue"], [
        ("预警看板", 1.0, 5.0, 1.6, 0.6),
        ("个人详情", 3.0, 5.0, 1.6, 0.6),
        ("班级统计", 5.0, 5.0, 1.6, 0.6),
    ]),
    ("L2 应用层  Spring Boot 3", 3.4, COLORS["green"], [
        ("预警 API", 1.0, 3.9, 1.6, 0.6),
        ("SHAP 解释 API", 3.0, 3.9, 1.6, 0.6),
        ("KG 查询 API", 5.0, 3.9, 1.6, 0.6),
    ]),
    ("L3 算法层  XGBoost + TransE + SHAP", 2.3, COLORS["orange"], [
        ("XGBoost 分类器", 1.0, 2.8, 1.6, 0.6),
        ("TransE 嵌入", 3.0, 2.8, 1.6, 0.6),
        ("SHAP 解释器", 5.0, 2.8, 1.6, 0.6),
    ]),
    ("L4 数据层  MySQL 8 + Neo4j 5", 1.2, COLORS["purple"], [
        ("MySQL 行为日志", 1.5, 1.7, 2.0, 0.6),
        ("Neo4j 知识图谱", 4.0, 1.7, 2.0, 0.6),
    ]),
]

# 画层标题
for name, y, color, _ in layers:
    ax.text(0.2, y + 0.3, name, ha="left", va="center",
            fontsize=10, weight="bold", color=color)

# 画层背景 + 框
for i, (name, y, color, items) in enumerate(layers):
    # 层背景
    rect = Rectangle((0.4, y - 0.2), 7.0, 1.1, facecolor=COLORS["light_gray"], alpha=0.4, edgecolor="none")
    ax.add_patch(rect)
    # 框
    for x, _, w, h, _ in items:
        # x 和 h 在 items 里, 实际是 (text, x, y, w, h)
        pass

# 重新画（修正参数顺序）
for name, y, color, items in layers:
    for item in items:
        text, x, _, w, h = item
        draw_box(ax, x, y, w, h, text, fc=color, ec=color, tc="white", fs=9)

# 画层间箭头 (从上到下)
for i in range(3):
    src_y = layers[i][1] - 0.2  # 上层底部
    dst_y = layers[i+1][1] + 0.6  # 下层顶部
    draw_arrow(ax, 3.5, src_y, 3.5, dst_y, color="#666", lw=2)
    # 标注协议
    protocols = ["HTTP/REST", "JDBC", "Python RPC"]
    ax.text(3.8, (src_y + dst_y) / 2, protocols[i], fontsize=8, color="#666")

# 标题
ax.text(5, 5.7, "图 3.1  学业预警系统 4 层 B/S 架构图",
        ha="center", va="center", fontsize=13, weight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIG, "3-1-arch.png"), dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("    [完成] 3-1-arch.png")

# ============================================================
# 图 3.2 用例图
# ============================================================
print("[2/4] 图 3.2 用例图 ...")
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.5)
ax.set_aspect("equal")
ax.axis("off")

# 3 个 actor (左)
actors = [
    (1.0, 4.2, "教务管理者"),
    (1.0, 2.7, "辅导员"),
    (1.0, 1.2, "学生"),
]

# 6 个用例椭圆 (右)
usecases = [
    (5.5, 4.4, "查看全校预警看板"),
    (5.5, 3.6, "查看学院统计"),
    (5.5, 2.4, "查询班级预警名单"),
    (5.5, 1.6, "记录干预措施"),
    (5.5, 0.8, "查看个人预警等级"),
    (7.5, 0.8, "查看改进建议"),
]

# 画 actor
for x, y, name in actors:
    # 头部
    head = Circle((x, y + 0.25), 0.12, facecolor=COLORS["blue"], edgecolor="black")
    ax.add_patch(head)
    # 身体
    body = Rectangle((x - 0.15, y - 0.15), 0.3, 0.35, facecolor=COLORS["blue"], edgecolor="black")
    ax.add_patch(body)
    # 名字
    ax.text(x, y - 0.3, name, ha="center", va="top", fontsize=10, weight="bold")

# 画用例椭圆
for x, y, name in usecases:
    ellipse = mpatches.Ellipse((x, y), 2.4, 0.5, facecolor=COLORS["light_green"], edgecolor=COLORS["green"], linewidth=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, name, ha="center", va="center", fontsize=9)

# 画连线
connections = [
    # (actor_idx, usecase_idx)
    (0, 0),  # 教务管理者 - 全校看板
    (0, 1),  # 教务管理者 - 学院统计
    (1, 2),  # 辅导员 - 班级名单
    (1, 3),  # 辅导员 - 干预措施
    (2, 4),  # 学生 - 个人预警
    (2, 5),  # 学生 - 改进建议
]
for actor_i, uc_i in connections:
    ax_x, ax_y, _ = actors[actor_i]
    uc_x, uc_y, _ = usecases[uc_i]
    draw_arrow(ax, ax_x + 0.15, ax_y, uc_x - 1.2, uc_y, color="#444", lw=1.2)

# 标题
ax.text(5, 5.2, "图 3.2  学业预警系统用例图",
        ha="center", va="center", fontsize=13, weight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIG, "3-2-usecase.png"), dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("    [完成] 3-2-usecase.png")

# ============================================================
# 图 4.1 数据流图（核心创新）
# ============================================================
print("[3/4] 图 4.1 数据流图 ...")
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13)
ax.set_ylim(0, 5)
ax.set_aspect("equal")
ax.axis("off")

# 3 段式
# 左侧: 行为特征 (48 维)
# 中部: 知识图谱 (64 维)
# 右侧: 分类器 + 解释

# ----- 左侧 -----
draw_box(ax, 0.2, 3.5, 1.8, 0.7, "OULAD\n原始数据", fc=COLORS["light_gray"], ec="#666", tc="black", fs=9)
draw_box(ax, 0.2, 2.3, 1.8, 0.7, "4 类行为\n× 12 统计量", fc=COLORS["light_blue"], ec=COLORS["blue"], tc="black", fs=9)
draw_box(ax, 0.2, 1.1, 1.8, 0.7, "48 维\n行为特征", fc=COLORS["blue"], ec=COLORS["blue"], tc="white", fs=10, bold=True)

# ----- 中部 -----
draw_box(ax, 4.5, 3.5, 1.8, 0.7, "课程大纲 +\n教材目录", fc=COLORS["light_gray"], ec="#666", tc="black", fs=9)
draw_box(ax, 4.5, 2.3, 1.8, 0.7, "知识图谱\n(Neo4j)", fc=COLORS["light_purple"], ec=COLORS["purple"], tc="black", fs=9)
draw_box(ax, 4.5, 1.1, 1.8, 0.7, "TransE 64 维\n知识点嵌入", fc=COLORS["purple"], ec=COLORS["purple"], tc="white", fs=9, bold=True)
draw_box(ax, 4.5, 0.0, 1.8, 0.6, "注意力池化\n+ 行为序列", fc=COLORS["light_orange"], ec=COLORS["orange"], tc="black", fs=8)

# ----- 右侧 -----
draw_box(ax, 9.0, 2.3, 1.8, 0.7, "concat 拼接\n112 维融合", fc=COLORS["light_red"], ec=COLORS["red"], tc="black", fs=9)
draw_box(ax, 9.0, 1.1, 1.8, 0.7, "XGBoost\n分类器", fc=COLORS["red"], ec=COLORS["red"], tc="white", fs=10, bold=True)
draw_box(ax, 11.0, 1.1, 1.8, 0.7, "P(挂科)\n+ SHAP 解释", fc="#2C5F2D", ec="#1A3A1B", tc="white", fs=10, bold=True)

# 箭头
# 左侧
draw_arrow(ax, 1.1, 3.5, 1.1, 3.0, color="#666")
draw_arrow(ax, 1.1, 2.3, 1.1, 1.8, color="#666")
# 中部
draw_arrow(ax, 5.4, 3.5, 5.4, 3.0, color="#666")
draw_arrow(ax, 5.4, 2.3, 5.4, 1.8, color="#666")
draw_arrow(ax, 5.4, 1.1, 5.4, 0.6, color="#666")
# 跨段
draw_arrow(ax, 2.0, 1.4, 4.5, 0.3, color="#666", style="->")
# 到右侧
draw_arrow(ax, 6.3, 0.3, 9.0, 0.3, color="#444", lw=2)
draw_arrow(ax, 6.3, 1.4, 9.0, 2.0, color="#444", lw=2)
draw_arrow(ax, 10.8, 1.4, 11.0, 1.4, color="#444", lw=2)

# 标注
ax.text(3.0, 0.0, "行为特征\n(48 维)", ha="center", va="center", fontsize=8, color="#666", style="italic")
ax.text(7.5, 0.0, "知识点掌握度\n(64 维)", ha="center", va="center", fontsize=8, color="#666", style="italic")
ax.text(5.0, -0.2, "", ha="center")

# 标题
ax.text(6.5, 4.6, "图 4.1  学业预警系统数据流图（核心创新：行为特征 + KG 嵌入融合）",
        ha="center", va="center", fontsize=12, weight="bold")

# 底注
ax.text(6.5, 4.1, "知识图谱特征增强是关键创新点：TransE + 注意力池化得到 64 维知识掌握度向量，与 48 维行为特征拼接为 112 维融合特征",
        ha="center", va="center", fontsize=9, color="#444", style="italic")

plt.tight_layout()
plt.savefig(os.path.join(FIG, "4-1-dataflow.png"), dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("    [完成] 4-1-dataflow.png")

# ============================================================
# 图 4.2 知识图谱局部示例
# ============================================================
print("[4/4] 图 4.2 知识图谱局部 ...")
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.set_aspect("equal")
ax.axis("off")

# 中心: 贝叶斯定理
center_x, center_y = 5, 3.5
center = Circle((center_x, center_y), 0.5, facecolor=COLORS["red"], edgecolor="black", linewidth=2)
ax.add_patch(center)
ax.text(center_x, center_y, "贝叶斯\n定理", ha="center", va="center", fontsize=10, weight="bold", color="white")

# 上层: 4 个前置/相关
upper = [
    (2.0, 5.5, "条件概率"),
    (4.0, 5.8, "先验概率"),
    (6.0, 5.8, "后验概率"),
    (8.0, 5.5, "似然估计"),
]
upper_colors = [COLORS["blue"], COLORS["blue"], COLORS["blue"], COLORS["blue"]]
for (x, y, name), color in zip(upper, upper_colors):
    circle = Circle((x, y), 0.35, facecolor=color, edgecolor="black", linewidth=1.2)
    ax.add_patch(circle)
    ax.text(x, y, name, ha="center", va="center", fontsize=9, color="white", weight="bold")
    # 连线到中心
    draw_arrow(ax, x, y - 0.35, center_x, center_y + 0.5, color="#444", lw=1)
    # 关系标签
    mid_x, mid_y = (x + center_x) / 2, (y + center_y) / 2
    ax.text(mid_x, mid_y, "前置", fontsize=7, color="#666", style="italic")

# 下层: 2 个下游
lower = [
    (3.0, 1.2, "朴素贝叶斯\n分类器"),
    (7.0, 1.2, "贝叶斯网络"),
]
for x, y, name in lower:
    circle = Circle((x, y), 0.45, facecolor=COLORS["green"], edgecolor="black", linewidth=1.2)
    ax.add_patch(circle)
    ax.text(x, y, name, ha="center", va="center", fontsize=8, color="white", weight="bold")
    # 连线
    draw_arrow(ax, center_x, center_y - 0.5, x, y + 0.45, color="#444", lw=1)
    mid_x, mid_y = (x + center_x) / 2, (y + center_y) / 2
    ax.text(mid_x, mid_y, "应用", fontsize=7, color="#666", style="italic")

# 节点类型说明（左下角）
ax.text(0.2, 0.3, "图例：\n● 核心知识点\n● 前置知识点\n● 下游应用",
        ha="left", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS["light_gray"], edgecolor="gray"))

# 标题
ax.text(5, 6.6, "图 4.2  知识图谱局部示例（以\"贝叶斯定理\"为中心）",
        ha="center", va="center", fontsize=12, weight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIG, "4-2-kg.png"), dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("    [完成] 4-2-kg.png")

print("\n=== 4 张架构图全部生成 ===")
for f in ["3-1-arch.png", "3-2-usecase.png", "4-1-dataflow.png", "4-2-kg.png"]:
    fp = os.path.join(FIG, f)
    print(f"  {f}  ({os.path.getsize(fp)//1024} KB)")
