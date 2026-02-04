import gradio as gr

from llama3 import llama3
from OpenAIModel import OpenAIModel
def gradio_function(message, history):
    return llama3().chat(message)
gr.ChatInterface(gradio_function).launch()

#