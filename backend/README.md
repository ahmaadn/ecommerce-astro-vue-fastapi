# BACKEND

## 🚀 Getting Started

Follow these steps to set up and run the FastAPI server.

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/ecommerce-astro-vue-fastapi.git
    cd ecommerce-astro-vue-fastapi/backend
    ```

2. **Install dependencies:**

    ```sh
    poetry install
    ```

3. **Set up environment variables:**

    Copy the example environment file and update it with your configuration.

    ```sh
    cp .env.example .env
    ```

    Edit the .env file to set your environment variables.

### Running the Server
Start the FastAPI server
```sh
cd app
fastapi dev
```

The server will start at `http://127.0.0.1:8000`.

### API Documentation
Once the server is running, you can access the API documentation at:

Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`
