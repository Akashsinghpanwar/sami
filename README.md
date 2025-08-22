# Maritime Virtual Assistant

This project is a virtual AI assistant for the maritime industry. It can answer queries related to laytime, weather, distances, and charter party clauses.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirement.txt
    ```

2.  **Configure API keys:**
    Create a `.env` file in the root of the project and add your API keys:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    WEATHER_API_KEY="your_weather_api_key_here"
    ```

## Running the application

The application provides two interfaces: a FastAPI backend and a Gradio UI.

### FastAPI Backend

To run the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
The API documentation will be available at `http://localhost:8000/docs`.

### Gradio UI

To run the Gradio UI:
```bash
python -m app.gradio_app
```
This will launch a web interface, typically on `http://127.0.0.1:7860`.
