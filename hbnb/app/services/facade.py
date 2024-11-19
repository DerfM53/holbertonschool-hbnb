from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self, user_repo, place_repo, amenity_repo, review_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.amenity_repo = amenity_repo
        self.review_repo = review_repo

    def create_user(self, user_data):
        # Vérifier si l'email existe déjà
        if self.user_repo.find_by_email(user_data['email']):
            raise ValueError("Email already registered")
    
        # Créer un nouvel utilisateur avec le mot de passe
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
    
        # Sauvegarder l'utilisateur
        return self.user_repo.add(new_user)
    
    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user is None:
            print(f"User with ID {user_id} not found")  # Ajoutez ce log pour le débogage
            raise ValueError("User not found")  # Lever une exception explicite
        return user
    
    def get_user_by_email(self, email):
        return self.user_repo.find_by_email(email)
    
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
    
        user.update(user_data)  # Utilise la méthode update du modèle User
        return user
    
    def delete_user(self, user_id):
        """Delete a user by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)  # Supposons que votre dépôt a une méthode delete
        return True

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Amenity name is required")
        new_amenity = Amenity(name=amenity_data['name'])
        if not hasattr(new_amenity, 'id') or new_amenity.id is None:
            raise ValueError("Amenity object does not have a valid ID")
        self.amenity_repo.add(new_amenity)
        return new_amenity
        
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity by ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)  # Supposons que votre dépôt a une méthode delete
        return True
    
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"User with ID {owner_id} not found")
        new_place = Place(**place_data, owner_id=owner_id)
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            print(f"Place with ID {place_id} not found")  # Log pour le débogage
            raise ValueError("Place not found")  # Lever une exception explicite
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    def create_review(self, review_data):
        # Vérifiez si le texte est vide
        if not review_data.get('text'):
            raise ValueError("Text cannot be empty")

        # Vérifiez si l'utilisateur et le lieu existent
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found")
    
        # Créez la nouvelle revue
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )

        # Ajoutez la revue au dépôt
        self.review_repo.add(new_review)
        return new_review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
    
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")
    
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return True
    
    def is_user_admin(self, user_id):
        """
        Vérifie si un utilisateur est un administrateur.
        
        Args:
            user_id (str): L'ID de l'utilisateur à vérifier.
        
        Returns:
            bool: True si l'utilisateur est un administrateur, False sinon.
        """
        user = self.get_user(user_id)
        return user.is_admin if user else False

    def is_review_owner(self, review_id, user_id):
        """
        Vérifie si un utilisateur est le propriétaire d'une review.
        
        Args:
            review_id (str): L'ID de la review.
            user_id (str): L'ID de l'utilisateur.
        
        Returns:
            bool: True si l'utilisateur est le propriétaire de la review, False sinon.
        """
        review = self.get_review(review_id)
        return review.user_id == user_id if review else False

    def can_modify_review(self, review_id, user_id):
        """
        Vérifie si un utilisateur peut modifier une review (propriétaire ou admin).
        
        Args:
            review_id (str): L'ID de la review.
            user_id (str): L'ID de l'utilisateur.
        
        Returns:
            bool: True si l'utilisateur peut modifier la review, False sinon.
        """
        return self.is_review_owner(review_id, user_id) or self.is_user_admin(user_id)
