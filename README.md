# RAG API

Implementation of a RAG API with an Elasticsearch database

- The API is made with Python and Flask framework

Implementation of an UI example for the API's upload feature

- The UI is made with React

## Requirements

Install [Elasticsearch](https://www.elastic.co/fr/downloads/elasticsearch) and set it as an environment variable

## Launching

To use and test the API, execute the file run.sh in the root directory of the project.

It will install Python dependencies and launch the API on http://127.0.0.1:49168

You can directly test the GET methods on your browser or utilize Postman for all request methods.

The shell script will also launch the UI on http://localhost:3000/, allowing you to easily test the API's upload functionality.

## Endpoints

This API exposes the following endpoints :

### Create a new indew

- URL : `/<index_name>`
- Method : `PUT`
- Description : Create a new index with its mapping
- URL Params : `index_name=[index_name]`
- Mapping example in the request body :
  ```json
  "properties": {
      "id": {"type": "keyword"},
      "title": {"type": "text"},
      "description": {"type": "text"},
      "extension": {"type": "keyword"},
      "creatorName": {"type": "keyword"},
      "source": {"type": "keyword"},
      "data_type": {"type": "keyword"},
      "content": {"type": "text"}
  }
  ```
- Example : http://127.0.0.1:49168/projectly

### Delete an index

- URL : `/<index_name>`
- Method : `DELETE`
- Description : Delete an index
- URL Params : `index_name=[index_name]`

### Display all documents

- URL : `/projectly/docs/all`
- Method : `GET`
- Description : Retrieve all documents
- Example : http://127.0.0.1:49168/projectly/docs/all

### RAG search

- URL : `/projectly/docs/rag_search/<req>`
- Method : `GET`
- Description : Retrieve documents with a specific request
- URL Params : `req=[req]`
- Example : http://127.0.0.1:49168/projectly/docs/rag_search/bill

### Upload document

- URL : `/projectly/docs/upload`
- Method : `POST`
- Description : Add a new document
- Example : try directly the upload feature on the UI on http://localhost:3000

### Update document

- URL : `/projectly/docs/update/<id>`
- Method : `PUT`
- Description : Update a document with a specific id and a content specified in the request body
- URL Params : `id=[id]`
- New content example in the request body :
  ```json
  {
    "title": "new title",
    "description": "new description",
    "content": "new content"
  }
  ```
- Example : http://127.0.0.1:49168/projectly/docs/update/idTesthhh007

### Delete document

- URL : `/projectly/docs/delete/<id>`
- Method : `DELETE`
- Description : Delete a document with a specific id
- URL Params : `id=[id]`
- Example : http://127.0.0.1:49168/projectly/docs/delete/idTesthhh007
