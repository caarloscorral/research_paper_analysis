import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the root of the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.document_ingestor import DocumentIngestor


class TestDocumentIngestor(unittest.TestCase):
	"""
	Test cases for the DocumentIngestor class.
	"""

	@patch('fitz.open', autospec=True)
	def test_process_text_valid_pdf_with_lists(self, mock_fitz_open):
		"""
		Test processing text from a valid PDF file containing numbered and bullet lists.
		"""
		# Define PDF behavior with a mock
		mock_pdf = MagicMock()
		mock_fitz_open.return_value.__enter__.return_value = mock_pdf
		mock_pdf.page_count = 1

		# Simulate PDF page content with lists
		mock_page = MagicMock()
		mock_page.get_text.return_value = (
			"1. First item\n"
			"Details of first item continue.\n"
			"2. Second item\n"
			"● Bullet item A\n"
			"● Bullet item B\n"
			"3. Third item\n"
		)
		mock_pdf.load_page.return_value = mock_page

		# Initialize ingestor and process the mock PDF
		ingestor = DocumentIngestor('dummy.pdf')
		processed_text = ingestor.process_text()

		# Define expected text processing result where lists are properly combined
		expected_text = (
			"1. First item Details of first item continue.\n"
			"2. Second item\n"
			"● Bullet item A\n"
			"● Bullet item B\n"
			"3. Third item"
		)

		# Assert processed text matches expected result
		self.assertEqual(processed_text, expected_text)


	def test_initialize_invalid_file(self):
		"""
		Test initializing with a non-PDF file should raise a ValueError.
		"""
		with self.assertRaises(ValueError):
			DocumentIngestor('dummy.txt')


	@patch('fitz.open', side_effect=RuntimeError("Corrupted PDF"))
	def test_process_text_corrupted_pdf(self, mock_fitz_open):
		"""
		Test processing a corrupted PDF raises an appropriate exception.
		"""
		ingestor = DocumentIngestor('dummy.pdf')
		with self.assertRaises(Exception) as context:
			ingestor.process_text()

		self.assertIn("Error while reading PDF file", str(context.exception))


if __name__ == '__main__':
	unittest.main()
