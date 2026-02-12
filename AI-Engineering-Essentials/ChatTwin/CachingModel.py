import os
import openai
import instructor
from instructor import Instructor
from AbstractModel import AbstractChatClient
from litellm import completion, ModelResponse, Choices, CustomStreamWrapper
from pydantic import BaseModel, Field
from typing import Union
import requests

class WeatherReport(BaseModel):
    city: str
    country: str
    temperature: float = Field(..., alias="temperature_2m")
    humidity: int = Field(..., alias="relative_humidity_2m")
    units: str = "Celsius"

    class Config:
        populate_by_name = True # Allows using both alias and field name

class Weather(BaseModel):
    city: str = Field(description="Name of the city", )

class GeneralChat(BaseModel):
    message : str = Field(description="Response to the message")

class Common(BaseModel):
    choice : Union[GeneralChat, Weather]
    
class CachingAIModel(AbstractChatClient):
    def __init__(self, model_name="openai/gpt-5-nano-2025-08-07", model_key="", model_role_type="You are an assistant"):
        super().__init__(model_name, model_key, model_role_type=model_role_type)
        # self.client = instructor.from_litellm(completion)
        self.client : Instructor
        self.initialize_client()

    def initialize_client(self):
        """
        Initializes the OpenAI client.
        """
        self.client = instructor.from_litellm(completion)

    def chat(self, prompt, temperature=0, max_tokens=500, model=None, print_messages = True) -> str:
        """
        Gets a completion from the OpenAI API.
        """
        content : str | None = None
        """
        user can change model but maintain context from the previous conversation
        """
        if model is None:
            model = self.model_name
        """
        add the prompt to the context
        """    
        self.add_message(self.USER_ROLE, prompt)
        response : Common
        try:             
            response = self.client.chat.completions.create(
                model=model,
                messages=self.get_messages(),
                response_model=Common)
            if(isinstance(response.choice, GeneralChat)):
                content = response.choice.message
            else:
                content = response.choice.city
                weather_report = self.get_weather_object(content)
                if(weather_report is not None):
                    self.add_message(self.ASSISTANT_ROLE, content= "I will check the weather for you")
                    self.add_message(self.SYSTEM_ROLE, content=f"This is the weather in {content} is {weather_report.temperature}. Respond back to the user with the information I have given.")
                    chat_response = self.client.chat.completions.create(model=model, messages=self.get_messages(), response_model=GeneralChat)
                    if(isinstance(chat_response, GeneralChat)):
                        content = chat_response.message
                    else:
                        content = "I don't have that information"
            """
            add the response to the context
            """
            self.add_message(self.ASSISTANT_ROLE, content)
            if(print_messages):
                print(content)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        if (content is None):
            return "An error occurred during the chat. Response is empty"
        else: 
            return content

    def get_weather_object(self, city_name: str) -> WeatherReport:
        # 1. Geocode
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
        geo_res = requests.get(geo_url).json()["results"][0]
        
        # 2. Get Weather
        lat, lon = geo_res["latitude"], geo_res["longitude"]
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
        w_res = requests.get(w_url).json()["current"]
        
        # 3. Instantiate the Model
        return WeatherReport(
            city=geo_res["name"],
            country=geo_res["country"],
            **w_res # Unpacks temperature_2m and relative_humidity_2m directly
        )

    # Usage
