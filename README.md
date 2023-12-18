# RAG API

Implementation of an API for RAG database

- The API is made with Python and Flask framework

Implementation of an UI example for the API's upload feature

- The UI is made with React

## Utilisation

To use and test the API, execute the file run.sh in the root directory of the project.

It will install Python dependencies and launch the API on http://127.0.0.1:5000/

You can directly test the GET methods on your browser or utilize Postman for all request methods.

In particular, for RAG searches, you can make a GET request like so:
http://127.0.0.1:5000/projectly/docs/rag_search/bill

The shell script will also launch the UI on http://localhost:3000/, allowing you to easily test the API's upload functionality.
