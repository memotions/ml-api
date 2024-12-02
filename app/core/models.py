import gc
import tensorflow as tf


from app.core.logging_config import setup_logging
from app.core.response import json_response

logger, _ = setup_logging()


async def load_model(MODEL_URL, TFBertModel):
    try:
        logger.debug(f"Load model from {MODEL_URL}...")
        model = tf.keras.models.load_model(
            "mood_classifier_bert.keras",
            custom_objects={"TFBertModel": TFBertModel},
        )
        return model

    except Exception as e:
        logger.error(f"Error loading model: {e}", exc_info=True)
        return json_response(404, "Model not found")


async def unload_model(model):
    del model
    gc.collect()
