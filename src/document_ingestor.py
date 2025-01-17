import re
import fitz

class DocumentIngestor:
	"""
	Class responsible for extracting text from PDF documents.
	"""
	def __init__(self, file_path: str) -> None:
		"""
		Initialize with the path to a PDF file.

		:param file_path: str, path to the PDF file to be processed
		"""
		if file_path.endswith('.pdf'):
			self.file_path = file_path
		else:
			raise ValueError("Provided file is not a PDF.")


	def __process_lists(self, text: str) -> str:
		"""
		Processes text to ensure list items are combined with their accompanying content
		on the same line. This function detects lines starting with a numbered pattern or a bullet point and appends
		their content if the subsequent line is meant to continue the item.

		:param: text: str, raw text containing numbered lists.
		:returns: str, formatted text with numbered list items and content on a single line.
		"""
		lines = text.split('\n')
		list_item_pattern = re.compile(r'^(?:\d+[\s)*\.\-•●]*|[*•●-]+|[○]+)')

		combined_lines = []
		i = 0
		while i < len(lines):
			line = lines[i].strip()
			if list_item_pattern.match(line):
				# If next line continues the content of a list item, combine them
				while i + 1 < len(lines) and not list_item_pattern.match(lines[i + 1].strip()):
					line += " " + lines[i + 1].strip()
					i += 1
			combined_lines.append(line)
			i += 1
		
		# Ensure lines are separated properly
		return "\n".join(combined_lines).strip()


	def process_text(self) -> str:
		"""
		Processes text from each page of the PDF.

		:return: str, string containing the processed text.
		"""
		try:
			with fitz.open(self.file_path) as pdf:
				text = ""

				# Extract text from a page and join into one single string
				for page_number in range(pdf.page_count):
					page = pdf.load_page(page_number)
					text += page.get_text('text')
				
			text = self.__process_lists(text)
			
			return text

		except Exception as e:
			raise Exception(f"Error while reading PDF file: {e}")
