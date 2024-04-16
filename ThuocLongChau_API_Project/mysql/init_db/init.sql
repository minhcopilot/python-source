CREATE DATABASE thuoclongchau;
USE thuoclongchau;

CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  parent_name VARCHAR(255),
  slug VARCHAR(255),
  level INT,
  is_active BOOLEAN
);

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(255),
  name VARCHAR(255),
  webName VARCHAR(255),
  image TEXT,
  category_id INT,
  price DECIMAL(10,2),
  slug VARCHAR(255),
  ingredients TEXT,
  dosage_form VARCHAR(255),
  brand VARCHAR(255),
  display_code INT,
  is_active BOOLEAN,
  is_publish BOOLEAN,
  search_scoring FLOAT,
  product_ranking FLOAT,
  specification TEXT,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);