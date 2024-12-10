import gc
import os
import dotenv
import tensorflow as tf
from google.cloud import storage
from app.core.logging_config import setup_logging
from app.core.response import json_response

logger, _ = setup_logging()

async def load_model(MODEL_URL):
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    CLOUD_MODEL_PATH = os.getenv("CLOUD_MODEL_PATH")
    try:
        if not os.path.exists(MODEL_URL):
            if BUCKET_NAME and CLOUD_MODEL_PATH:
                logger.info(
                    f"Model not found locally. Attempting to download from cloud storage..."
                )
                await download_model_from_cloud(
                    BUCKET_NAME, CLOUD_MODEL_PATH, MODEL_URL
                )
            else:
                logger.error(
                    "Model not found locally and cloud storage details are not provided."
                )
                return json_response(500, "Something went wrong")

        logger.info(f"Load model from {MODEL_URL}...")
        model = tf.keras.models.load_model(MODEL_URL)
        return model

    except Exception as e:
        logger.error(f"Error loading model: {e}", exc_info=True)
        return json_response(404, "Model not found")


async def unload_model(model):
    del model
    gc.collect()


async def download_model_from_cloud(BUCKET_NAME, CLOUD_MODEL_PATH, destination):
    try:
        logger.info(
            f"Downloading model from cloud storage: {BUCKET_NAME}/{CLOUD_MODEL_PATH} to {destination}..."
        )
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(CLOUD_MODEL_PATH)
        blob.download_to_filename(destination)
        logger.info("Model download completed.")
    except Exception as e:
        logger.error(f"Error downloading model from cloud: {e}", exc_info=True)
        raise
