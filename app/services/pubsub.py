import os
from google.cloud import pubsub_v1
from app.schemas.schema import JournalSchema

def publish_to_pubsub(journal: JournalSchema):
  # get env variables and set up pubsub
  publisher = pubsub_v1.PublisherClient()
  project_id = os.getenv('PROJECT_ID')
  topic_id = os.getenv('TOPIC_ID')
  topic_path = publisher.topic_path(project_id, topic_id)
    
  # handle id not found or set
  if not project_id or not topic_id:
    raise ValueError("PROJECT_ID or TOPIC_ID environment variable is not set.")
  
  # convert pydantic schema into json
  journal_json = journal.model_dump_json()
  
  # convert json into bytes 
  data_bytes = journal_json.encode("utf-8")
  print(f"Project ID: {project_id}, Topic Path: {topic_path}")
  print(f'\nPUBLISHING MESSAGE {journal_json}\n')
  
  # publishing message
  try:
    future = publisher.publish(topic_path, data_bytes)
    result = future.result()
    print(f"Message published successfully with message ID: {result}")
  except Exception as e:
    print(f"Failed to publish message: {e}")