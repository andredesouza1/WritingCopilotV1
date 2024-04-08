import streamlit as st
from typing import List
from create_queue import Node, Queue, Paragraph

from llm_queries import generate_bullet_points_llm

st.set_page_config(layout="wide")
#Define empty variables

if 'article' not in st.session_state:
    st.session_state["article"] = ""

if 'paragraphs' not in st.session_state:
    st.session_state["paragraphs"] = []

if "bullet_point_list" not in st.session_state:
    st.session_state["bullet_point_list"] = []    

if "sentence_comparison_data" not in st.session_state:
    st.session_state["sentence_comparison_data"] = []

if "select_model" not in st.session_state:
    st.session_state["select_model"] = 'gpt-3.5-turbo'


def save_value(key):
    st.session_state[key] = st.session_state["_"+key]
def get_value(key):
    st.session_state["_"+key] = st.session_state[key]
def instantiate_value(key):
    if key not in st.session_state:
        st.session_state[key] = ""




st.header('Alpha Version 0.0.1')
st.title('Create an Article')

openai_api_key = st.text_input('Enter OpenAI API Key')

select_model = st.selectbox("Select Model",["gpt-3.5-turbo (Cost $0.5 per 1M Tokens)", "gpt-4-0125-preview (Cost $10 per 1M tokens)"])

if select_model == "gpt-3.5-turbo (Cost $0.5 per 1M Tokens)":
    st.session_state["select_model"] = 'gpt-3.5-turbo'
elif select_model == "gpt-4-0125-preview (Cost $10 per 1M tokens)":
    st.session_state["select_model"] = 'gpt-4-0125-preview'

topic = st.text_input('Enter a Article Title')

number_of_paragraphs = st.number_input('Total number of paragraphs in the article', min_value=1)

for i in range(number_of_paragraphs):
    
    st.write(":black[_____________________________________________________________________________________]")
    paragraph = st.text_input(f'Enter Paragraph {i+1} Topic', key = "paragraph_" + str(i+1))

    bullet_point_number = st.number_input('Enter the number of bullet points', min_value=1, key = "bullet_point_number_" + str(i+1))


    for j in range(bullet_point_number):
        bullet_point = st.text_input(f'Enter bullet point {j+1}', key = "_" + str(i+1) + "_bullet_point_" + str(j+1), on_change = save_value, args=(str(i+1) + "_bullet_point_" + str(j+1),))
        instantiate_value(str(i+1) + "_bullet_point_" + str(j+1))

    generate_bullet_points = st.button(f"Generate Bullet Points for Paragraph {i+1} based on the following topic")

    topic_for_bullet_points = st.session_state["paragraph_" + str(i+1)]

    if generate_bullet_points:
        bullet_point_results = generate_bullet_points_llm(topic, topic_for_bullet_points, bullet_point_number, openai_api_key, st.session_state["select_model"])

        sentences = bullet_point_results.split("\n- ")
        sentences = [line.lstrip("- ") for line in bullet_point_results.split("\n") if line.strip()]

        print(sentences)

        # Print each sentence
        for index, sentence in enumerate(sentences):
            print("Sentence: ",sentence)
            st.session_state[str(i+1) + "_bullet_point_" + str(index+1)] = sentence
        
    for d in range(bullet_point_number):
        st.write( st.session_state[str(i+1) + "_bullet_point_" + str(d+1)]) 
        

st.write("=======================================================================")


# Creates the queue of paragraphs and bullet points
my_queue = Queue()

for i in range(number_of_paragraphs):
    new_data = Paragraph(f"{st.session_state['paragraph_' + str(i+1)]}")
    for j in range(st.session_state['bullet_point_number_' + str(i+1)]):
        new_data.bullet_points.append(st.session_state[ "_" + str(i+1) + "_bullet_point_" + str(j+1)])

    
    my_queue.enqueue(new_data)


from process_queue import process_queue

create_article = st.button('Create Article')

if create_article and openai_api_key != "":
    st.session_state["article"], st.session_state["paragraphs"], st.session_state["bullet_point_list"] = process_queue(my_queue, openai_api_key, st.session_state["select_model"])
