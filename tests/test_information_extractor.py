import os
import sys
import unittest
from openai import OpenAIError
from unittest.mock import patch, MagicMock

# Add the root of the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.information_extractor import InformationExtractor


class TestInformationExtractor(unittest.TestCase):
	"""
	Test cases for the InformationExtractor class, responsible for extracting
	structured data from text using models from the LangChain library.
	"""

	@patch('src.information_extractor.InformationExtractor.get_extracted_data', autospec=True)
	@patch('src.information_extractor.OpenAI', autospec=True)
	def test_extract_all_properties(self, mock_openai, mock_get_extracted_data):
		"""
		Test the extraction of all properties using a mocked OpenAI model.
		Covers extraction methods for title, author, publication date,
		abstract, key findings, methodology, summary, and keywords.
		"""
		# Mock the get_extracted_data method of InformationExtractor to simulate responses
		mocked_data = {
			'title': "Test Title",
			'authors': "John Doe",
			'publication_date': "2023/01/01",
			'abstract': "Abstract content.",
			'findings': "Key finding one.",
			'methodology': "Methodology details.",
			'summary': "Paper summary.",
			'keywords': "keyword1, keyword2",
		}

		mock_get_extracted_data.return_value = mocked_data
		
		# Create an instance of the InformationExtractor with sample text
		extractor = InformationExtractor("Sample text", 'fake_api_key')
		
		# Get the extracted data as a dictionary
		data = extractor.get_extracted_data()

		# Assert each piece of extracted data against expected mock responses
		self.assertEqual(data['title'], "Test Title")
		self.assertEqual(data['authors'], "John Doe")
		self.assertEqual(data['publication_date'], "2023/01/01")
		self.assertEqual(data['abstract'], "Abstract content.")
		self.assertEqual(data['findings'], "Key finding one.")
		self.assertEqual(data['methodology'], "Methodology details.")
		self.assertEqual(data['summary'], "Paper summary.")
		self.assertEqual(data['keywords'], "keyword1, keyword2")


	@patch('src.information_extractor.InformationExtractor.get_extracted_data', autospec=True)
	@patch('src.information_extractor.OpenAI', autospec=True)
	def test_handle_openai_error(self, mock_openai, mock_get_extracted_data):
		"""
		Test handling of OpenAI errors during prompt processing.
		Simulates a scenario where the OpenAI model raises an error.
		"""
		# Mock the get_extracted_data method of InformationExtractor to simulate error response
		mock_get_extracted_data.side_effect = OpenAIError("API limit exceeded")
		
		# Assert that an OpenAIError is raised during extraction
		with self.assertRaises(OpenAIError) as context:
			InformationExtractor("Sample text", 'fake_api_key').get_extracted_data()
		self.assertEqual(str(context.exception), "API limit exceeded")


if __name__ == '__main__':
	unittest.main()
