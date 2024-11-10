# HBnB - Holberton Bed and Breakfast

HBnB is a rental management application inspired by Airbnb. It allows users to create accounts, list properties, make reservations, and leave reviews.

## Architecture

The application is structured as follows:

hbnb/
├── app/
│ ├── init.py
│ ├── api/
│ │ ├── init.py
│ │ ├── v1/
│ │ ├── init.py
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ ├── amenities.py
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ ├── amenity.py
│ ├── services/
│ │ ├── init.py
│ │ ├── facade.py
│ ├── persistence/
│ ├── init.py
│ ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md


## Features

- User management (creation, retrieval)
- Property management (creation, retrieval, updating)
- Review management (creation, retrieval, updating, deletion)
- Amenity management (creation, retrieval, updating)

## Technologies Used

- Python 3
- Flask: Web framework
- Flask-RESTX: Extension for creating RESTful APIs

## Installation

1. Clone this repository.
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`

## API Usage

The API is accessible at `http://localhost:5000/`. The Swagger documentation for the API is available at `http://localhost:5000/`.

### Example Endpoints:

- Create a user: `POST /api/v1/users/`
- Retrieve a user: `GET /api/v1/users/<user_id>`
- Create a place: `POST /api/v1/places/`
- Retrieve all places: `GET /api/v1/places/`

## Objective

Develop a RESTful API with Flask that allows interaction with a database to manage entities such as Users, Places, Aménities and Reviews.

## Advanced Features

- User management with CRUD operations (Create, Read, Update).
- Use of UUID to ensure unique user IDs.
- Layered architecture to separate business logic and database interactions.
- Compliance with REST standards for API endpoint structure.

## Authors

- **Fred Mieuzet** [GitHub](https://github.com/DerfM53)
- **Mohamed Lamine Bouricha** [GitHub](https://github.com/Xdamix1991)
- **Mehdi Zemihi** [GitHub](https://github.com/MrSandouiche2)


## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
