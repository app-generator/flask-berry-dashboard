import os
import mysql.connector
import pandas as pd
from apps.analytics import lollipop_policy as lp
from apps.analytics import create_sql_prompt as pol
import openai

def main(input: str,
     **kwargs
):
    
    lollipop_response = lp.main(input)

    if lollipop_response == 'data':
        return nlp2sql(input)
    else:
        return lollipop_response

def nlp2sql(
    input: str,
     **kwargs
):

    openai.api_key = os.getenv("")

    local_host = os.getenv("RDS_HOST")
    local_user = os.getenv("RDS_USER")
    local_pwd = os.getenv("RDS_PASSWORD")


    conn = mysql.connector.connect(host=local_host, 
                                user=local_user, 
                                password=local_pwd, 
                                database="rr_core")

    history = kwargs.get('history', None)
    

    # formulate OpenAI prompt
    prompt = pol.create_message(conn, query = input, history=history)


    # transform prompt into OpenAI format
    converted_message = [
        {
        "role": "system",
        "content": prompt.system
        },
        {
        "role": "user",
        "content": prompt.user
        }
        ]

    response = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = converted_message,
            temperature = 0.3,
            max_tokens = 256)

    # extract sql query from response
    sql = response.choices[0].message.content
    sql = sql.replace("```", "") # get rid of ``` in query
    #sql = sql[4:] # remove first 5 characters i.e. sql\n
    start_of_query = sql.find("SELECT")
    end_of_query = sql.find(";")
    sql = sql[start_of_query:end_of_query+1] # start from there

    # test the OpenAI generated SQL query
    # 
    result = pd.read_sql_query(sql, con=conn)

    conn.close()

    return result

# debug

# print(nlp2sql("Hello"))

# print(main("Who is Taylor Swift"))

# print(main("Whats up!"))

# *check* struggling with these - thinks they are data questions
# print(main("What is euro 2024 ?"))
# print(main("Who is the favourite to win euro 2024 ?"))

# print(main("How many inference jobs failed this morning"))

# print(nlp2sql("Could you break that down by client ?",
#               history = ["How many inference jobs failed this morning",
#                          "What was the main anomaly in the last 7 days ?"]))
