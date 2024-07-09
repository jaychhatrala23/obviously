
# obviously

This application is a Django REST Framework (DRF)-based server that provides a RESTful API for managing a Persons model. The API offers a range of endpoints enabling CRUD (Create, Read, Update, Delete) operations and search functionalities.
## Features

- Basic Authentication using username and password for all endpoints

- CRUD Operations: Admin users have full access to create, read, update, and delete operations on the Persons model. 

- Search Functionality: Both admin and guest users can perform search operations on the Persons data. This includes Basic Search, Vector based Similarity Search and Elasticsearch with Fuzzy 

- Custom Exception Handler

- Optimized Docker Image to run the application that uses in-memory SQLite db and Elasticsearch

## API Endpoints

ADMIN only: 

- POST /persons/: Create a new person record.
- GET /persons/: Retrieve a list of all person records.
- GET /persons/{id}/: Retrieve a specific person by their ID.
- PUT /persons/{id}/: Update a person record.
- DELETE /persons/{id}/: Delete a person record.

ADMIN & GUEST : 

- GET /persons/search/?first_name=John&last_name=Doe&age=34 : Retrieve persons that match by first_name, last_name or age or all of them

- GET /persons/vector_search/?q=admin : Retrieve persons that match the query (limited to nearest 5 vectors)

- GET /persons/elastic_search/?q=jey : Elasticsearch implementation to Fuzzy search on full name of Person, eg. if theres a person named Jay Chhatrala, and if you query by jey or chhaatrraala , it will return the instance of Jay Chhatrala


## Installation

1. Clone the Repository 

```
git clone https://github.com/jaychhatrala23/obviously.git
cd obviously
```

2. Build and Run the Docker container

```
docker-compose up --build
```

3. Access the endpoints 

- Server will run on http://localhost:8000
- Use the API endpoints as defined above.
