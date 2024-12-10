import joblib
import numpy as np
import re

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app.core.logging_config import setup_logging

logger, _ = setup_logging()


with open("word_to_index80.pkl", "rb") as f:
    word_to_index = joblib.load(f)


def clean_text(text):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.lower()
    text = stopword.remove(text)
    return text


def tokenize_text(text):
    return re.findall(r"\b\w+\b", text)


def indices_token(text, word_to_index):
    return [word_to_index.get(token, 0) for token in text]


def padding_text(tokens):
    return pad_sequences([tokens], maxlen=53, padding="post", truncating="post")[0]


def preprocess_text(text):
    logger.debug(f"Input Text : {text}")
    text = clean_text(text)
    logger.debug(f"Clean Text : {text}")
    text = tokenize_text(text)
    logger.debug(f"Tokenize Text : {text}")
    logger.debug(f"Stemming : {text}")
    text = indices_token(text, word_to_index)
    logger.debug(f"indices : {text}")
    text = padding_text(text)
    logger.debug(f"Padding Text : {text}")
    return np.array([text])
