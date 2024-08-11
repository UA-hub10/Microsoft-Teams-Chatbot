import os
import requests
from monitoring import monitor
from dotenv import load_dotenv 
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

class Tools:
    @staticmethod
    @tool
    def Booking_Flight(input: str) -> str:
        """
        The queries focus on booking a flight involves searching for flights, selecting a preferred option based on price, schedule,
        and other factors, providing passenger details, choosing any additional services or add-ons, and completing the payment. 
        """
        response =  requests.get("http://Teams-api-env.eba-np6m9sbm.us-east-1.elasticbeanstalk.com/create-pnr",verify=False)
        monitor(query=input, api="/create-pnr")
        return response
    
    @staticmethod
    @tool
    def Update_Trip(input: str) -> str:
        """
        The queries focus on changing destination of a booked flight, they cover how to update the destination any fees or fare
        differences involved and whether the change can be done online or require customer service. 
        """
        response =  requests.get("http://Teams-api-env.eba-np6m9sbm.us-east-1.elasticbeanstalk.com/update-trip",verify=False)  
        monitor(query=input, api="/update-trip")
        return response

    @staticmethod
    @tool
    def Rescheduling(input: str) -> str:
        """
        The queries focus on rescheduling flights, addressing how to change flight dates, fees involved and the process 
        of rescheduling online or last minute.
        """
        response =  requests.get("http://Teams-api-env.eba-np6m9sbm.us-east-1.elasticbeanstalk.com/reschedule",verify=False) 
        monitor(query=input, api="/reschedule")
        return response

    @staticmethod
    @tool
    def Cancellation(input: str) -> str:
        """
        The queries revolve around how to cancel a booking and the process of requesting a refund or travel credit because of
        cancellation. Queries relate to cancellation policies for different ticket types including non-refundable fares and
        the timeframe for cancelling a flight before departure. 
        """
        response =  requests.get("http://Teams-api-env.eba-np6m9sbm.us-east-1.elasticbeanstalk.com/cancellation",verify=False)
        monitor(query=input, api="/cancellation")
        return response
    
    @staticmethod
    @tool
    def Irrelevant(input: str) -> str:
        """
         Any queries that are not related to booking flights, updating destination, rescheduling and cancelling the
         bookings.
        """
        # response =  requests.get("http://Teams-api-env.eba-np6m9sbm.us-east-1.elasticbeanstalk.com/irrelevant",verify=False)
        monitor(query=input, api="no api calls")
        return response

class Agents(Tools):
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("api_key")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=self.openai_api_key)
        self.tools = [Tools.Booking_Flight, Tools.Update_Trip, Tools.Rescheduling, Tools.Cancellation, Tools.Irrelevant]

    
    def Response(self, query):
        system = """
        You are a helpful assistant specialized in handling queries related to United Airlines.
        You have access to the following tools to assist with various tasks:

        1. Booking_Flight: Assists with booking flights.
        2. Update_Trip: Helps in updating existing trips.
        3. ReScheduling: Handles rescheduling of flights.
        4. Cancellation: Manages the cancellation of flights.
        5. Irrelevation: Identifies irrelevant queries and handles them appropriately.

        Please assist with questions related to United Airlines:
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system,
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=False)
        response = agent_executor.invoke({"input": query})
        return response


