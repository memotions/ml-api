import os
from vertexai.generative_models import SafetySetting


class Config:
    # System Instruction
    SYSTEM_INSTRUCTION = """Tolong berikan saran atau motivasi hanya dalam satu paragraf yang terdiri dari setidaknya lima kalimat, sesuai dengan mood dari user."""

    # Generation Configuration
    GENERATION_CONFIG = {
        "max_output_tokens": 400,
        "temperature": 1,
        "top_p": 1,
    }

    # Safety Settings
    SAFETY_SETTINGS = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        ),
    ]
