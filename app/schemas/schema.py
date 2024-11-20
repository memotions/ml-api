from pydantic import BaseModel
from enum import Enum

class Emotion(Enum):
  SAD = 'sad'
  HAPPY = 'happy'
  NEUTRAL = 'neutral'
  ANGER = 'anger'
  SCARED = 'scared'
  
class Journal(BaseModel):
  userId: str
  journalId: str
  journal: str
  emotion: list[dict[Emotion, str]] | None
  feedback: str | None