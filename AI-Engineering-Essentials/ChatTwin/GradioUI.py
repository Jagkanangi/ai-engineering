import gradio as gr

from llama3 import llama3
from OpenAIModel import OpenAIModel
llama3 = llama3()
# function to call gardio
def gradio_function(message, history):
    return llama3.chat(prompt=message)
gr.ChatInterface(gradio_function).launch()
 
#