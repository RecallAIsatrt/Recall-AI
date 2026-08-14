"""OCR 服务 - PaddleOCR 图片识别"""
import base64
import io
from pathlib import Path
from PIL import Image


class OCRService:
    def __init__(self):
        self._ocr = None

    def _get_ocr(self):
        if self._ocr is None:
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        return self._ocr

    async def recognize_image(self, image_data: str | bytes) -> dict:
        """
        识别图片中的文字
        :param image_data: base64 编码或文件路径
        :return: {text, confidence, lines}
        """
        try:
            if isinstance(image_data, str):
                if image_data.startswith("data:"):
                    image_data = image_data.split(",", 1)[1]
                img_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(img_bytes))
            else:
                img = Image.open(io.BytesIO(image_data))
        except Exception:
            return {"text": "", "confidence": 0, "lines": []}

        ocr = self._get_ocr()
        result = ocr.ocr(img, cls=True)

        lines = []
        full_text = []
        total_conf = 0

        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                conf = line[1][1]
                lines.append({"text": text, "confidence": round(conf, 3)})
                full_text.append(text)
                total_conf += conf

        count = len(lines) if lines else 1
        return {
            "text": "\n".join(full_text),
            "confidence": round(total_conf / count, 3) if lines else 0,
            "lines": lines,
        }


ocr_service = OCRService()
