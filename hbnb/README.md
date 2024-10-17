# HbNb Application

## Business Logic Layer

The business logic layer contains the core entities of our application. These entities represent the main concepts and operations of our vacation rental platform.

### User

The `User` class represents a user of our platform.

Responsibilities:
- Store user information (first name, last name, email)
- Manage user authentication status

Example usage:
```python
user = User("John", "Doe", "john.doe@example.com")
print(user.full_name)  # Output: John Doe
user.email = "new.email@example.com"  # This will validate the email format

Place
The Place class represents a rental property on our platform.
Responsibilities:
Store property information (title, description, price, location)
Manage the relationship with the owner (User)
Handle reviews and amenities associated with the property
Example usage:

owner = User("Alice", "Smith", "alice@example.com")
place = Place("Cozy Cabin", "A beautiful cabin in the woods", owner, price=100.0, latitude=45.5, longitude=-122.6)
place.add_amenity("WiFi")
print(place.title)  # Output: Cozy Cabin

Review
The Review class represents a review left by a user for a specific place.
Responsibilities:
Store review content (text, rating)
Manage the relationship with the user who wrote the review and the place being reviewed
Example usage:

user = User("Bob", "Johnson", "bob@example.com")
place = Place("Beach House", "Lovely house by the sea", owner, price=150.0)
review = Review("Great stay!", 5, place, user)
place.add_review(review)
print(len(place.reviews))  # Output: 1

File Structure
app/
__init__.py: Configures the Flask application with placeholders.
models/
user.py: Defines the User class.
place.py: Defines the Place class.
review.py: Defines the Review class.
persistence/
repository.py: Implements the in-memory repository.
services/
facade.py: Plans the facade pattern with placeholders.
run.py: Creates the entry point.
config.py: Prepares the configuration.
How to Use
Create instances of User, Place, and Review as needed.
Use the Facade (once implemented) to interact with the system in a simplified manner.
The Repository will handle data persistence (currently in-memory).
Note: This is a work in progress. Further implementations will include more detailed business logic, data validation, and integration with the web framework.


This README now includes information about the business logic layer, describing the main entities (User, Place, Review) and their responsibilities. It also provides examples of how these classes can be used. The file structure section has been updated to include the new model files we've been working on. 

Remember to keep this README updated as you continue to develop your application, adding more details about new features, classes, or usage instructions as they are implemented.