:::mermaid

classDiagram

    class User {
        +String id
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
    }

    class Place {
        +String id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
    }

    class Review {
        +String id
        +String text
        +Int rating
        +String place_id
        +String user_id
    }

    class Amenity {
        +String id
        +String name
    }

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Amenity "0..*" --> "0..*" Place : available at
    Review "1" --> "1" User : written by
    Review "1" --> "1" Place : for
    
:::
