create table telegrambot.OnexData (
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
team1 VARCHAR(150) NOT NULL,
team2 VARCHAR(150) NOT NULL,
start_date VARCHAR(255) NOT NULL,
title VARCHAR(255) NOT NULL,
INDEX (team1, team2, start_date)
)