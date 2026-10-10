-- Лабораторна робота №4. Організація набору даних у MySQL засобами MySQL Workbench
-- Варіант 4. База даних про книги, куплені бібліотекою:
-- назва, автор, рік видання, адреса автора, адреса видавництва, ціна, книготорговельна фірма.

-- 1. Створення бази даних (схеми)
DROP SCHEMA IF EXISTS `library4`;
CREATE SCHEMA `library4` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `library4`;

-- 2. Таблиця Автор (author)
CREATE TABLE author (
  id_author INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  address VARCHAR(200) NOT NULL,
  PRIMARY KEY (id_author)
);

-- 3. Таблиця Видавництво (publisher)
CREATE TABLE publisher (
  id_publisher INT UNSIGNED NOT NULL AUTO_INCREMENT,
  city VARCHAR(50) NOT NULL,
  country VARCHAR(50) NOT NULL,
  PRIMARY KEY (id_publisher)
);

-- 4. Таблиця Книготорговельна фірма (bookstore)
CREATE TABLE bookstore (
  id_bookstore INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_bookstore)
);

-- 5. Таблиця Книга (book) - головна таблиця
CREATE TABLE book (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  publication_year SMALLINT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  id_author INT UNSIGNED NOT NULL,
  id_publisher INT UNSIGNED NOT NULL,
  id_bookstore INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_author) REFERENCES author (id_author),
  FOREIGN KEY (id_publisher) REFERENCES publisher (id_publisher),
  FOREIGN KEY (id_bookstore) REFERENCES bookstore (id_bookstore)
);

-- 6. Заповнення таблиць даними (ті самі книги, що й у практикумі №1)
INSERT INTO `library4`.`author` (`id_author`, `name`, `address`)
VALUES
(NULL, 'Тарас Шевченко', 'м. Київ, Україна'),
(NULL, 'Леся Українка', 'м. Київ, Україна'),
(NULL, 'Іван Багряний', 'м. Охтирка, Україна'),
(NULL, 'Валер’ян Підмогильний', 'м. Київ, Україна'),
(NULL, 'Іван Франко', 'м. Львів, Україна');

INSERT INTO `library4`.`publisher` (`id_publisher`, `city`, `country`)
VALUES
(NULL, 'м. Київ', 'Україна'),
(NULL, 'м. Харків', 'Україна'),
(NULL, 'м. Львів', 'Україна');

INSERT INTO `library4`.`bookstore` (`id_bookstore`, `name`)
VALUES
(NULL, 'Книгарня Є'),
(NULL, 'Yakaboo'),
(NULL, 'Книголенд'),
(NULL, 'Наш Формат');

INSERT INTO `library4`.`book` (
  `id`, `title`, `publication_year`, `price`,
  `id_author`, `id_publisher`, `id_bookstore`
)
VALUES
(NULL, 'Кобзар', 1840, 350.00, 1, 1, 1),
(NULL, 'Лісова пісня', 1911, 280.00, 2, 1, 2),
(NULL, 'Тигролови', 1944, 320.00, 3, 2, 3),
(NULL, 'Місто', 1928, 300.00, 4, 2, 1),
(NULL, 'Захар Беркут', 1883, 275.00, 5, 3, 4);
