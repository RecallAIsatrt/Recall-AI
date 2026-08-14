"""导出服务 - PDF / Markdown"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


def export_to_pdf(mistakes: list[dict], title: str = "Recall 错题集") -> bytes:
    """将错题导出为 PDF"""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], fontSize=18, spaceAfter=12))
    styles.add(ParagraphStyle(name="Question", parent=styles["Normal"], fontSize=12,
                              textColor=colors.HexColor("#1D1D1F"), spaceAfter=6))
    styles.add(ParagraphStyle(name="Analysis", parent=styles["Normal"], fontSize=11,
                              textColor=colors.HexColor("#10B981"), spaceAfter=4, leftIndent=12))
    styles.add(ParagraphStyle(name="Meta", parent=styles["Normal"], fontSize=9,
                              textColor=colors.grey, spaceAfter=12))

    story = []
    story.append(Paragraph(title, styles["Title2"]))
    story.append(Paragraph(f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Meta"]))
    story.append(Spacer(1, 8*mm))

    for i, m in enumerate(mistakes, 1):
        story.append(Paragraph(f"{i}. {m.get('title', '')}", styles["Question"]))
        story.append(Paragraph(f"题目：{m.get('content', '')}", styles["Question"]))
        if m.get("ai_analysis"):
            story.append(Paragraph(f"AI 解析：{m['ai_analysis']}", styles["Analysis"]))
        meta = f"学科：{m.get('subject', '')} | 知识点：{m.get('knowledge_point', '')} | 复习 {m.get('review_count', 0)} 次"
        story.append(Paragraph(meta, styles["Meta"]))
        story.append(Spacer(1, 4*mm))

    doc.build(story)
    return buf.getvalue()


def export_to_markdown(mistakes: list[dict], title: str = "Recall 错题集") -> str:
    """将错题导出为 Markdown"""
    lines = [f"# {title}", "", f"> 导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    for i, m in enumerate(mistakes, 1):
        lines.append(f"## {i}. {m.get('title', '')}")
        lines.append("")
        lines.append(f"**学科**：{m.get('subject', '')} | **知识点**：{m.get('knowledge_point', '')}")
        lines.append("")
        lines.append(f"**题目**：{m.get('content', '')}")
        lines.append("")
        if m.get("ai_analysis"):
            lines.append(f"> **AI 解析**：{m['ai_analysis']}")
            lines.append("")
        lines.append(f"---")
        lines.append("")

    return "\n".join(lines)
