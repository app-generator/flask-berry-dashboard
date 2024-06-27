import boto3
from langchain.llms.bedrock import Bedrock

from langchain.prompts import PromptTemplate

def rag_enhanced(input: str,
                 kbId: str,
                 regId: str = "us-east-1",):
    
    bedrock_client = boto3.client("bedrock-runtime", region_name = regId)
    bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name = regId) # *check* diff b/w bedrock-runtime and bedrock-agent-runtime

    claude_llm = Bedrock(
    model_id="anthropic.claude-v2:1",
    model_kwargs={"temperature": 0, "top_k": 10, "max_tokens_to_sample": 3000},
    client=bedrock_client,
    )
    
    response = bedrock_agent_client.retrieve(
        retrievalQuery={"text": input},
        knowledgeBaseId=kbId,
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": 3} # *check* what is 3 here ?
        },
    )    
    retrievalResults = response["retrievalResults"]

    contexts = get_contexts(retrievalResults)
    
    claude_prompt = llm_prompt_template()
    prompt = claude_prompt.format(context=contexts, question=input) # question NOT query_str for langchain step4 - see https://stackoverflow.com/questions/77839844/langchain-retrievalqa-missing-some-input-keys
    return claude_llm(prompt)

def get_contexts(retrievalResults):
        contexts = []
        for retrievedResult in retrievalResults:
            contexts.append(retrievedResult["content"]["text"])
        return " ".join(contexts)


def llm_prompt_template():

    # # question NOT query_str for langchain step4 - see https://stackoverflow.com/questions/77839844/langchain-retrievalqa-missing-some-input-keys
    PROMPT_TEMPLATE = """
    Human: You are an AI system working on forecast anomalies, and provides answers to questions \
    by using fact based and statistical information when possible.
    Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    <context>
    {context}
    </context>

    <question>
    {question}
    </question>

    The response should be specific and use statistics or numbers when possible.

    Assistant:"""

    claude_prompt = PromptTemplate(
        template=PROMPT_TEMPLATE, input_variables=["context", "question"] # question NOT query_str for langchain step4 - see https://stackoverflow.com/questions/77839844/langchain-retrievalqa-missing-some-input-keys
    )

    return claude_prompt
