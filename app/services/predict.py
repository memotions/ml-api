import numpy as np
from datetime import datetime
from app.core.logging_config import setup_logging
from app.schemas.schema import JournalSchema, Emotion, EmotionItem
from app.services.feedback import feedback_service

logger, _ = setup_logging()


async def predict_service(journal: JournalSchema, model) -> JournalSchema:
    threshold = 0.2
    try:
        logger.info("Starting prediction process for journal")
        if not journal.journal.strip():
            raise ValueError("Journal text is empty")

        if model is None:
            raise ValueError("Prediction model is not loaded")

        # Format input data and predict
        input_data = np.array([journal.journal]).astype("object")
        logger.debug(f"Input data shape: {input_data.shape}")

        # Process predictions
        predictions = model.predict(input_data)
        logger.debug(f"Raw prediction values: {predictions}")

        # Format prediction result into pydantic schema
        emotion_classes = [emotion.value for emotion in Emotion]
        emotion_data = [
            EmotionItem(result=emotion_classes[i], confidence=round(float(conf), 3))
            for i, conf in enumerate(predictions[0])
            if conf > threshold
        ]

        if not emotion_data:
            logger.warning("No emotions detected above threshold")

        logger.info(f"Detected emotions: {[e.result for e in emotion_data]}")
        # Update journal
        journal.emotion = emotion_data
        journal.analyzedAt = datetime.now()

        # Generate feedback
        journal = await feedback_service(journal, model)

        return journal

    except Exception as e:
        logger.error(f"Error in predict_service: {e}", exc_info=True)
        raise ValueError(f"Prediction service failed: {e}")
