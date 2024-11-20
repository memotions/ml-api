import gc
import tensorflow as tf

async def load_model(MODEL_URL):
  model = tf.keras.models.load_model(MODEL_URL)
  print(f'\nModel: {model} loaded from {MODEL_URL}...\n')
  return model

async def unload_model(*models):
    for model in models:
        del model  # Delete the model instance
    gc.collect()