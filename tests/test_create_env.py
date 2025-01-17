import os
import sys
import unittest
from unittest.mock import patch, mock_open

# Add the root of the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.create_env import load_config


class TestCreateEnv(unittest.TestCase):
	"""
	Test cases for the load_config function in create_env.py.
	"""

	def setUp(self):
		"""
		Set up mock configuration content.
		"""
		self.mock_config_content = """
		[CREDENTIALS]
		OPENAI_API_KEY = test_openai_key
		GOOGLE_APPLICATION_CREDENTIALS = /mock/path/to/service-account-file.json

		[DATASET]
		FILE_PATH = /mock/path/to/pdf/file

		[STORAGE]
		DATASET_ID = test_dataset_id
		TABLE_ID = test_table_id
		"""

	@patch('builtins.open', new_callable=mock_open, read_data='{"project_id": "test_project_id"}')
	@patch('os.path.join', return_value='config.ini')
	@patch('configparser.ConfigParser.read', return_value=['config.ini'])
	@patch('configparser.ConfigParser.get')
	@patch.dict(os.environ, {}, clear=True)
	def test_load_config(self, mock_get, mock_read, mock_join, mock_file):
		"""
		Test loading of configuration and setting environment variables from fictional config.ini.
		"""
		
		# Simulate reading values from the config file
		mock_get.side_effect = lambda section, option: {
			('CREDENTIALS', 'OPENAI_API_KEY'): 'test_openai_key',
			('CREDENTIALS', 'GOOGLE_APPLICATION_CREDENTIALS'): '/mock/path/to/service-account-file.json',
			('DATASET', 'FILE_PATH'): '/mock/path/to/pdf/file',
			('STORAGE', 'DATASET_ID'): 'test_dataset_id',
			('STORAGE', 'TABLE_ID'): 'test_table_id'
		}[(section, option)]
		
		# Run the configuration loader
		load_config()

		# Use os.path.abspath for full consistency and direct comparison
		expected_gcp_path = os.path.abspath(os.path.normpath('/mock/path/to/service-account-file.json'))

		# Use os.getenv to verify the environment variables
		self.assertEqual(os.getenv('OPENAI_API_KEY'), 'test_openai_key')
		self.assertEqual(os.path.abspath(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')), expected_gcp_path)
		self.assertEqual(os.path.abspath(os.getenv('FILE_PATH')), os.path.abspath(os.path.normpath('/mock/path/to/pdf/file')))
		self.assertEqual(os.getenv('DATASET_ID'), 'test_dataset_id')
		self.assertEqual(os.getenv('TABLE_ID'), 'test_table_id')
		self.assertEqual(os.getenv('PROJECT_ID'), 'test_project_id')


	@patch('configparser.ConfigParser.read', return_value=[])
	def test_load_config_not_found(self, mock_read):
		"""
		Test handling of a missing configuration file.
		"""
		with self.assertRaises(AssertionError):
			load_config()

if __name__ == '__main__':
	unittest.main()
