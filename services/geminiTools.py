import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Tool, Part, Content, ChatSession
from flight_manager import search_flights, book_flight

project = "gemini-explorer-424819"
vertexai.init(project = project)

# Declaring the Tool 
get_search_flights = generative_models.FunctionDeclaration( #this is Google's object; going to create and declare the function the large language model can have access to 
    #defining this function that the model does not know about yet, and you are telling the model what exactly does this function do 
    name="get_search_flights",
    description="Tool for searching a flight with origin, destination, and departure date", #make sure the description is detailed; This is how the model knows what to use it for 
    #parameters: creating a json obj in which the model needs to respond back 
    parameters={ 
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "The airport of departure for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "destination": {
                "type": "string",
                "description": "The airport of destination for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "departure_date": {
                "type": "string",
                "format": "date",
                "description": "The date of departure for the flight in YYYY-MM-DD format" #format that ISO accepts
            },
        },
        "required": [#required to have origin, destination, and departure date in order to call the object 
            "origin",
            "destination",
            "departure_date",
        ]
    },
)

#Declaring the book_flight tool
post_book_flight = generative_models.FunctionDeclaration(
    name = "post_book_flight",
    description= "tool for booking a flight with the flight ID, seat type, and number of seats",
    parameters={
        "type" : "object",
        "properties": {
            "flight_id" : {
                "type" : "integer",
                "description" : "The ID of the flight"
            },
            "seat_type" : {
                "type" : "string",
                "description" : "The type of seat to be booked. This can be either 'economy', 'business', or 'first_class' "
            },

            "num_seats": {
                "type" : "integer",
                "description" : "Optional parameter with a default value of 1. This is the number of seats to be booked"
            }   
        }
        
    }
)



#In essence, with the parameters you are telling the model you have a function - model does not need to what the function does - just need to tell the model, this is how the model works and this is how to invoke the function 

#Binding the function to a search tool  
# Instantiate tool and model with tools
search_tool = generative_models.Tool( #instantiating the tool 
    function_declarations=[get_search_flights, post_book_flight],
)


config = generative_models.GenerationConfig(temperature=0.4)
# Load model with config
model = GenerativeModel( #passing in model, list of tools, and passing the config
    "gemini-pro",
    tools = [search_tool], #passing the tool into the GenerativeModel
    generation_config = config
)

#When adding a new tool to the model, you need to go through this process again. You have to define what the tool is through a function declaration as above. Then you are going to instantiate and equip the model with those tools. Lastly, you need to bind it to the actual model itself

#the way the model works is if there is a tool that gets called, it needs to stop in terms of its responses to get a response back from the API
#helper function to unpack responses 
def handle_response(response):

    #Check for function call with intermediate step, always return response
    if response.candidates[0].content.parts[0].function_call.args: #checking are there any arguments called in order for the function tools to actually exist
        # Function call exists, upack and load into a function
        response_args = response.candidates[0].content.parts[0].function_call.args #unpacking google's response

        function_params = {} #packaging it into a dictionary 
        for key in response_args:
            value = response_args[key]
            function_params[key] = value
        

        results = search_flights(**function_params) #unpackaging the dictionary back of all its arguments into the search flights function, and it is sending a GET request to our fastAPI endpoint to receive back the info 

        if results: #if there are any results (get request),  we need to send out FastAPI results back to google gemini
            intermediate_response = chat.send_message(
                Part.from_function_response(
                    name = "get_search_flights",
                    response = results
                )
            )
            return intermediate_response.candidates[0].content.parts[0].text #then return the actual intermediate response (the second turn in the conversation)
        else:
            return "Search Failed"
    else:
        #if its not calling back any function, we are just calling back the regular text itself 
        return response.candidates[0].content.parts[0].text
        



#helper function to display and send streamlit messages. Will serve as a way to display and store the messages that will be incoming 
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query) #going to store the response and sending the query over to the chat session
    output = handle_response(response)
    # output = response.candidates[0].content.parts[0].text #from there we get the actual text output 


    with st.chat_message("model"):
        st.markdown(output) #model.markdown; telling the stream to create a chat message from this output and applying it to the chat session

#displaying and sending stream messages:
    st.session_state.messages.append( #going to append in the session memory that the user had made a query 
        {
            "role": "user",
            "content": query
        }
    )

    st.session_state.messages.append(#from there we are going to append the models output
        {
            "role": "model",
            "content": output
        }
    )


st.title("Gemini Flights")

chat = model.start_chat()

#initialize chat history 
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display and load to chat history 
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message['role'],
        parts = [Part.from_text(message['content'])]
    )
    
    if index != 0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    chat.history.append(content)


#For initial message startup 
if len(st.session_state.messages) == 0:
    #initial message 
    initial_prompt = "Introduce yourself as a flights management assistant, Rex, powered by Google Gemini and designed to search/book flights. You use emojis to be interactive. For reference, the year for dates is 2024"

    llm_function(chat,initial_prompt)

#To capture user input 
query = st.chat_input("Gemini Flights")

if query: 
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)