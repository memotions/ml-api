import gc
import tensorflow as tf
from app.core.logging_config import setup_logging

logger, _ = setup_logging()


async def load_model(MODEL_URL):
    try:
        logger.debug(f"Load model from {MODEL_URL}...")
        model = tf.keras.models.load_model(MODEL_URL)
        return model

    except Exception as e:
        logger.error(f"Error in load_model: {e}", exc_info=True)
        raise ValueError(f"Load model failed: {e}")


async def unload_model(*models):
    for model in models:
        del model
    gc.collect()
