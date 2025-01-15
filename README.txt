To run the server on localhost:
python main.py

Examples on how to use the API

Create a new entry:
curl -X POST http://127.0.0.1:5000/api/entries \
-H "Content-Type: application/json" \
-d '{"name": "Sample Entry", "description": "This is a test entry."}'

Ask for existing entries:
$ curl -X GET http://127.0.0.1:5000/api/entries
