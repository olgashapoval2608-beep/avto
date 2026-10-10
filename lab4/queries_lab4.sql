USE `library4`;

-- Q1. Перегляд таблиць (Select Rows)
SELECT * FROM author;
SELECT * FROM publisher;
SELECT * FROM bookstore;
SELECT * FROM book;

-- Q2. WHERE: книга з назвою 'Кобзар'
SELECT *
FROM `book`
WHERE title = 'Кобзар';

-- Q3. WHERE з вибіркою з двох таблиць: книга 'Кобзар' та її автор
SELECT *
FROM `book`, `author`
WHERE title = 'Кобзар'
AND book.id_author = author.id_author;

-- Q4. Реляційні та булеві оператори: книги, видані після 1900 року, разом з автором
SELECT *
FROM book, author
WHERE book.publication_year > 1900
AND book.id_author = author.id_author;

-- Q5. Реляційні та булеві оператори: книги дорожчі за 280 грн, але не з Харкова
SELECT book.title, book.price, publisher.city
FROM book, publisher
WHERE book.price >= 280 AND NOT publisher.city = 'м. Харків'
AND book.id_publisher = publisher.id_publisher;

-- Q6. OR: книги, куплені у фірм 'Книгарня Є' або 'Yakaboo'
SELECT book.title, book.price, bookstore.name
FROM book, bookstore
WHERE (bookstore.name = 'Книгарня Є' OR bookstore.name = 'Yakaboo')
AND book.id_bookstore = bookstore.id_bookstore;

-- Q7. IN: те саме, переписане через IN
SELECT book.title, book.price, bookstore.name
FROM book, bookstore
WHERE bookstore.name IN ('Книгарня Є', 'Yakaboo')
AND book.id_bookstore = bookstore.id_bookstore;

-- Q8. ORDER BY ... ASC: книги за зростанням ціни
SELECT title, publication_year, price
FROM book
ORDER BY price ASC;

-- Q9. ORDER BY ... DESC: книги за спаданням року видання
SELECT title, publication_year, price
FROM book
ORDER BY publication_year DESC;

-- Самостійно 1. Знайти назву книги, автора та країну видавництва, якщо ціна книги = 350
SELECT book.title, author.name, publisher.country
FROM book, author, publisher
WHERE book.price = 350
AND book.id_author = author.id_author
AND book.id_publisher = publisher.id_publisher;

-- Самостійно 2. Знайти назви книг, якщо видавництво знаходиться в м. Харків
SELECT book.title
FROM book, publisher
WHERE publisher.city = 'м. Харків'
AND book.id_publisher = publisher.id_publisher;

-- Підсумковий запит: повна інформація про кожну книгу (усі 8 полів варіанта)
SELECT book.id, book.title, author.name AS author, book.publication_year,
       author.address AS author_address,
       CONCAT(publisher.city, ', ', publisher.country) AS publisher_address,
       book.price, bookstore.name AS bookstore
FROM book, author, publisher, bookstore
WHERE book.id_author = author.id_author
AND book.id_publisher = publisher.id_publisher
AND book.id_bookstore = bookstore.id_bookstore
ORDER BY book.id;
