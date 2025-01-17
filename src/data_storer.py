from typing import List
from google.cloud.bigquery import Client, SchemaField, Table

class DataStorer:
	"""
	Loads extracted data into a BigQuery table.
	"""

	def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
		"""
		Initializes the DataStorage with BigQuery configurations.

		:param: project_id: str, Google Cloud project ID.
		:param: dataset_id: str, BigQuery dataset ID.
		:param: table_id: str, BigQuery table ID.
		"""
		self.project_id = project_id
		self.dataset_id = dataset_id
		self.table_id = table_id
		self.client = Client()


	def create_schema(self) -> List:
		"""
		Creates a schema for the BigQuery table.

		:returns: list of SchemaField objects defining the table schema.
		"""
		schema = [
			SchemaField('utc_timestamp', 'TIMESTAMP'),
			SchemaField('title', 'STRING'),
			SchemaField('authors', 'STRING'),
			SchemaField('publication_date', 'DATETIME'),
			SchemaField('abstract', 'STRING'),
			SchemaField('findings', 'STRING'),
			SchemaField('methodology', 'STRING'),
			SchemaField('summary', 'STRING'),
			SchemaField('keywords', 'STRING', mode='REPEATED')
		]

		return schema


	def store_data(self, extracted_data: dict) -> None:
		"""
		Stores extracted data into the BigQuery table.

		:param: extracted_data: dict, extracted data to be stored into the table.
		"""
		table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
		table = Table(table_ref, schema=self.create_schema())
		self.client.create_table(table, exists_ok=True)

		rows_to_insert = [
			{
				u'utc_timestamp': extracted_data['utc_timestamp'],
				u'title': extracted_data['title'],
				u'authors': extracted_data['authors'],
				u'publication_date': extracted_data['publication_date'],
				u'abstract': extracted_data['abstract'],
				u'findings': extracted_data['findings'],
				u'methodology': extracted_data['methodology'],
				u'summary': extracted_data['summary'],
				u'keywords': extracted_data['keywords']
			}
		]

		# Insert rows into the BigQuery table and handle potential errors
		errors = self.client.insert_rows_json(table, rows_to_insert)
		if errors:
			print("Encountered errors while inserting rows: {}".format(errors))
