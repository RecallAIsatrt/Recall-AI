"""AI 服务 - DeepSeek API 调用"""
import httpx
from app.config import settings


async def chat_completion(messages: list[dict], temperature: float = 0.7) -> str:
    """调用 DeepSeek API 进行对话"""
    if not settings.DEEPSEEK_API_KEY:
        return _mock_response(messages[-1]["content"])

    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def analyze_mistake(content: str, subject: str) -> dict:
    """AI 分析错题"""
    messages = [
        {
            "role": "system",
            "content": (
                "你是一位经验丰富的教师，擅长分析学生的错题。"
                "请根据题目内容，给出：1. 错因分析 2. 正确解题思路 3. 知识点 4. 建议复习策略"
                "请以 JSON 格式返回：{error_type, analysis, knowledge_point, suggestion}"
            ),
        },
        {"role": "user", "content": f"学科：{subject}\n题目：{content}"},
    ]

    result = await chat_completion(messages, temperature=0.3)
    return {"raw": result}


async def generate_variant(content: str, subject: str) -> str:
    """生成变体题"""
    messages = [
        {
            "role": "system",
            "content": "你是一位出题专家，请根据原题生成一道同知识点但不同情境的变体题。只返回题目本身。",
        },
        {"role": "user", "content": f"学科：{subject}\n原题：{content}"},
    ]
    return await chat_completion(messages, temperature=0.8)


def _mock_response(user_input: str) -> str:
    """无 API Key 时的本地兜底回复"""
    return (
        f"收到你的问题：「{user_input[:50]}...」\n\n"
        "这是 AI 助手的模拟回复。配置 DeepSeek API Key 后可获得真实 AI 回答。\n\n"
        "**解题思路**：请仔细审题，注意关键词和条件。\n"
        "**错因分析**：常见错误包括概念混淆、计算失误、审题不清。\n"
        "**建议**：多练习同类题型，巩固知识点。"
    )
