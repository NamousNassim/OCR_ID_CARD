# Extraction Model Microservice

This microservice extracts text from images using a pre-trained model.

## Setup

1. Clone the repository.
2. Navigate to the project directory.

## Running Locally

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

## Running with Docker

1. Build the Docker image:
    ```sh
    docker build -t extraction_model .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8000:8000 extraction_model
    ```

## API Endpoints

- `POST /extract-text/`: Upload an image to extract text from it.