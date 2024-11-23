import numpy as np
from datetime import datetime, timezone
from app.schemas.schema import JournalSchema, Emotion, EmotionItem
from app.services.feedback import feedback_service

async def predict_service(journal: JournalSchema, model) -> JournalSchema:
    threshold = 0.2
    try:
        # Format data
        input_data = np.array([journal.journal]).astype("object")
        print(f"Input data: {input_data}, type: {type(input_data)}")
        
        # Predict
        predictions = model.predict(input_data)
        print(f"Prediction result: {predictions}")
        
        # Identify classes above the threshold
        emotion_classes = [emotion.value for emotion in Emotion]
        emotion_data = [
            EmotionItem(result=emotion_classes[i], confidence=round(float(conf), 3))
            for i, conf in enumerate(predictions[0]) if conf > threshold
        ]
        
        # Specify datetime
        analyzed_at = datetime.now()
        
        # Assign data into journalSchema
        journal.emotion =  emotion_data
        journal.analyzedAt = analyzed_at
        
        # Generate feedback
        journal = await feedback_service(journal, model)
        return journal
    
    except Exception as e:
        # Handle and log errors
        print(f"Error during prediction: {e}")
        raise ValueError(f"Failed to generate prediction: {e}")
