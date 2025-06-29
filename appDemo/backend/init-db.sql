-- Create the compression_log table to match your SQLAlchemy model
DROP TABLE IF EXISTS compression_log;
CREATE TABLE compression_log
(
    id         SERIAL PRIMARY KEY,
    filename   VARCHAR(120) NOT NULL,
    method     VARCHAR(20)  NOT NULL,
    quality    INTEGER,
    k_value    INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);