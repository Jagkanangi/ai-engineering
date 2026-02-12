import gradio as gr

from llama3 import llama3
from OpenAIModel import OpenAIModel
from tiktoken import encoding_for_model
import numpy as np
import ollama
import numpy as np
from CachingModel import CachingAIModel
# system_prompt = """Answer to only what is asked in the message. 
# Your profile is everything that is present between the tags <info>. 
# Additional information about your profile may also be embedded in the message along with the question that is asked.
# Any text that is present between the <info> tag is an addition to your profile. The text between the <info> tag is to help you answer the question. 
# If the question is specific to your profile and you don't have that information then you should respond with a statement "I don't have that information". Never make up any answers. 
# Never mention that you are looking at the info tag. When you respond your answer should not include any mention of the info tag. 

# <info>
# This is who you are; You are a seasoned software engineer. Your name is Jag. 
# You are a consultant who has worked in many different roles. From a developer, to a team lead, to an architect, to a manager.
# You took a sabbatical for between 2021 and 2025. You are not getting back into what you love doing the most.
# You have been working since 1997. You have worked in both the public as well as private sector. You also were the director of engineering for a startup.
# You love cooking. You also like to golf. You are a very good mentor.You enjoy teaching concepts to people. You were an expert in Java
# but now are looking to excel in AI. You have been furiously learning AI for the past few weeks. You can build and train LLMs including fine tuning
# for both classification and well as instruction.
# <info>"""

# additional_prompt = {"Where do you live?": "<info> You live in Toronto <info>", 
#                      "Where did you graduate from?": "<info> Your school was Madras University, India <info>",
#                      "What is your passion?": "<info> You are passionate about AI technology <info>",
#                      "What is your citizenship?" : "<info> You are a Canadian <info>"}

# llama3 = llama3(model_role_type=system_prompt)
cachingModel = CachingAIModel()
# function to call gardio
def input_guardrails(message : str) -> str:
    message = message.replace("<info>", "")
    message = message.replace("</info>", "")
    return message
def gradio_function(message, history):
    # message = input_guardrails(message)
    # value_in_dictionary = encode_and_compare(message)
    # message = value_in_dictionary +" If the info tag is present and it is relevant to the question thenyou can respond to the question using the text between the info tag. Do not mention the info tag in your response. " + message 
    # print(message)
    return cachingModel.chat(prompt=message)


# def encode_and_compare(message) -> str :
#     return_string : str = ""
#     message_embedd = ollama.embeddings(model='nomic-embed-text', prompt=message)
#     encoded_message = np.array(message_embedd['embedding'])
#     print(message_embedd)
#     for key, value in additional_prompt.items():
#         encoded_key = np.array(ollama.embeddings(model='nomic-embed-text', prompt=key)['embedding'])
#         similarity = np.dot(encoded_key, encoded_message) / (np.linalg.norm(encoded_key) * np.linalg.norm(encoded_message))
#         print(similarity)
#         if similarity > 0.7:
#             return_string = value
#             break
#     return return_string


gr.ChatInterface(gradio_function).launch(inbrowser=True)
 

#