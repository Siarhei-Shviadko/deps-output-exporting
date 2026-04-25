from datetime import date

from pydantic import BaseModel, ConfigDict

FORBIDDEN_TO_CAMELIZE = frozenset(("__root__",))

__all__ = ["ConfiguredBaseModel"]


def snake_to_camel(snake: str) -> str:
    if snake in FORBIDDEN_TO_CAMELIZE:
        return snake
    snake_words = (
        snake_word.capitalize() if index else snake_word for index, snake_word in enumerate(snake.split("_"))
    )
    return "".join(snake_words)


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        alias_generator=snake_to_camel,
        json_encoders={
            date: lambda d: d.isoformat(),
        },
    )
