import os
from fastapi import HTTPException
from google.cloud import pubsub_v1
from app.schemas.schema import JournalSchema
from app.core.logging_config import setup_logging
from app.core.response import json_response

logger, _ = setup_logging()


async def publish_to_pubsub(journal: JournalSchema):
    # Get env variables and set up pubsub
    publisher = pubsub_v1.PublisherClient()
    project_id = os.getenv("PROJECT_ID")
    topic_id = os.getenv("TOPIC_ID")
    # Handle id not found or set
    if not project_id or not topic_id:
        logger.error("Missing required environment variables")
        raise HTTPException(
            status_code=500,
            message="PROJECT_ID or TOPIC_ID environment variable is not set.",
        )

    # Convert pydantic schema into json
    journal_json = journal.model_dump_json()
    data_bytes = journal_json.encode("utf-8")

    logger.info(f"Preparing to publish message to Pub/Sub")
    logger.debug(f"Message payload: {journal_json}")

    # Publishing message
    try:
        topic_path = publisher.topic_path(project_id, topic_id)
        logger.debug(f"Publishing to topic: {topic_path}")
        future = publisher.publish(topic_path, data_bytes)
        result = future.result()
        logger.info(f"Message published successfully with ID: {result}")
        return result

    except Exception as e:
        logger.error(f"Failed to publish message to Pub/Sub: {e}", exc_info=True)
        return json_response(status_code=500, message="Something went wrong")
