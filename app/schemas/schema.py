from pydantic import BaseModel
from enum import Enum
    
class Emotion(Enum):
  SAD = 'sad'
  HAPPY = 'happy'
  NEUTRAL = 'neutral'
  ANGER = 'anger'
  SCARED = 'scared'

class EmotionItem(BaseModel):
  result: Emotion
  confidence: int
    
class JournalSchema(BaseModel):
  userId: str
  journalId: str
  journal: str
  emotion: list[EmotionItem] | None
  feedback: str | None