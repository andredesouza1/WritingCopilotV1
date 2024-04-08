from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from typing import List
import random


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


def generate_bullet_points_llm( article_title:str, paragraph_topic:str, number:int, openai_api_key:str, model:str = 'gpt-3.5-turbo'): 

    generate_bullet_points_prompt = """

    You are an assistant for an article writer and editor. The Article Title is {article_title}. Your job is to come up with potential bullet points to help format a paragraph with the following topic {paragraph_topic}. The bullet points should be elaborated to make coherent points for the whole paragraph. CREATE {number} Bullet Points. ONLY PROVIDE THE BULLET POINTS AS SENTENCES FOR THE A RESPONSE. DO NOT NUMBER THEM OR DEMARCATE THEM IN ANY WAY. DO NOT PROVIDE ANY OTHER RESPONSE:


    """

    prompt = ChatPromptTemplate.from_template(generate_bullet_points_prompt)

    model = ChatOpenAI(api_key = openai_api_key, temperature = random.random() ** .7, model = model) # Random Temperature with a .7 skew

    chain = (
        {"article_title": RunnablePassthrough(), "paragraph_topic": RunnablePassthrough(), "number": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke({"article_title": article_title, "paragraph_topic": paragraph_topic, "number": number})

    return response


if __name__ == "__main__":

    input_number = 5

    result = generate_bullet_points_llm("The Impact of Climate Change on the Environment", "The impact of climate change on the environment is a topic that has been discussed for many years. The effects of climate change are becoming more and more evident as time goes on. The environment is changing rapidly, and it is important to understand the impact that this is having on the world around us. In this article, we will explore the impact of climate change on the environment and what can be done to mitigate these effects.", input_number, OPENAI_API_KEY, model = 'gpt-3.5-turbo')

    print(result)

    sentences = result.split(" - ")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Print each sentence
    for sentence in sentences:
        print(sentence)
