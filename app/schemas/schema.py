from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum


class Emotion(Enum):
    SAD = "Sad"
    HAPPY = "Happy"
    NEUTRAL = "Neutral"
    ANGER = "Anger"
    SCARED = "Scared"


class EmotionItem(BaseModel):
    result: Emotion
    confidence: float

    @field_validator("confidence", mode="before")
    def format_confidence(cls, value):
        return round(float(value), 4)


class JournalSchema(BaseModel):
    userId: int
    journalId: int
    journal: str
    emotion: list[EmotionItem] | None
    analyzedAt: datetime | str | None
    feedback: str | None
    createdAt: datetime | str | None
