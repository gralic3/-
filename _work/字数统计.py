import re
with open(r"C:\Users\a1442\Desktop\创新思维大作业\_work\论文初稿.md", "r", encoding="utf-8") as f:
    text = f.read()
# 移除 markdown 语法
text = re.sub(r'#+\s*', '', text)
text = re.sub(r'\*+', '', text)
text = re.sub(r'\$\$.*?\$\$', '公式', text, flags=re.DOTALL)
text = re.sub(r'<sub>(.*?)</sub>', r'_\1', text)
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'^\s*-\s+', '', text, flags=re.MULTILINE)
# 统计
chinese = re.findall(r'[\u4e00-\u9fff]', text)
total = len(text.replace(' ', '').replace('\n', ''))
print(f"中文字符数: {len(chinese)}")
print(f"总字符数 (含数字/英文): {total}")
print(f"估计正文字数 (中文字符 ÷ 0.85): {int(len(chinese) / 0.85)}")
