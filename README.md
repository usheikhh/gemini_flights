# Gemini Flight Manager

## Overview

Gemini Flight Manager is a comprehensive backend system built using FastAPI, designed for managing and simulating flight-related operations. This system provides a robust platform for handling various aspects of flight management, including flight generation, search, and booking functionalities.

The project leverages FastAPI's efficient and easy-to-use framework to create a high-performance, scalable solution ideal for flight data management. It comes equipped with an SQLite database (`flights.db`) pre-populated with initial data, allowing for quick deployment and testing.

Key features of Gemini Flight Manager include:
- Advanced search capabilities to query flights based on criteria like origin, destination, and dates.
- Booking system that handles seat availability across different classes and calculates costs accordingly.

Designed with extensibility and scalability in mind, Gemini Flight Manager is well-suited for both educational purposes and as a foundation for more complex flight management applications.

**For the purposes of Gemini Function Calling, you will only need `search_flights` and `book_flight` functions.

## Mission Scenario  
Design an interactive flights management chat interface that revolutionizes the flight booking experience through a conversational platform. This advanced chat system, powered by Google's latest large language model, Gemini, enables users to search and book flights using natural language, providing a seamless and intuitive user experience. Gemini's unique function calling capability allows for the creation of custom tools that interact with a local backend server/database, simulating real-time flight management and booking processes.

## Mission Tasks 
- ✨ Setting up Google Gemini
- Clone Premade FastAPI Server
- ☁️ Google Cloud Developer Initialization
- 📞 Function Calling with Tools
- 📊 Streamlit Integration
- ✈️ Build the Book_Flight Tool

## Requirements:

- Python version 3.9x or above [Python](https://www.python.org/downloads/)
- Streamlit [Streamlit Documentation](https://docs.streamlit.io/)
- Gcloud account
- Vertexai [Vertexai Documentation](https://cloud.google.com/vertex-ai)


### Step-by-Step Installation Guide

1. **Clone the Repository**
   
   Start by cloning the repository to your local machine. Use the following command:
   

## Set Up a Virtual Environment (Optional but recommended)

It's a good practice to create a virtual environment for your Python projects. This keeps your project dependencies isolated. If you have `virtualenv` installed, create a new environment with:

```bash
virtualenv venv
source venv/bin/activate
```

## Install Dependencies
Inside the virtual environment, install all necessary dependencies by running:
```bash
pip install -r requirements.txt
```

## Starting the FastAPI Server

After the installation, you can start the FastAPI server using Uvicorn. Navigate to the project directory and run:

```bash
uvicorn main:app
```

## Accessing the API
With the server running, you can access the API at `http://127.0.0.1:8000.`

For interactive API documentation, visit `http://127.0.0.1:8000/docs`, where you can test the API endpoints directly from your browser.



