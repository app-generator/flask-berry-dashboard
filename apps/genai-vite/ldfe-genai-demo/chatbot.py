import os

from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain import PromptTemplate


apiKey = '5bebb595ea0a4ad7a657ec0682ce8745'
DEPLOYMENT_NAME = "gpt-35-turbo"

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://azo-ai-gpt.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = apiKey

llm = AzureChatOpenAI(model=DEPLOYMENT_NAME, temperature=1)

template = """
You are an assistant for question-answering tasks. Keep the answers as concise as possible.
\nQuestion: {query}  \nAnswer:
"""

prompt_template = PromptTemplate(
    input_variables=["query"],
    template=template
)

llm_chain = LLMChain(llm=llm, prompt=prompt_template)

zeroShotQuery = 'What is the capital of France?'
fewShotQuery = 'LLMs are great: positive. I hate RAG so much: negative. Few shot prompting is the worst: '
NoCOTQuery = ('Which is a faster way to get to work? Option 1: Take a 1000 minute bus, then a half hour train, '
              'and finally a 10 minute bike ride. Option 2: Take an 800 minute bus, then an hour train, and finally '
              'a 30 minute bike ride.')
COTQuery = ('Which is a faster way to get to work? Option 1: Take a 1000 minute bus, then a half hour train, '
              'and finally a 10 minute bike ride. Option 2: Take an 800 minute bus, then an hour train, and finally '
              'a 30 minute bike ride. Explain your reasoning including steps where you convert time to minutes first')
#query = input('Please enter your query: ')

print(llm_chain.invoke({'query': COTQuery})['text'])

