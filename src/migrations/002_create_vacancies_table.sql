CREATE TABLE vacancies
(
    id          INTEGER PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    url         VARCHAR(255) NOT NULL,
    type        VARCHAR(255) NOT NULL,
    salary_from INTEGER,
    salary_to   INTEGER,
    employer_id INTEGER NOT NULL,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);
