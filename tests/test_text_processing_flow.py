import os
import sys
import unittest
from langgraph.graph import START, END
from unittest.mock import MagicMock, patch

# Add the root of the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.text_processing_flow import TextProcessingFlow

class TestTextProcessingFlow(unittest.TestCase):

	def setUp(self):
		"""
		Sets up the test case with necessary mocks and initialize
		the TextProcessingFlow instance.
		"""
		self.file_path = "dummy/path/to/file.pdf"
		self.openai_api_key = 'dummy_api_key'
		self.project_id = 'dummy_project_id'
		self.dataset_id = 'dummy_dataset_id'
		self.table_id = 'dummy_table_id'
		
		self.flow = TextProcessingFlow(
			file_path=self.file_path,
			openai_api_key=self.openai_api_key,
			project_id=self.project_id,
			dataset_id=self.dataset_id,
			table_id=self.table_id
		)


	@patch('src.text_processing_flow.DocumentIngestor.process_text', return_value="Mocked PDF content")
	@patch('src.text_processing_flow.InformationExtractor.get_extracted_data', return_value={'title': 'Mocked Title'})
	@patch('src.text_processing_flow.DataStorer.store_data', return_value=None)
	def test_ingest_document_success(self, mock_process, mock_extract, mock_store):
		"""
		Tests that the ingest_document function processes the document correctly.
		"""
		state = {'pdf_content': ""}
		result = self.flow.ingest_document(state)
		self.assertEqual(result['pdf_content'], "Mocked PDF content")
		self.assertEqual(state['pdf_content'], "Mocked PDF content")


	@patch('src.text_processing_flow.InformationExtractor.get_extracted_data', return_value={'title': 'Mocked Title'})
	@patch('src.information_extractor.OpenAI', autospec=True)
	def test_extract_information_success(self, mock_openai, mock_extract):
		"""
		Tests that the extract_information method extracts data successfully.
		"""
		state = {'pdf_content': "Mocked PDF content", 'extracted_data': {}}
		result = self.flow.extract_information(state)
		self.assertEqual(result['extracted_data']['title'], "Mocked Title")
		self.assertEqual(state['extracted_data']['title'], "Mocked Title")


	@patch('src.text_processing_flow.DataStorer.store_data', return_value=None)
	@patch('src.data_storer.Client', autospec=True)
	def test_store_information_success(self, mock_client, mock_store):
		"""
		Tests that store_information succeeds in storing data.
		"""
		state = {'extracted_data': {'title': 'Mocked Title'}}
		self.flow.store_information(state)
		mock_store.assert_called_once()
		mock_client.assert_called_once()


	@patch('src.text_processing_flow.DataStorer.store_data', side_effect=Exception("Mocked storage error"))
	@patch('src.data_storer.Client', autospec=True)
	def test_store_information_failure(self, mock_client, mock_store):
		"""
		Tests that store_information handles errors during storage.
		"""
		state = {'extracted_data': {'title': 'Mocked Title'}}
		self.flow.store_information(state)
		mock_store.assert_called_once()
		mock_client.assert_called_once()


	def test_create_graph_nodes(self):
		"""
		Tests that nodes are correctly added to the graph.
		"""
		original_workflow = MagicMock()
		modified_workflow = self.flow.create_graph_nodes(original_workflow)
		modified_workflow.add_node.assert_any_call('ingest_document', self.flow.ingest_document)
		modified_workflow.add_node.assert_any_call('extract_information', self.flow.extract_information)
		modified_workflow.add_node.assert_any_call('store_information', self.flow.store_information)


	def test_create_graph_edges(self):
		"""
		Tests that edges are correctly connected in the graph.
		"""
		original_workflow = MagicMock()
		modified_workflow = self.flow.create_graph_edges(original_workflow)
		modified_workflow.add_edge.assert_any_call(START, 'ingest_document')
		modified_workflow.add_edge.assert_any_call('ingest_document', 'extract_information')
		modified_workflow.add_edge.assert_any_call('extract_information', 'store_information')
		modified_workflow.add_edge.assert_any_call('store_information', END)


	@patch('src.text_processing_flow.DocumentIngestor.process_text', return_value="Mocked PDF content")
	@patch('src.text_processing_flow.InformationExtractor.get_extracted_data', return_value={'title': 'Mocked Title'})
	@patch('src.text_processing_flow.DataStorer.store_data', return_value=None)
	@patch('src.data_storer.Client', autospec=True)
	def test_full_workflow_execution(self, mock_client, mock_process, mock_extract, mock_store):
		"""
		Tests the full workflow execution.
		"""
		initial_state = {'pdf_content': "", 'extracted_data': {}}
		config = {'configurable': {'thread_id': 'my_thread'}}
		self.flow.workflow.invoke(input=initial_state, config=config)
  
		self.assertEqual(self.flow.workflow.get_state(config).values['pdf_content'], "Mocked PDF content")
		self.assertIn('title', self.flow.workflow.get_state(config).values['extracted_data'])
		self.assertEqual(self.flow.workflow.get_state(config).values['extracted_data']['title'], "Mocked Title")
		mock_store.assert_called_once()
		mock_client.assert_called_once()


if __name__ == '__main__':
	unittest.main()
