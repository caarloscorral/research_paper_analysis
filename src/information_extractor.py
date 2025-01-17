import datetime
from openai import OpenAIError
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

class InformationExtractor:
	"""
	Extracts structured data from text using OpenAI from LangChain.
	"""

	def __init__(self, raw_text: str, openai_api_key: str) -> None:
		"""
		Initializes the InformationExtractor with API credentials.
		:param: raw_text: str, text to be analyzed.
		:param openai_api_key: str, OpenAI API key.
		"""
		self.raw_text = raw_text

		# Initialize OpenAI model through LangChain
		self.llm = OpenAI(api_key=openai_api_key)

		# Variables to store extracted data
		self.title = ""
		self.authors = ""
		self.publication_date = ""
		self.abstract = ""
		self.key_findings = ""
		self.methodology = ""
		self.summary = ""
		self.keywords = []


	def set_raw_text(self, raw_text: str) -> str:
		"""
		Sets and returns class variable with raw text to extract information.

		:param: raw_text: str, text to be analyzed.
		:returns: str, text to be analyzed.
		"""
		self.raw_text = raw_text

		return self.raw_text


	def run_prompt(self, prompt_template: PromptTemplate) -> str:
		"""
		General method to run a given prompt through the LLM.

		:param prompt_template: PromptTemplate, prompt to be processed by the LLM.
		:returns: str, response from the LLM.
		"""
		# Setup the prompt
		llm_chain = LLMChain(llm=self.llm, prompt=prompt_template)
		
		# Obtain and return the response
		try:
			response = llm_chain.invoke(prompt_template.format(text=self.raw_text)).strip()
		except OpenAIError as e:
			response = f"An error occurred: {e}"
		except Exception as e:
			response = f"Unexpected error: {e}"
		return response


	def extract_title(self) -> str:
		"""
		Extracts title from the text.

		:returns: str, research paper's title.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Extract the title of the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def extract_authors(self) -> str:
		"""
		Extracts author(s) from the text.

		:returns: str, author(s) of the research paper.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Extract the author(s) of the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def extract_publication_date(self) -> str:
		"""
		Extracts publication date from the text.

		:returns: str, research paper's publication date.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Extract the publication date of the following scientific research paper, format as YYYY/MM/DD:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def extract_abstract(self) -> str:
		"""
		Extracts abstract from the text.

		:returns: str, research paper's abstract.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Extract the abstract of the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def extract_key_findings(self) -> str:
		"""
		Extracts key research findings from the text.

		:returns: str, key findings from the research paper.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Identify key findings in the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def extract_methodology(self) -> str:
		"""
		Extracts methodology from the text.

		:returns: str, methodology from the research paper.
		"""
		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Identify the methodology used in the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def generate_summary(self) -> str:
		"""
		Generates a text summary.

		:returns: str, research paper's summary.
		"""

		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Generate a brief summary of the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def generate_keywords(self) -> str:
		"""
		Generates keywords of the text.

		:returns: str, research paper's keywords.
		"""

		prompt_template = PromptTemplate(
			input_variables=['text'],
			template="Generate keywords for the following scientific research paper:\n{text}"
		)

		return self.run_prompt(prompt_template)


	def get_extracted_data(self) -> dict:
		"""
		Retrieves all extracted data as a dictionary.

		:returns: dict, dictionary containing all extracted information.
		"""
		return {
			'utc_timestamp': datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d %H:%M:%S"),
			'title': self.extract_title(),
			'authors': self.extract_authors(),
			'publication_date': self.extract_publication_date(),
			'abstract': self.extract_abstract(),
			'findings': self.extract_key_findings(),
			'methodology': self.extract_methodology(),
			'summary': self.generate_summary(),
			'keywords': self.generate_keywords()
		}
	