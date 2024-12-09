CREATE TABLE USERS (
    user_id TEXT,
    email TEXT,
    geo TEXT
)

CREATE TABLE LOG (
    user_id TEXT,
    time DATETIME,
    bet REAL,
    win REAL
)