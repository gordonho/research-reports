#!/usr/bin/env python3
import re

with open('/Users/gordon/clawd/research-reports/2026-06-02-ai-agent-memory-coding-assistant.md', 'r') as f:
    md = f.read()

def md_to_html(text):
    lines = text.split('\n')
    html_lines = []
    in_table = False
    table_rows = []
    
    for line in lines:
        if line.startswith('## '):
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            level = line.count('#')
            tag = f'h{level}'
            content = re.sub(r'^#+\s+', '', line)
            html_lines.append(f'<{tag}>{content}</{tag}>')
        elif line.strip() == '---':
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            html_lines.append('<hr>')
        elif line.startswith('|'):
            parts = [c.strip() for c in line.split('|')[1:-1]]
            if all(re.match(r'^[-:]+$', c.replace(' ', '')) for c in parts):
                if table_rows:
                    html_lines.append('<table><thead><tr>')
                    for cell in table_rows[0]:
                        html_lines.append(f'<th>{cell}</th>')
                    html_lines.append('</tr></thead><tbody>')
                    for row in table_rows[1:]:
                        html_lines.append('<tr>')
                        for cell in row:
                            html_lines.append(f'<td>{cell}</td>')
                        html_lines.append('</tr>')
                    html_lines.append('</tbody></table>')
                    table_rows = []
                    in_table = True
            else:
                table_rows.append(parts)
        else:
            if in_table and line.startswith('|'):
                continue
            elif in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            if line.startswith('**'):
                parts = re.match(r'\*\*(.+?)\*\*(.*)', line)
                if parts:
                    html_lines.append(f'<li><strong>{parts.group(1)}</strong>{parts.group(2)}</li>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{re.sub(r"^- ", "", line)}</li>')
            elif line.startswith('* '):
                html_lines.append(f'<li>{re.sub(r"^\* ", "", line)}</li>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
    
    if in_table:
        html_lines.append('</tbody></table>')
    
    return '\n'.join(html_lines)

content = md_to_html(md)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent 记忆架构与编码助手：2026生产级进展 | Research Notes</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --primary: #001935; --accent: #00a8e8; --bg: #fafafa; --card-bg: #ffffff; --text: #444; --text-light: #888; --border: #e0e0e0; }}
        body {{ font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 16px; }}
        .header {{ background: var(--card-bg); border-bottom: 1px solid var(--border); padding: 20px 0; position: sticky; top: 0; z-index: 100; }}
        .header-inner {{ max-width: 840px; margin: 0 auto; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; }}
        .logo {{ font-size: 24px; font-weight: 700; color: var(--primary); text-decoration: none; letter-spacing: -0.5px; }}
        .logo span {{ color: var(--accent); }}
        .nav a {{ color: var(--text-light); text-decoration: none; margin-left: 24px; font-size: 14px; transition: color 0.2s; }}
        .nav a:hover {{ color: var(--accent); }}
        .main {{ max-width: 840px; margin: 40px auto; padding: 0 20px 80px; }}
        .report-meta {{ background: linear-gradient(135deg, #001935, #003366); color: white; padding: 20px 24px; border-radius: 12px; margin-bottom: 32px; font-size: 14px; }}
        .report-meta p {{ opacity: 0.85; margin-top: 4px; }}
        h1 {{ font-size: 32px; color: var(--primary); margin-bottom: 24px; line-height: 1.3; }}
        h2 {{ font-size: 22px; color: var(--primary); margin: 36px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--accent); }}
        h3 {{ font-size: 18px; color: var(--primary); margin: 24px 0 12px; }}
        h4 {{ font-size: 16px; color: var(--text); margin: 20px 0 10px; }}
        p {{ margin-bottom: 16px; color: var(--text); }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
        th {{ background: var(--primary); color: white; padding: 10px 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}
        tr:nth-child(even) td {{ background: #f8f9fa; }}
        ul, ol {{ margin: 12px 0 16px 24px; }}
        li {{ margin-bottom: 8px; }}
        strong {{ color: var(--primary); }}
        hr {{ border: none; border-top: 1px solid var(--border); margin: 32px 0; }}
        .highlight-box {{ background: #e8f4fd; padding: 16px 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid var(--accent); }}
        .footer {{ text-align: center; padding: 40px 20px; color: var(--text-light); font-size: 13px; border-top: 1px solid var(--border); margin-top: 60px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-inner">
            <a href="index.html" class="logo">Research<span>Notes</span></a>
            <nav class="nav">
                <a href="index.html">首页</a>
                <a href="daily_video_prompts.html">每日视频</a>
            </nav>
        </div>
    </div>
    <main class="main">
        <h1>AI Agent 记忆架构与编码助手：2026生产级进展深度报告</h1>
        <div class="report-meta">
            <strong>📄 报告日期</strong>：2026年6月2日<br>
            <strong>📂 报告类型</strong>：深度行业分析<br>
            <p>覆盖范围：记忆架构Token效率突破、Google Jules异步编码Agent、2026编码助手成本格局</p>
        </div>
        {content}
    </main>
    <div class="footer">
        本报告基于公开信息整理，仅供研究参考，不构成投资建议。
    </div>
</body>
</html>'''

with open('/Users/gordon/clawd/research-reports/2026-06-02-ai-agent-memory-coding-assistant.html', 'w') as f:
    f.write(html)

print('Done')