if openai_api_key == "":
    warning = st.warning("Remember to add your OpenAI API Key before creating the article", icon="🤖")
else:
    warning = ""


col1, col2 = st.columns(2)


from text_splitting import split_text

with col2:
    dropdown_menu_bullet_points = []
    for i in st.session_state["bullet_point_list"]:
        for j in range(len(i)):
            dropdown_menu_bullet_points.append(i[j])
    select_bullet_point = st.selectbox("Bullet Points",options=dropdown_menu_bullet_points)

# Now that we are able to write an article we need to be able to take each bullet point and compare it to each sentence within the paragraph it generated. 

# Logic for calculating sentence similarity. Eventually make a helper function for this. We take the items in the bulletpoint list and pass it into the sentence similarity function to get the similarity score.
#Once we have the similarity score we should be able to manipulate the article in a variety of ways usuing heat maps
from sentence_similarity import calculate_sentences_similarity

calculate_similartiy_button = st.button("Calculate Similarity")

# Added so that we dont run this code every time we update the code
if calculate_similartiy_button:
    for index, paragraph in enumerate(st.session_state["paragraphs"]):
        indexed_bullet_point_list = st.session_state["bullet_point_list"][index]
        paragraph_sentences = split_text(paragraph)

        for i, j in enumerate(indexed_bullet_point_list):
            print("---------------------------------------------------------------")
            temp = [j]
            similarity_results = calculate_sentences_similarity(temp,paragraph_sentences)
            st.session_state["sentence_comparison_data"].append(similarity_results)

    
    

# I am using a lot of looping in this first pass try to think of ways to use more efficient search algorithms instead when rewriting this code TODO
# Will start with equals but may introduce some bugs down the line

#Article heatmap Alogrithms Below:



def top_three(article,sentence_comparison_data,selected_bullet_point):
    items_to_heatmap =[]
    for i in range(len(sentence_comparison_data)):
        if sentence_comparison_data[i][0][0].lower() in selected_bullet_point.lower():
            
            for j in range(3):
                items_to_heatmap.append(st.session_state["sentence_comparison_data"][i][j])
            

    color = ["green", "orange", "red"]
    colored_sentences = []

    for number, items in enumerate(items_to_heatmap):
        sentence = items[1]
        colored_sentence = f"<span style='background-color:{color[number]}; color:white'>{sentence}</span>"
        colored_sentences.append(colored_sentence)

    colored_article = article  # Initialize with the original article
    for colored_sentence in colored_sentences:
        colored_article = colored_article.replace(colored_sentence.split('>',1)[1].split('<',1)[0],colored_sentence)

    return colored_article

from color_pallete import heatmap_color

def seaborn_heatmap(article,sentence_comparison_data,selected_bullet_point):
    items_to_heatmap =[]
    
    for i in range(len(sentence_comparison_data)):
        if sentence_comparison_data[i][0][0].lower() in selected_bullet_point.lower():
            
            for j in range(len(sentence_comparison_data[i])):
                items_to_heatmap.append(st.session_state["sentence_comparison_data"][i][j])
            

    
    colored_sentences = []

    for number, items in enumerate(items_to_heatmap):
        sentence = items[1]
        color = heatmap_color(items_to_heatmap[number][2])
        
        colored_sentence = f"<span style='background-color:{color}; color:white;'>{sentence}</span>"
        colored_sentences.append(colored_sentence)

    colored_article = article  # Initialize with the original article
    for colored_sentence in colored_sentences:
        
        colored_article = colored_article.replace(colored_sentence.split('>',1)[1].split('<',1)[0],colored_sentence)

    return colored_article


with col1:
    function_choice = st.selectbox("Choose heatmap",["None","Top Three","Warm"])
    article = st.session_state["article"]
    colored_article = article
    
    match function_choice:
        case "Top Three":
            colored_article = top_three(article,st.session_state["sentence_comparison_data"],select_bullet_point)
        case "Warm":
            colored_article = seaborn_heatmap(article,st.session_state["sentence_comparison_data"],select_bullet_point)
    
    
    st.title("Article")
    st.markdown(colored_article, unsafe_allow_html=True)


st.write(st.session_state)