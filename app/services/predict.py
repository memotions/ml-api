import numpy as np
from fastapi import HTTPException
from datetime import datetime
from app.core.response import json_response
from app.core.logging_config import setup_logging
from app.schemas.schema import JournalSchema, Emotion, EmotionItem
from app.services.feedback import feedback_service

logger, _ = setup_logging()


async def predict_service(journal: JournalSchema, model) -> JournalSchema:
    threshold = 0.2
    try:
        if model is None:
            raise HTTPException(status_code=404, detail="Prediction model not found")
        if not journal.journal.strip():
            raise HTTPException(status_code=400, detail="Journal text cannot be empty")

        logger.info("Starting prediction process for journal")

        # Predict emotions
        input_data = np.array([journal.journal]).astype("object")
        predictions = model.predict(input_data)
        logger.debug(f"Predictions: {predictions}")

        # Filter predictions by confidence threshold
        emotion_classes = [emotion.value for emotion in Emotion]
        emotion_data = [
            EmotionItem(result=emotion_classes[i], confidence=round(float(conf), 3))
            for i, conf in enumerate(predictions[0])
            if conf > threshold
        ]
        if not emotion_data:
            logger.warning("No emotions detected above threshold")

        # Update journal with results
        journal.emotion = emotion_data
        journal.analyzedAt = datetime.now()

        # Generate feedback
        return await feedback_service(journal, model)

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        return json_response(status_code=e.status_code, message=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return json_response(status_code=500, detail="Prediction failed")
