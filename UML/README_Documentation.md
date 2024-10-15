
# HBnB Project - Technical Documentation

## Introduction

This document serves as the technical guide for the implementation of the HBnB project.

The documentation includes various architectural diagrams, detailed class models, and API interaction flows that guide the development and design of the system.

The goal of this document is to provide a comprehensive overview of the system architecture, the structure of key business entities, and the flow of API calls within the application. It will help developers understand the core design decisions and implement the system in a structured and efficient way.



## High-Level Architecture

The application follows a **layered architecture** consisting of three main layers:

- **Presentation Layer**: This layer handles user interactions and API endpoints.
- **Business Logic Layer**: This layer manages the application's core business rules and operations.
- **Persistence Layer**: This layer is responsible for database interactions and data storage.


### Explanation:

- The **Presentation Layer** exposes a service API for user interaction and communication with the Business Logic Layer.
- The **Business Logic Layer** manages the core operations, validating and processing the user requests.
- The **Persistence Layer** manages the interaction with the database, performing data retrieval and storage operations.

- The **User**, **Place**, **Review**, and **Amenity** entities represent the main components of the system.
- The **Presentation Layer** (UI and API) interacts directly with the business models in the Business Logic Layer.
- Each business entity interacts with its corresponding repository in the Persistence Layer to store and retrieve data.

The system design employs the **Facade Pattern** between the Presentation Layer and Business Logic Layer to simplify interaction and isolate complexity. Below is the high-level architecture diagram:


```mermaid

graph TD;

	subgraph Presentation layer
		UI[user interface]
		API[end points]
	end

	subgraph Business Logic Layer
		User[User Model]
		Place[Place Model]
		Review[Review Model]
		Amenity[Amenity Model]
	end

	subgraph Persistence Layer
		User_repo[user data]
		Place_repo[place data]
		Review_repo[review data]
		Amenity_repo[Amenity data]
	end

	UI --> API

	API --> User
	API --> Review
	API --> Place
	Place --> Amenity


	User --> User_repo
	Place --> Place_repo
	Review --> Review_repo
	Amenity --> Amenity_repo

```



## Business Logic Layer - Class Diagram

The **Business Logic Layer** contains the primary entities responsible for managing user data, accommodation listings (places), reviews, and amenities. Below is the detailed class diagram that outlines the main entities and their relationships:



### Explanation:


Each core business entity is modeled with a base class that includes basic functionalities like creating, updating, and deleting entries:

- The **Entity** base class provides common functionalities such as create, update, and delete for all business entities.
- The **User** class manages user-related information and operations such as registering and updating user details.
- The **Place** class represents accommodation listings, storing details like price and location.
- the **Review** classe associated with a user place contains comments that user can give to a place.
- the **Amenity** classe associated to user's place contains all the commodities belongin to a user's place

```mermaid

classDiagram

	class Entity {
		+id: String
		+createdAt: Date
		+updatedAt: Date
		+create()
		+update()
		+delete()
	}

	class User {
		+first_name: String
		+last_name: String
		+email: String
		+pass_word: String

		+check_administrator()
		+register_user()
		+update_user_info()
		+create()
		+update()
		+delete()
	}

	class Place {
		+title: String
		+price: Float
		+latitude: Float
		+longitude: Float

		+owner()
		+list_of_amenities()
		+create()
		+update()
		+delete()
	}

	class Review {
		+rating: int
		+comment: String

		+association_to_user()
		+association_to_place()
		+create()
		+update()
		+delete()
	}

	class Amenity {
		+name: String
		+description: String

		+list()
		+association_to_place()
	}

	Entity <|-- User
	Entity <|-- Place
	Entity <|-- Review
	Entity <|-- Amenity

```



## API Interaction Flow

The following sequence diagrams illustrate the interactions between the user, API, business logic, and persistence layers during key API calls.

```mermaid

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Persistence(DataBase)

    User->>API: createUser(first_name, last_name, email, pass_word)
    API-->>User: Return Success/Failure

    User->>API: updateUserInfo(userId, newInfo)
    API-->>User: Return Success/Failure

    User->>API: getOwnerInfo(userId)
    API-->>User: Return Success/Failure

    User->>API: addComment(reviewId, comment)
    API-->>User: Return Success/Failure

    API->>BusinessLogic: validateAndProcessRequest(request)
    BusinessLogic->>Persistence(DataBase): saveUserData(userData)
    Persistence(DataBase)-->>BusinessLogic: confirmSave()
    BusinessLogic-->>API: returnResponse(dataSaved)
    API-->>User: Return Success

```

### EXEMPLE User Registration Flow

The following sequence diagram demonstrates the process of a user registration:

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Persistence(DataBase)

    User->>API: createUser(first_name, last_name, email, pass_word)
    API-->>User: Return Success/Failure

    API->>BusinessLogic: validateAndProcessRequest(request)
    BusinessLogic->>Persistence(DataBase): saveUserData(userData)
    Persistence(DataBase)-->>BusinessLogic: confirmSave()
    BusinessLogic-->>API: returnResponse(dataSaved)
    API-->>User: Return Success
```

### Explanation:
- The user initiates a request to create a new account by sending their details to the API.
- The API forwards the request to the Business Logic Layer for validation and processing.
- After processing, the data is stored in the database via the Persistence Layer, and a success or failure response is sent back to the user.

### Additional API Calls

Similarly, other API calls follow this structure, such as updating user information, adding reviews, or retrieving user data:

```mermaid
sequenceDiagram
    User->>API: updateUserInfo(userId, newInfo)
    API-->>User: Return Success/Failure

    User->>API: getOwnerInfo(userId)
    API-->>User: Return Success/Failure

    User->>API: addComment(reviewId, comment)
    API-->>User: Return Success/Failure
```

### Explanation:
- The **updateUserInfo** call allows users to update their profile details.
- The **getOwnerInfo** call fetches the details of the place owner.
- The **addComment** API call enables users to add comments to reviews.

Each API call follows a similar sequence, passing through the API, Business Logic, and Persistence layers to complete the operation.
