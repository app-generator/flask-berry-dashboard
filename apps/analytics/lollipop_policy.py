import os

import openai

def main(prompt: str):

  openai.api_key = os.getenv("OPENAI_API_KEY")

  # examples:
  # prompt = "hello"
  # prompt = "whats going on with this data"
  # prompt = "how many forecast runs were there yesterday"
  # prompt = "Yo!"
  # prompt = "hey hows it going"


  # *check* OpenAI how to add examples to help provide better responses (few-shot training)
  lollipop_policy = [
      {
        "role": "system",
        "content": """"Determine whether a user's question is:
        a) a greeting or small talk 
        b) a sports or general knowledge, chat-gpt type question like:

        - who was JFK ?
        - who is the likely to win the world cup ?

        or 
        c) a question related to forecasting, models, training, inference, labour demand, clients, sites, data e.g.

        - summarise the forecasts for me
        - what job errors are you seeing ?
        - what are the top 5 anomalies for client X

        If a) or b) reply with an appropriate conversational response and please don't state the classification of the question itself). 
        If c) just reply with 'data'."""
      },
      {
        "role": "user",
        "content": prompt
      },

      # {
      #   "role": "user",
      #   "content": "Hello! How are you today?"
      # },
      # {
      #   "role": "assistant",
      #   "content": "convo"
      # },
      # {
      #   "role": "user",
      #   "content": "How many failed forecast runs were there yesterday ?"
      # },
      # {
      #   "role": "assistant",
      #   "content": "data"
      # },
    ]

  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=lollipop_policy,                                                                                                                                            
    temperature=0.5,
    max_tokens=64,
    top_p=1
  )

  return(response.choices[0].message.content)
  # print(response.choices[0].message.content)                                                                                        
