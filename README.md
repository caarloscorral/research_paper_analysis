# Research Paper Analysis

This project facilitates the extraction and analysis of structured data from scientific research paper PDFs using language models like OpenAI via LangChain, storing the extracted data in a BigQuery table.

## Project Structure

```
research_paper_analysis/
│
├── .venv/
├── src/
│   ├── __init__.py
│   ├── create_env.py
│   ├── data_storer.py
│   ├── document_ingestor.py
│   ├── information_extractor.py
│   ├── text_processing_flow.py
│   └── main.py
│
├── tests/
│
├── config.ini
└── requirements.txt
```

## Prerequisites

- Python 3.7+
- A Google Cloud account with service credentials for BigQuery.
- OpenAI API Key for accessing the language models.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/caarloscorral/research_paper_analysis
   ```

2. Navigate to the project directory:
   ```bash
   cd research_paper_analysis
   ```

3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Linux/macOS
   .venv\Scripts\activate     # For Windows
   ```

4. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### BigQuery Setup

1. **Google Cloud Setup:**
   - Create a Google Cloud account and set up a new project.
   - Enable the BigQuery API for your project through the Google Cloud Console.

2. **Service Account:**
   - Create a service account in your Google Cloud project.
   - Download the service account key as a JSON file. This will be used to authenticate your requests.

3. **BigQuery Dataset and Table:**
   - In the BigQuery console, create a new dataset.
   - Create a table within the dataset where the extracted data will be stored.

4. **Environment Variables:**
   - Update the `config.ini` file with the path to your service account JSON file, dataset ID, and table ID:

   ```ini
   [CREDENTIALS]
   GOOGLE_APPLICATION_CREDENTIALS = path/to/your/service-account-file.json

   [STORAGE]
   DATASET_ID = your_dataset_id
   TABLE_ID = your_table_id
   ```

### OpenAI Setup

1. **API Key:**
   - Create an account with OpenAI if you haven't already.
   - Obtain an OpenAI API key from the OpenAI dashboard.

2. **Environment Variable:**
   - Update the `config.ini` file with your OpenAI API key:

   ```ini
   [CREDENTIALS]
   OPENAI_API_KEY = your_openai_key
   ```

### Config File

Edit the `config.ini` file to define your environment variables:

```ini
[CREDENTIALS]
OPENAI_API_KEY = your_openai_key
GOOGLE_APPLICATION_CREDENTIALS = path/to/your/service-account-file.json

[DATASET]
FILE_PATH = path/to/your/pdf/file

[STORAGE]
DATASET_ID = your_dataset_id
TABLE_ID = your_table_id
```

## Usage

1. **Load environment configurations**: They are automatically loaded when running `main.py`.
  
2. **Run the processing flow**:
   ```bash
   python src/main.py
   ```

   This command will process PDFs, extract and analyze data using OpenAI, and store the data in BigQuery.

## Customization

All modules can be customized as needed:
- **`document_ingestor.py`**: Handles text extraction from PDFs.
- **`information_extractor.py`**: Performs structured information extraction using language models.
- **`data_storer.py`**: Integrates extracted data into BigQuery.

## Contributions

Contributions are welcome. Please open a Pull Request to suggest changes or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/caarloscorral/research_paper_analysis/blob/main/LICENSE) file for details.
