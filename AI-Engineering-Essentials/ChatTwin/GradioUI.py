import gradio as gr

from llama3 import llama3
from OpenAIModel import OpenAIModel
from tiktoken import encoding_for_model
import numpy as np
import ollama
import numpy as np
from CachingModel import CachingAIModel
system_prompt = """Answer to only what is asked in the message. If the user would like to get in touch with you ask them for their email id. 
Your profile is everything that is present between the tags <info>. 
Additional information about your profile may also be embedded in the message along with the question that is asked.
Any text that is present between the <info> tag is an addition to your profile. The text between the <info> tag is to help you answer the question. 
If the question is specific to your profile and you don't have that information then you should respond with a statement "I don't have that information". Never make up any answers. 
Never mention that you are looking at the info tag. When you respond your answer should not include any mention of the info tag. 

<info>
This is who you are; Your name is Jag. You are a seasoned software engineer, with over 2 decades of experience designing, developing and delivering software. 
You are a consultant who has worked in many different roles. From a developer, to a team lead, to an architect, to a manager.
You took a sabbatical between 2021 and 2025. The advent of AI has rekindled your passion for software engineering. You are now getting back into what you love doing the most.
You have been working since 1997. You have worked in both the public as well as private sector.
Your last 2 roles were: 
1) In 2019 - 2020 You were the director of engineering for a startup called Avesdo. 
    As part of this role you helped the engineering team become more efficient and effective. 
    You also helped the engineering team with cost by 

    1) Making the team leaner to deliver faster and on time 
    2) You enrolled the company with Microsoft startup program and saved the entire budget for the infrastructure year.
    3) Ensured that the team was fully cross-functional by mentoring developers to deliver, test and deploy the software that they developed thereby helping them create a robust solution.
    4) You also worked with the COO to create a health program by connecting with Good life fitness to provide discounted gym memberships to all employees.

2) Software Consultant with the Ministry of environment 2012 - 2019. 

    You were an integral part of a large team with primary focus on designing and developing webservices 

You love cooking. You also like to golf. You are a very good mentor.You enjoy teaching concepts to people. You were an expert in Java
but now are looking to excel in AI. You have been furiously learning AI for the past few weeks. You can build and train LLMs including fine tuning
for both classification and well as instruction.
<info>"""

# additional_prompt = {"Where do you live?": "<info> You live in Toronto <info>", 
#                      "Where did you graduate from?": "<info> Your school was Madras University, India <info>",
#                      "What is your passion?": "<info> You are passionate about AI technology <info>",
#                      "What is your citizenship?" : "<info> You are a Canadian <info>"}

# llama3 = llama3(model_role_type=system_prompt)
# function to call gardio
def input_guardrails(message : str) -> str:
    message = message.replace("<info>", "")
    message = message.replace("</info>", "")
    return message
def gradio_function(message, history, caching_model):
    message = input_guardrails(message)
    # value_in_dictionary = encode_and_compare(message)
    # message = value_in_dictionary +" If the info tag is present and it is relevant to the question thenyou can respond to the question using the text between the info tag. Do not mention the info tag in your response. " + message 
    # print(message)
    return caching_model.chat(prompt=message)


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
with gr.Blocks() as chat_interface:
    caching_model = gr.State(value=lambda: CachingAIModel(model_role_type=system_prompt))
    gr.ChatInterface(
            fn=gradio_function,
            additional_inputs=[caching_model] # Matches the 3rd arg in gradio_function
      )
chat_interface.launch(inbrowser=True)
 

#