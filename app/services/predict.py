import os
import numpy as np
from fastapi import HTTPException
from datetime import datetime
from app.core.response import json_response
from app.core.preproccess import preprocess_text
from app.core.logging_config import setup_logging
from app.schemas.schema import JournalSchema, Emotion, EmotionItem
from app.services.feedback import feedback_service

logger, _ = setup_logging()


async def predict_service(journal: JournalSchema, model) -> JournalSchema:
    threshold = 0.2
    try:
        if model is None:
            logger.error("Prediction Model Not Found")
            raise HTTPException(status_code=500, detail="Prediction model not found")
        if not journal.journalContent.strip():
            logger.error("Journal Text Empty")
            return json_response(
                status_code=400, message="Journal text cannot be empty"
            )

        logger.info("Starting prediction process for journal")

        # Predict emotions
        input_data = preprocess_text(journal.journalContent)
        predictions = model.predict(input_data)
        logger.debug(f"Predictions_raw: {predictions}")
        predictions = np.round(predictions, 3)
        logger.debug(f"Predictions: {predictions}")

        # Filter predictions by confidence threshold
        emotion_classes = [emotion.value for emotion in Emotion]
        emotion_data = [
            EmotionItem(emotion=emotion_classes[i], confidence=round(float(conf), 3))
            for i, conf in enumerate(predictions[0])
            if conf > threshold
        ]

        logger.debug(emotion_data)
        if not emotion_data:
            logger.warning("No emotions detected above threshold")

        # Update journal with results
        journal.emotionAnalysis = emotion_data
        journal.analyzedAt = datetime.now()

        # Generate feedback
        return await feedback_service(journal)

    except Exception as e:
        logger.error(f"Failed to predict: {e}", exc_info=True)
        return json_response(status_code=500, message="Something went wrong")
