-- ============================
-- Users
-- ============================
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- Workouts (single text field for full workout)
-- ============================
CREATE TABLE workouts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    date            DATE NOT NULL,

    workout_text    TEXT NOT NULL,

    energy_level    INTEGER,
    notes           TEXT,
    metadata        TEXT,

    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================
-- Meals (single text field for description)
-- ============================
CREATE TABLE meals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    date            DATE NOT NULL,

    name            TEXT NOT NULL,
    description     TEXT,

    calories        INTEGER,
    protein         INTEGER,
    carbs           INTEGER,
    fat             INTEGER,

    notes           TEXT,
    metadata        TEXT,

    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================
-- Embedding Index (optional helper)
-- Tracks what has been embedded for ChromaDB
-- ============================
CREATE TABLE embedding_index (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type     TEXT NOT NULL,
    source_id       INTEGER NOT NULL,
    last_embedded   DATETIME DEFAULT CURRENT_TIMESTAMP
);
