import logging
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.data_storer import DataStorer
from src.document_ingestor import DocumentIngestor
from src.information_extractor import InformationExtractor


class State(TypedDict):
	"""
	State is used as a container to manage the data being processed and passed between
	different stages of the LangGraph pipeline. This structured type helps to maintain 
	the state of extracted content and any additional information generated at each 
	processing stage.
	"""
	pdf_content: str
	extracted_data: dict


class TextProcessingFlow:
	"""
	Manages the workflow for extracting text from a research paper in a PDF file, processing the text
	to extract structured information, and storing this data in a BigQuery table.
	"""

	def __init__(self, file_path: str, openai_api_key: str, project_id: str, dataset_id: str, table_id: str) -> None:
		"""
		Initializes with necessary components for document ingestion, information extraction,
		and data storage in a BigQuery table.

		:param file_path: Path to the PDF file.
		:param openai_api_key: API key for OpenAI.
		:param project_id: Google Cloud project ID.
		:param dataset_id: BigQuery dataset ID.
		:param table_id: BigQuery table ID.
		"""
		self.file_path = file_path
		self.openai_api_key = openai_api_key
		self.project_id = project_id
		self.dataset_id = dataset_id
		self.table_id = table_id

		# Set up logging
		logging.basicConfig(level=logging.INFO)

		# Create and compile the workflow using LangGraph
		self.workflow = self.create_workflow()


	def ingest_document(self, state) -> dict:
		"""
		Node function to ingest a document and extract text from it.
		"""
		# Initialize Document Ingestor
		document_ingestor = DocumentIngestor(self.file_path)

		# Extract text from PDF and save it into state
		try:
			state['pdf_content'] = document_ingestor.process_text()
			logging.info("Text processed successfully from PDF file.")
		
		except Exception as e:
			logging.error(f"Failed to process text from PDF file: {e}")

		return {'pdf_content': state['pdf_content']}


	def extract_information(self, state) -> dict:
		"""
		Node function to extract information from the PDF content.
		"""
		# Initialize Information Extractor
		information_extractor = InformationExtractor(raw_text=state['pdf_content'], openai_api_key=self.openai_api_key)

		# Extract needed info from text and save it into state
		try:
			state['extracted_data'] = information_extractor.get_extracted_data()
			logging.info("Data extracted successfully from text.")
	
		except Exception as e:
			logging.error(f"Failed to extract data from text: {e}")

		return {'extracted_data': state['extracted_data']}


	def store_information(self, state) -> dict:
		"""
		Node function to store extracted information in BigQuery.
		"""
		# Initialize Data Storer
		data_storer = DataStorer(project_id=self.project_id, dataset_id=self.dataset_id, table_id=self.table_id)
		# Store extracted data in BigQuery
		try:
			data_storer.store_data(state['extracted_data'])
			logging.info("Data stored successfully in BigQuery.")
	
		except Exception as e:
			logging.error(f"Failed to store data in BigQuery: {e}")

		return {}


	def create_graph_nodes(self, workflow: StateGraph) -> StateGraph:
		"""
		Adds nodes to the workflow of the StateGraph. Each node represents a distinct
		processing step in the computational pipeline. Nodes are associated with their
		respective processing functions.

		This function defines three primary nodes:
		- ingest_document: Responsible for ingesting and extracting text from a PDF.
		- extract_information: Responsible for extracting structured information from raw text.
		- store_information: Responsible for storing the extracted information into BigQuery.

		:param workflow: StateGraph, workflow execution graph to be configured with nodes.
		:returns: StateGraph, workflow with added nodes.
		"""
		# Add a node for the document ingestion process, associating it with its method
		workflow.add_node('ingest_document', self.ingest_document)

		# Add a node for the information extraction process, associating it with its method
		workflow.add_node('extract_information', self.extract_information)

		# Add a node for the data storage process, associating it with its method
		workflow.add_node('store_information', self.store_information)

		return workflow


	def create_graph_edges(self, workflow: StateGraph) -> StateGraph:
		"""
		Defines the directed edges between nodes within the workflow graph of StateGraph.
		These edges establish a processing sequence, dictating the order in which nodes
		should be executed.

		The current sequence is structured as follows:
		1. Start with the 'ingest_document' node.
		2. Proceed to the 'extract_information' node.
		3. Move to the 'store_information' node.
		4. Conclude the process at the END node.

		:param workflow: StateGraph, workflow execution graph to configure with edges.
		:returns: StateGraph, workflow with added edges.
		"""
		# Connect the START node to the 'ingest_document' node
		workflow.add_edge(START, 'ingest_document')

		# Connect 'ingest_document' to the next node, 'extract_information'
		workflow.add_edge('ingest_document', 'extract_information')

		# Connect 'extract_information' to 'store_information', continuing the process flow
		workflow.add_edge('extract_information', 'store_information')

		# Connect 'store_information' to the END node, marking the conclusion of the process
		workflow.add_edge('store_information', END)

		return workflow


	def create_workflow(self):
		"""
		Creates and compiles the workflow using LangGraph, which orchestrates it.
		"""
		# Set up memory
		memory = MemorySaver()
		
		# Initialize workflow
		workflow = StateGraph(State)
		
		# Add nodes
		workflow = self.create_graph_nodes(workflow)
		
		# Define edges between nodes
		workflow = self.create_graph_edges(workflow)

		# Compile workflow into a LangChain Runnable, meaning it can be used as we would any other runnable
		return workflow.compile(checkpointer=memory)


	def run(self):
		"""
		Executes the processing workflow.
		"""
		# Set up configuration
		self.config = {'configurable': {'thread_id': 'my_thread'}}

		# Set up initial state
		initial_state = State(pdf_content="", extracted_data={})
		
		# Run the workflow
		self.workflow.invoke(input=initial_state, config=self.config)
