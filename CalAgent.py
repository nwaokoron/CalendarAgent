
import datetime
from entities import EventDetails
import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# Specify a function declaration and parameters for an API request
# get_calendar_events = "get_calendar_events"

# get_product_sku_func = FunctionDeclaration(
#     name=get_product_sku,
#     description="Get the SKU for a product",
#     # Function parameters are specified in OpenAPI JSON schema format
#     parameters={
#         "type": "object",
#         "properties": {
#             "product_name": {"type": "string", "description": "Product name"}
#         },
#     },
# )


class CalAgent:
    def __init__(self, calendar):
        self.chat = None
        self.model = None
        self.calendar = calendar  # user calendar

        project_id = "wahala-solutions"
        vertexai.init(project=project_id, location="us-central1")

        get_calendar_events = "get_calendar_events"

        get_calendar_events_func = FunctionDeclaration(
            name=get_calendar_events,
            description="Get number of calendar events",
            # Function parameters are specified in OpenAPI JSON schema format
            parameters={
                "type": "object",
                "properties": {
                    "number_of_events": {"type": "integer", "description": "number of calendar events requested by user"}
                },
            },
        )

        
        create_calendar_event = "create_calendar_event"
        create_calendar_event_func = FunctionDeclaration(
            name=create_calendar_event,
            description="Create a calendar event",
            parameters={
                "type": "object",
                "properties": {
                    "event_name": {"type": "string", "description": "Name of the event"},
                    "start_time": {"type": "string", "description": "Start time of the event in ISO8601 format"},
                    "end_time": {"type": "string", "description": "End time of the event in ISO8601 format"},
                    "location": {"type": "string", "description": "Location of the event"},
                },
            }
        )

        # Define a tool that includes the above functions
        calendar_tools = Tool(
            function_declarations=[
                get_calendar_events_func,
                create_calendar_event_func
            ],
        )

        self.model = GenerativeModel(
            model_name="gemini-1.5-pro-preview-0514",
            generation_config=GenerationConfig(temperature=0.42),
            tools=[calendar_tools],
        )
        
        #self.chat = self.model.start_chat()


    def getChat(self):
        if self.chat is None:
            self.chat = self.model.start_chat()
        return self.chat
    
    def get_today_date(self):
        today = datetime.date.today()
        return today.strftime("%Y-%m-%d")
    
    def get_current_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")



    def start_chat(self):

        while True:
            prompt = ""
            if self.chat is None:
                # TODO: Add a more sophisticated prompt that better capture the agents duties and behavior(think response style, tone, awareness, Come up with unique event titles if the user for get's one. don't create events in the past, ...)
                prePrompt = "Your are a calendar assistant, Your job is to help user with their calendar. For reference today's date and time is " + self.get_today_date() + ",  " + self.get_current_time() + "."
                chat = self.getChat()  
                prompt = input("CalAgent: How can I help you with your calendar? ")
                prompt = prePrompt + "\n" + prompt
            else:
                chat = self.getChat()  
                prompt = input("CalAgent: Is there anything else?")

           
            response = chat.send_message(prompt)
            function_call = response.candidates[0].function_calls[0]
            print(function_call)
            api_response = self.process_function_call(function_call)

            response = chat.send_message(
                Part.from_function_response(
                    name="get_store_location",
                    response={
                        "content": api_response,
                    },
                ),
            )

            print(response.text)
    

    # TODO: update to switch statement 
    def process_function_call(self, function_call): 
        if function_call.name == "get_calendar_events":
            number_of_events = function_call.args["number_of_events"]
            print(f"Number of events: {number_of_events}")
            return self.get_calendar_events(number_of_events)
        elif function_call.name == "create_calendar_event":
            event_name = function_call.args["event_name"]
            start_time = function_call.args["start_time"]
            end_time = function_call.args["end_time"]
            location = function_call.args["location"]
            print(f"Event name: {event_name}, Start time: {start_time}, End time: {end_time}, Location: {location}")
            event_details = EventDetails(event_name, start_time, end_time, location)
            return self.create_calendar_event(event_details)
            # print("Event created successfully")
            # return event 
        else:
            raise ValueError(f"Unknown function call: {function_call.name}")


    def get_calendar_events(self, number_of_events):
        events = self.calendar.get_events(number_of_events)
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

        return events
    
    def create_calendar_event(self, event_details):
        event = self.calendar.create_event(event_details)
        return event



    def test(self):
        # self.model._tools.append()
        print("test")
        self.start_chat()


    