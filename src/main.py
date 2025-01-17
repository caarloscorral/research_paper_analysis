import os
from create_env import load_config

# Load environment configuration
load_config()

from text_processing_flow import TextProcessingFlow


def main():
	"""
	Main function to run the document processing pipeline.
	"""
	# Initialize processing flow with environment variables load from config file
	text_processing_flow = TextProcessingFlow(
		file_path=os.getenv('FILE_PATH'),
		openai_api_key=os.getenv('OPENAI_API_KEY'),
		project_id=os.getenv('PROJECT_ID'),
		dataset_id=os.getenv('DATASET_ID'),
		table_id=os.getenv('TABLE_ID')
	)

	# Run processing flow
	text_processing_flow.run()


if __name__ == "__main__":
	main()
