import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the root of the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_storer import DataStorer


class TestDataStorer(unittest.TestCase):
	"""
	Test cases for the DataStorer class.
	"""

	@patch('src.data_storer.Client', autospec=True)
	def test_store_data(self, mock_bq_client):
		"""
		Test storing data in BigQuery using a mocked client.
		"""
		# Create a mock instance for BigQuery client
		mock_client = mock_bq_client.return_value

		# Set up the DataStorer with mock parameters
		storer = DataStorer('project_id', 'dataset_id', 'table_id')

		# Create example extracted data
		extracted_data = {
			'utc_timestamp': '2025/01/01 00:00:00',
			'title': 'Title',
			'authors': 'Authors',
			'publication_date': '2023/01/01',
			'abstract': 'Abstract',
			'findings': 'Findings',
			'methodology': 'Methodology',
			'summary': 'Summary',
			'keywords': ['keyword1', 'keyword2']
		}
		
		# Store data using the DataStorer instance
		storer.store_data(extracted_data)

		# Assert the insert_rows_json function was called once
		mock_client.insert_rows_json.assert_called_once()


	@patch('src.data_storer.Client', autospec=True)
	def test_store_data_with_error(self, mock_bq_client):
		"""
		Test handling errors when storing data in BigQuery.
		"""
		# Create a mock instance for BigQuery client
		mock_client = mock_bq_client.return_value

		# Simulate an error when inserting rows
		mock_client.insert_rows_json.side_effect = Exception("BigQuery insert error")

		# Set up the DataStorer with mock parameters
		storer = DataStorer('project_id', 'dataset_id', 'table_id')

		# Create example extracted data
		extracted_data = {
			'utc_timestamp': '2025/01/01 00:00:00',
			'title': 'Title',
			'authors': 'Authors',
			'publication_date': '2023/01/01',
			'abstract': 'Abstract',
			'findings': 'Findings',
			'methodology': 'Methodology',
			'summary': 'Summary',
			'keywords': ['keyword1', 'keyword2']
		}
		
		# Attempt to store data and ensure an exception is raised
		with self.assertRaises(Exception):
			storer.store_data(extracted_data)


if __name__ == '__main__':
	unittest.main()
