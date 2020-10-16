CREATE DATABASE neovox_test;

CREATE USER 'neovox_user'@'localhost' IDENTIFIED BY 'neovox_pass';
GRANT ALL ON neovox_test.* TO 'neovox_user'@'localhost';

CREATE TABLE neovox_products (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, product_name VARCHAR(30) NOT NULL, description VARCHAR(200), value INT DEFAULT 0);

INSERT neovox_products (product_name, description, value) VALUES ('Laptop', 'Is a small, portable personal computer with a clamshell form factor', 1);
INSERT neovox_products (product_name, description, value) VALUES ('Mobile phone', 'Portable telephone that can make and receive calls over a radio frequency', 1);
INSERT neovox_products (product_name, description, value) VALUES ('Headset', 'Communication accessory, which is a combination of headphones with a microphone', 1);
