import boto3

from langchain.llms.bedrock import Bedrock
from langchain.retrievers.bedrock import AmazonKnowledgeBasesRetriever
from langchain.chains import RetrievalQA

from langchain.prompts import PromptTemplate

def LangChain(input: str,
    kbId: str,
    region: str = "us-east-1",
    # sessionId: str = None,  *check* is this needed with LangChain or does the framework retain context automatically ?
):
    
    # 1) LLM model set up
    bedrock_client = boto3.client("bedrock-runtime", region_name = 'us-east-1')

    claude_llm = Bedrock(
        model_id="anthropic.claude-v2:1",
        model_kwargs={"temperature": 0, "top_k": 10, "max_tokens_to_sample": 3000},
        client=bedrock_client,
)
    
    # 2) set up the LangChain retriever and specify number of results to return
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id=kbId,
        region_name=region,
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

    # set up the LangChain RetrievalQA and generate answers from the knowledge base:

    qa = RetrievalQA.from_chain_type(
        llm=claude_llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": llm_prompt_template()},
    )

    #[qa(q)["result"] for q in questions]

    return [qa(input)["result"]]

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
