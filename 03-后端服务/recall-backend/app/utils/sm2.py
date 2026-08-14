"""SM-2 间隔重复算法实现"""
from datetime import datetime, timedelta


def sm2(quality: int, easiness: float, interval: int, repetition: int) -> dict:
    """
    SM-2 算法
    :param quality: 回忆质量 0-5
        5 - 完美
        4 - 犹豫后正确
        3 - 困难但正确
        2 - 错误但似曾相识
        1 - 错误且陌生
        0 - 完全不记得
    :param easiness: 易度因子 (>=1.3)
    :param interval: 间隔天数
    :param repetition: 重复次数
    :return: dict with easiness, interval, repetition, next_review
    """
    if quality >= 3:
        if repetition == 0:
            interval = 1
        elif repetition == 1:
            interval = 6
        else:
            interval = round(interval * easiness)
        repetition += 1
    else:
        repetition = 0
        interval = 1

    easiness = max(1.3, easiness + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    next_review = datetime.utcnow() + timedelta(days=interval)

    return {
        "easiness": round(easiness, 2),
        "interval": interval,
        "repetition": repetition,
        "next_review": next_review,
    }


def get_mastery_level(review_count: int, avg_quality: float) -> float:
    """计算掌握度 0-1"""
    if review_count == 0:
        return 0.0
    base = min(review_count / 8.0, 1.0)
    quality_factor = avg_quality / 5.0
    return round(min(base * quality_factor, 1.0), 2)
