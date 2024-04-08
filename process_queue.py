from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def call_llm(article:str, topic:str, bullet_points:str, openai_api_key:str, model:str = 'gpt-3.5-turbo'):
    print("Calling OPENAI....")
    template = """
    Write the next paragraph in the following article: {article}. DO NOT DEVIATE AWAY FROM THE BULLET POINTS. MAKE SURE TO ONLY INCLUDE FACTUAL INFORMATION IN THE BULLET POINTS. HOWEVER YOU ARE ALLOWED TO ELABORATE.

    Paragraph Topic: {topic}
    Bullet Points: {bullet_points}
    """
    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(api_key = openai_api_key, temperature = 0, model = model)

    chain = (
        {"article": RunnablePassthrough(), "topic": RunnablePassthrough(), "bullet_points": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke({"article": article, "topic": topic, "bullet_points": bullet_points})

    return response


def process_queue(my_queue, openai_api_key:str = OPENAI_API_KEY, model:str = 'gpt-3.5-turbo'):
    # Define variables
    article = ""
    topic = ""
    bullet_points = ""
    bullet_points_list = []
    paragraphs = []

    # While there are items in the queue loop through and create the next Paragraph in the sequence
    
    while my_queue.count > 0:
        print(my_queue.count)  # For testing purposes
        my_data = my_queue.dequeue() # Grabs data from the first item in the queue
        topic = my_data.paragraph   # Saves the Paragraph topic to use when calling the llm
        bullet_points = str(my_data.bullet_points) # Saves bulletpoints as string for use in llm
        bullet_points_list.append(my_data.bullet_points) # Saves bullet points in a list for use in cosine similarity function later
        response = call_llm(article, topic, bullet_points, openai_api_key, model) # Calls the llm and saves response
        paragraphs.append(response) # Appends the reponse to the paragraph list 
        article = article + "\n\n" + response # Adds the new Paragraph each time the llm is called to the current article
        print(article)

    # Return the article, paragraphs and bullet points list for further use
    return article, paragraphs, bullet_points_list