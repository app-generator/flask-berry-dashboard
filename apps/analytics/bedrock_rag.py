import boto3

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name = 'us-east-1')

def retrieveAndGenerate(
    input: str,
    kbId: str,
    region: str = "us-east-1",
    sessionId: str = None,
    model_id: str = "anthropic.claude-v2", # changed from "anthropic.claude-v2:1",
):
    model_arn = f"arn:aws:bedrock:{region}::foundation-model/{model_id}"

    if sessionId:
        return bedrock_agent_client.retrieve_and_generate(
            input={"text": input},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kbId,
                    "modelArn": model_arn,
                },
            },
            sessionId=sessionId,
        )

    else:
        return bedrock_agent_client.retrieve_and_generate(
            input={"text": input},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kbId,
                    "modelArn": model_arn,
                },
            },
        )



