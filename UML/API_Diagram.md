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
