from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """
Without adding any additional information please take the following outline and write an informative 1000 word article about the topic. At least one sentence per bullet point but you can use more.

Outline:

{outline}

"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(api_key = OPENAI_API_KEY, temperature = 0)

chain = (
    {"outline": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

input = """
Title: The role of NPAS4 in the hippocampus.


Paragraph

- A heterogeneous population of inhibitory neurons controls the flow of information through a neural circuit.

-Inhibitory synapses that form on pyramidal neuron dendrites modulate the summation of excitatory synaptic potentials and prevent the generation of dendritic calcium spikes.

- Precisely timed somatic inhibition limits both the number of action potentials and the time window during which firing can occur. 

- The activity-dependent transcription factor NPAS4 regulates inhibitory synapse number and function in cell culture, but how this transcription factor affects the inhibitory inputs that form on distinct domains of a neuron in vivo was unclear. 

- Here we show that in the mouse hippocampus behaviourally driven expression of NPAS4 coordinates the redistribution of inhibitory synapses made onto a CA1 pyramidal neuron, simultaneously increasing inhibitory synapse number on the cell body while decreasing the number of inhibitory synapses on the apical dendrites. 

- This rearrangement of inhibition is mediated in part by the NPAS4 target gene brain derived neurotrophic factor (Bdnf), which specifically regulates somatic, and not dendritic, inhibition. 

-These findings indicate that sensory stimuli, by inducing NPAS4 and its target genes, differentially control spatial features of neuronal inhibition in a way that restricts the output of the neuron while creating a dendritic environment that is permissive for plasticity.



"""


response = chain.invoke(input)

print(response)