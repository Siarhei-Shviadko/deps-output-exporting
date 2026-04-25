from typing import Optional

__all__ = ["get_confidence_table_representation"]

NO_CONFIDENCE_SYMBOL = ""


def get_confidence_table_representation(confidence: Optional[float]) -> str:
    if confidence is None or confidence < 0:
        return NO_CONFIDENCE_SYMBOL
    return f"{confidence:.2f}"
