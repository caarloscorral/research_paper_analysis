import os
import json
import configparser

def load_config() -> None:
	"""
	Loads configuration settings from config.ini..
	Sets the required environment variables for the application.
	"""
	#---------------------------
	# Config Parser
	#---------------------------
	config = configparser.ConfigParser()
	conf = config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
	assert len(conf) != 0, 'Config file not found'

	#---------------------------
	# Credentials
	#---------------------------
	os.environ['OPENAI_API_KEY'] = config.get('CREDENTIALS', 'OPENAI_API_KEY')
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(config.get('CREDENTIALS', 'GOOGLE_APPLICATION_CREDENTIALS'))


	#---------------------------
	# Dataset
	#---------------------------
	os.environ['FILE_PATH'] = os.path.abspath(config.get('DATASET', 'FILE_PATH'))

	#---------------------------
	# Storage
	#---------------------------
	with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')) as f:
		os.environ['PROJECT_ID'] = json.load(f)['project_id']

	os.environ['DATASET_ID'] = config.get('STORAGE', 'DATASET_ID')
	os.environ['TABLE_ID'] = config.get('STORAGE', 'TABLE_ID')
