# Address Management API

This is a simple FastAPI-based API for managing addresses.

## Features

- List all addresses
- Filter addresses by street name
- Create a new address
- Update an existing address
- Delete an address by ID

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Python 3.8+ comes with SQLite ( if SQLite is not installed then install manually)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/md-rashid-2023/Address_FastApi.git
   cd Address_FastApi.git
   ```

2. Create a virtual environment and activate it:

    ``` python -m venv venv
        source venv/bin/activate  # For Linux/Mac

    ```

3. Install the required dependencies:

    ```
        pip install -r requirements.txt

    ```

4. Start the server:

    ``` cd api
        uvicorn application:app --reload
    ```