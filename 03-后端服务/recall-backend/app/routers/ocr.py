"""OCR 识别路由"""
import base64
import httpx
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.config import settings
from app.services.ocr_service import ocr_service

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = await ocr_service.recognize_image(image_bytes)
    return result


class VisionAnalyzeRequest(BaseModel):
    image_base64: str  # data:image/...;base64,....
    model: str = "Qwen/Qwen3-VL-32B-Instruct"


@router.post("/analyze")
async def vision_analyze(req: VisionAnalyzeRequest):
    """视觉识别代理：图片 → 多模态模型 → 学科/知识点/题目/解析

    密钥只保存在后端（config.DEEPSEEK_API_KEY），前端不暴露。
    """
    if not settings.DEEPSEEK_API_KEY:
        return {"code": 50001, "message": "后端未配置 API Key"}

    prompt = (
        "请仔细识别图中的错题（可能是数学/物理/英语/化学/生物/语文/历史/地理之一），"
        "严格按以下四行输出（不要多余解释、不要 Markdown 代码块）：\n"
        "学科: [八选一]\n知识点: [一句话]\n题目: [图中的完整题目原文，逐字保留]\n解析: [2-4 句解题说明或答案]"
    )
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": req.model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": req.image_base64}},
                ],
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1200,
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            return {"code": 0, "data": {"reply": reply}}
    except Exception as e:  # noqa: BLE001
        return {"code": 50002, "message": f"视觉识别失败: {e}"}
