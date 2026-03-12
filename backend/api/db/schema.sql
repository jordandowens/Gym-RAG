-- ============================
-- Users
-- ============================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- Workouts (single text field for full workout)
-- ============================
CREATE TABLE workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,

    workout_text TEXT NOT NULL,

    energy_level INT,
    notes TEXT,
    metadata TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================
-- Meals (single text field for description)
-- ============================
CREATE TABLE meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,

    name VARCHAR(255) NOT NULL,
    description TEXT,

    calories INT,
    protein INT,
    carbs INT,
    fat INT,

    notes TEXT,
    metadata TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================
-- Embedding Index
-- ============================
CREATE TABLE embedding_index (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_type VARCHAR(255) NOT NULL,
    source_id INT NOT NULL,
    last_embedded DATETIME DEFAULT CURRENT_TIMESTAMP
);
