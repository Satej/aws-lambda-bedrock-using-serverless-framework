import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def api(event, context):
    try:
        prompt = json.loads(event.get("body", "{}")).get("prompt", "")
    except (json.JSONDecodeError, AttributeError) as error:
        print(error)
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid JSON"})}

    if prompt == "":
        return {"statusCode": 400, "body": json.dumps({"message": "Please enter a prompt"})}

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0.6,
            "topP": 1
        }
    }

    try:
        bedrock_runtime_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
        response = bedrock_runtime_client.invoke_model(
            modelId="amazon.titan-text-lite-v1", body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        completion = response_body["results"][0]['outputText']
        
    except ClientError:
        logger.error("Couldn't invoke LLm")
        return {"statusCode": 500, "body": json.dumps({"message": "Internal Server Error"})}

    body = {
        "message": completion,
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}