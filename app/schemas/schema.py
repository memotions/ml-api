from pydantic import BaseModel
from enum import Enum
    
class Emotion(Enum):
  SAD = 'Sad'
  HAPPY = 'Happy'
  NEUTRAL = 'Neutral'
  ANGER = 'Anger'
  SCARED = 'Scared'

class EmotionItem(BaseModel):
  result: Emotion
  confidence: int
    
class JournalSchema(BaseModel):
  userId: str
  journalId: str
  journal: str
  emotion: list[EmotionItem] | None
  feedback: str | None