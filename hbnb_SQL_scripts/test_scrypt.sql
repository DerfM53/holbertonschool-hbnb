-- Vérification de l'utilisateur admin
SELECT * FROM User WHERE email = 'admin@hbnb.io';

-- Vérification des commodités
SELECT * FROM Amenity;

-- Test de la mise à jour de l'utilisateur admin
UPDATE User
SET first_name = 'Administrator'
WHERE email = 'admin@hbnb.io';

-- Vérification après mise à jour
SELECT * FROM User WHERE email = 'admin@hbnb.io';



-- Vérification après suppression
SELECT * FROM User WHERE email = 'admin@hbnb.io';

-- Test d'ajout de nouvelle commodité
INSERT INTO Amenity(id, name) VALUES (UUID(), 'Gym');

-- Vérification des commodités après ajout
SELECT * FROM Amenity;

DELETE FROM Amenity WHERE name = 'WiFi';

SELECT * FROM Amenity;
