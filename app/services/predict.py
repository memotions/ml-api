import os
from transformers import BertTokenizer
import numpy as np
from fastapi import HTTPException
from datetime import datetime
from app.core.response import json_response
from app.core.logging_config import setup_logging
from app.schemas.schema import JournalSchema, Emotion, EmotionItem
from app.services.feedback import feedback_service

logger, _ = setup_logging()
MAX_LENGTH = 64


async def predict_service(journal: JournalSchema, model) -> JournalSchema:
    tokenizer = BertTokenizer.from_pretrained(os.getenv("BERT_MODEL_NAME"))
    logger.debug(f"Tokenizer : {tokenizer}")
    threshold = 0.2
    try:
        if model is None:
            logger.error("Prediction Model Not Found")
            raise HTTPException(status_code=500, detail="Prediction model not found")
        if not journal.journal.strip():
            logger.error("Journal Text Empty")
            return json_response(
                status_code=400, message="Journal text cannot be empty"
            )

        logger.info("Starting prediction process for journal")

        # input_data = np.array([journal.journal]).astype("object")
        encoded_sample = tokenize_data([journal.journal], tokenizer)

        # Predict emotions
        prediction = model.predict(
            {
                "input_ids": encoded_sample["input_ids"],
                "attention_mask": encoded_sample["attention_mask"],
            }
        )
        logger.debug(f"Predictions: {prediction}")

        # Filter predictions by confidence threshold
        emotion_classes = [emotion.value for emotion in Emotion]
        emotion_data = [
            EmotionItem(result=emotion_classes[i], confidence=round(float(conf), 3))
            for i, conf in enumerate(prediction[0])
            if conf > threshold
        ]
        if not emotion_data:
            logger.warning("No emotions detected above threshold")

        # Update journal with results
        journal.emotion = emotion_data
        journal.analyzedAt = datetime.now()

        # Generate feedback
        return await feedback_service(journal)

    except Exception as e:
        logger.error(f"Failed to predict: {e}", exc_info=True)
        return json_response(status_code=500, message="Something went wrong")


def tokenize_data(texts, tokenizer, max_len=MAX_LENGTH):
    return tokenizer(
        list(texts),
        max_length=max_len,
        truncation=True,
        padding="max_length",
        return_tensors="tf",
    )
