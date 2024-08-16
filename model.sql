-- Create the Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create the UserRestrictions table
CREATE TABLE UserRestrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restricted_user_id INTEGER NOT NULL,
    year INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (restricted_user_id) REFERENCES Users(id),
    UNIQUE (user_id, restricted_user_id, year)
);

-- Create the Wishlists table
CREATE TABLE Wishlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    wishlist TEXT,
    year INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    UNIQUE (user_id, year)
);

-- Create the SecretSantaAssignments table
CREATE TABLE SecretSantaAssignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gifter_id INTEGER NOT NULL,
    giftee_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (gifter_id) REFERENCES Users(id),
    FOREIGN KEY (giftee_id) REFERENCES Users(id),
    UNIQUE (gifter_id, year),
    UNIQUE (giftee_id, year)
);
