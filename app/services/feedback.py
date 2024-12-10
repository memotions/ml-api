import os
import vertexai
from datetime import datetime
from fastapi import HTTPException
from vertexai.generative_models import GenerativeModel
from app.schemas.schema import JournalSchema
from app.services.pubsub import publish_to_pubsub
from app.core.logging_config import setup_logging
from app.core.response import json_response
from app.core.config import Config

logger, _ = setup_logging()


async def feedback_service(journal: JournalSchema):
    project_id = os.getenv("VERTEX_PROJECT_ID")
    model_location = os.getenv("GEN_MODEL_LOCATION")
    model_id = os.getenv("GEN_MODEL_ID")
    logger.debug(
        f"project_id = {project_id}, model_location = {model_location}, model_id = {model_id}"
    )
    if not project_id.strip() or not model_location.strip() or not model_id.strip():
        logger.error("Environment variables are present but invalid.")
        raise HTTPException(
            status_code=500,
            detail="Missing required environment variables: VERTEX_PROJECT_ID, MODEL_LOCATION, or GEN_MODEL_ID.",
        )

    try:
        # load model and generate response
        emotions = [emotion.emotion.value for emotion in journal.emotionAnalysis]
        input_data = f"{journal.journalContent}. Ini adalah mood {', '.join(emotions)}"
        logger.debug(f"Input data : {input_data}")
        logger.info("Generate feedback on journal")
        journal.feedback = await generate_feedback(
            input_data,
            project_id,
            model_location,
            model_id,
        )
        logger.debug(f"Generated Feedback: {journal.feedback}")
        journal.createdAt = datetime.now()

        # publish to pubsub
        await publish_to_pubsub(journal)

        return journal
    except Exception as e:
        logger.error(f"Generate Feedback failed : {e}")
        return json_response(status_code=500, message="Something went wrong")


async def generate_feedback(journal_text: str, project_id, model_location, model_id):
    try:
        vertexai.init(project=project_id, location=model_location)
        model = GenerativeModel(
            f"projects/{project_id}/locations/{model_location}/endpoints/{model_id}",
            system_instruction=[Config.SYSTEM_INSTRUCTION],
        )
        chat = model.start_chat()
        raw_response = chat.send_message(
            [journal_text],
            generation_config=Config.GENERATION_CONFIG,
            safety_settings=Config.SAFETY_SETTINGS,
        )
        logger.debug(f"raw response : {raw_response}")
        raw_response = raw_response.candidates[0].text
        result = " ".join(raw_response.split()).strip()
        return result
    except Exception as e:
        logger.error(f"Error generating feedback: {e}")
        return "Maaf, saat ini kami sedang tidak bisa memberikan feedback. Tapi tetap pantengin terus ya!"
