# RickAndMorty API Task

### Installing

1 Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the FastAPI application:
    ```sh
    uvicorn main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

## Usage

Once the FastAPI application is running, you can visit the root URL to fetch, process, and view the filtered data from the RickAndMorty API.

To view the filtered data in the browser, visit [http://127.0.0.1:8000](http://127.0.0.1:8000).


The application will generate three JSON files in the project directory each containing the processed data from the RickAndMorty API.

- characters.json
- locations.json
- episodes.json

location of files app/utils/third_party/morti_api/json_output
