CREATE DATABASE IF NOT EXISTS hbnb;
USE hbnb;

CREATE TABLE IF NOT EXISTS User(
	id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place(
	id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	price DECIMAL(10, 2),
	latitude FLOAT,
	longitude FLOAT,
	owner_id CHAR(36) NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Review(
	id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
	text TEXT NOT NULL,
	rating INT CHECK (rating >= 1 AND rating <= 5),
	user_id CHAR(36) NOT NULL,
	place_id CHAR(36) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES User(id),
	FOREIGN KEY (place_id) REFERENCES Place(id),
	CONSTRAINT unique_review UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity(
	id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
	name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS Place_Amenity(
	place_id CHAR(36) NOT NULL,
	amenity_id CHAR(36) NOT NULL,
	PRIMARY KEY (place_id, amenity_id),
	FOREIGN KEY (place_id) REFERENCES Place(id),
	FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT INTO User(id, email, first_name, last_name, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', '$2b$12$dKueCc6RAmJrnsq2brIuJOmwca3hFAr9zPg1o713PSIwbln8BWd16', TRUE);

INSERT INTO Amenity(id, name)
VALUES	(UUID(), 'WiFi'),
		(UUID(), 'Swimming Pool'),
		(UUID(), 'Air Conditioning');
