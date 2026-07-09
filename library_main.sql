DROP DATABASE library;
CREATE DATABASE library 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
use library;
show databases;

create table genres(
genre_id int auto_increment,
genre_name varchar(100) not null unique,
primary key(genre_id));

create table book (
book_id int auto_increment ,
title varchar(255) not null,
author varchar(255) not null,
book_year int not null,
edition varchar(255),
genre_id int,
total_copies bigint,
available_copies int,
book_description text,
cover_path varchar(255),
created_at timestamp,
primary key(book_id),
foreign key(genre_id) references genres(genre_id)
);

 alter table book 
 add constraint chk_available_cop
 check(available_copies >=0 and available_copies <= total_copies);

create index idx_book_title on book(title);
create index idx_book_author on book(author);
create index idx_book_genre on book(genre_id);

create table users (
user_id int auto_increment,
full_name varchar(100) not null,
email varchar(100) unique not null,
user_role enum('admin', 'teacher', 'student'),
faculty varchar(100),
phone varchar(20),
reg_date date,
is_active bool,
primary key(user_id)
);

create table loans(
loan_id int auto_increment,
book_id int not null,
user_id int not null,
loan_date date not null,
due_date date not null,
return_date date,
status_loan enum('active', 'returned', 'overdue', 'lost'),
primary key(loan_id),
foreign key(book_id) references book(book_id) on delete restrict,
foreign key(user_id) references users(user_id) on delete restrict
);

create index idx_loans_user on loans(user_id);
create index idx_loans_status on loans(status_loan);

create table fines (
fine_id int auto_increment,
loan_id int not null,
user_id int not null,
amount decimal(8,2) not null,
per_date_rate decimal(6,2) not null,
days_overdue int not null,
created_at datetime not null,
paid_at datetime,
is_paid boolean not null default false,
primary key (fine_id),
foreign key(loan_id) references loans(loan_id) on delete cascade,
foreign key(user_id) references users(user_id) on delete restrict
);

create table reservation(
reservation_id int auto_increment,
book_id int not null,
user_id int not null,
reservation_date datetime not null,
expiry_date datetime,
status_res enum('reserved', 'waiting', 'fulfilled','cancelled', 'expired'),
primary key(reservation_id),
foreign key(book_id) references book(book_id) on delete cascade,
foreign key(user_id) references users(user_id) on delete cascade
);

INSERT INTO genres (genre_name) VALUES 
('Программирование'), ('Математика'), ('Физика'), ('Художественная литература'), 
('История'), ('Психология'), ('Биология'), ('Философия');


INSERT INTO book (title, author, book_year, edition, genre_id, total_copies, available_copies, book_description, cover_path) VALUES
('Чистый код', 'Роберт Мартин', 2008, '1-е издание', 1, 10, 10, 'Руководство по созданию качественного кода.', 'CHistiy_kod.jpg'),
('Совершенный код', 'Стив Макконнелл', 2004, '2-е издание', 1, 5, 5, 'Практическое руководство по конструированию ПО.', 'Sovershenniy_kod.jpg'),
('Алгоритмы: построение и анализ', 'Томас Кормен', 2013, '3-е издание', 1, 8, 8, 'Фундаментальный труд по алгоритмам.', 'Introduction_to_Algorithms_2nd_Russian_cover.jpg'),
('1984', 'Джордж Оруэлл', 1949, 'Классика', 4, 15, 12, 'Знаменитая антиутопия.', 'orall.jpg'),
('О дивный новый мир', 'Олдос Хаксли', 1932, 'Классика', 4, 10, 10, 'Антиутопия о обществе потребления.', 'dvi.jpg'),
('Краткая история времени', 'Стивен Хокинг', 1988, 'Популярная наука', 3, 7, 7, 'О происхождении Вселенной.','Kratkaya_istoriya_vremeni_Stiven_Hoking.jpg'),
('Думай медленно... решай быстро', 'Даниэль Канеман', 2011, '1-е издание', 6, 12, 11, 'Психология принятия решений.', 'ss.jpg'),
('Sapiens: Краткая история человечества', 'Юваль Ной Харари', 2011, '1-е издание', 5, 20, 18, 'История нашего вида.', 'as.jpg'),
('Эгоистичный ген', 'Ричард Докинз', 1976, 'Юбилейное издание', 7, 6, 6, 'Основы эволюции.', '9.jpg'),
('Государство', 'Платон', -375, 'Философия', 8, 5, 5, 'Диалоги о справедливости и политике.', '10.jpg'),
('Мастер и Маргарита', 'Михаил Булгаков', 1967, 'Классика', 4, 25, 20, 'Роман о дьяволе в Москве.', '11.jpg'),
('Преступление и наказание', 'Федор Достоевский', 1866, 'Классика', 4, 15, 15, 'Психологический роман.', '12.jpg'),
('Война и мир', 'Лев Толстой', 1869, 'Классика', 4, 10, 10, 'Эпопея о войне и обществе.', '13.jpg'),
('Паттерны объектно-ориентированного проектирования', 'Эрих Гамма', 1994, '1-е издание', 1, 7, 7, 'Классика проектирования ПО.', '14.jpg'),
('Грокаем алгоритмы', 'Адитья Бхаргава', 2017, 'Иллюстрированное', 1, 30, 25, 'Алгоритмы для начинающих.', '15.jpg'),
('Выразительный JavaScript', 'Марейн Хавербеке', 2018, '3-е издание', 1, 10, 10, 'Современное программирование на JS.', '16.jpg'),
('Изучаем Python', 'Марк Лутц', 2013, '5-е издание', 1, 12, 9, 'Полное руководство по Python.', '17.png'),
('CLR via C#', 'Джеффри Рихтер', 2012, '4-е издание', 1, 8, 8, 'Глубокое погружение в .NET.','18.jpg'),
('Архитектура компьютера', 'Эндрю Таненбаум', 2013, '6-е издание', 1, 5, 5, 'Устройство ЭВМ.', '19.jpg'),
('Критика чистого разума', 'Иммануил Кант', 1781, 'Философия', 8, 4, 4, 'Фундаментальная работа по теории познания.', '20.jpg'),
('Человек в поисках смысла', 'Виктор Франкл', 1946, 'Психология', 6, 15, 14, 'О логотерапии и смысле жизни.', '21.jpg'),
('Искусство войны', 'Сунь-цзы', -500, 'Трактат', 5, 20, 20, 'Древнекитайская стратегия.', '22.jpg'),
('Так говорил Заратустра', 'Фридрих Ницше', 1883, 'Философия', 8, 10, 10, 'Философская поэма.', '23.jpg'),
('Братья Карамазовы', 'Федор Достоевский', 1880, 'Классика', 4, 12, 12, 'Последний роман автора.', '24.jpg'),
('Анна Каренина', 'Лев Толстой', 1877, 'Классика', 4, 10, 10, 'Трагическая история любви.', '25.jpg'),
('Божественная комедия', 'Данте Алигьери', 1320, 'Классика', 4, 8, 8, 'Путешествие по загробному миру.', '26.jpg'),
('Улисс', 'Джеймс Джойс', 1922, 'Модернизм', 4, 5, 5, 'Сложный роман одного дня.', '27.jpg'),
('Фауст', 'Иоганн Гёте', 1808, 'Классика', 4, 6, 6, 'Трагедия о сделке с дьяволом.', '28.jpg'),
('Сто лет одиночества', 'Габриэль Маркес', 1967, 'Магический реализм', 4, 14, 13, 'История рода Буэндиа.', '29.jpg'),
('Великий Гэтсби', 'Фрэнсис Фицджеральд', 1925, 'Классика', 4, 18, 15, 'Американская мечта.',  '30.jpg'),
('Три товарища', 'Эрих Мария Ремарк', 1936, 'Классика', 4, 20, 20, 'О дружбе и любви после войны.', '31.jpg'),
('На западном фронте без перемен', 'Эрих Мария Ремарк', 1929, 'Классика', 4, 15, 15, 'Антивоенный роман.', '32.jpg'),
('Старик и море', 'Эрнест Хемингуэй', 1952, 'Классика', 4, 12, 12, 'Повесть о мужестве.', '33.jpg'),
('Прощай, оружие!', 'Эрнест Хемингуэй', 1929, 'Классика', 4, 10, 10, 'Любовь на фоне войны.', '34.jpg'),
('По ком звонит колокол', 'Эрнест Хемингуэй', 1940, 'Классика', 4, 9, 9, 'Гражданская война в Испании.', '35.jpg'),
('Маленький принц', 'Антуан де Сент-Экзюпери', 1943, 'Сказка', 4, 30, 28, 'Мудрая сказка для всех.', '36.jpg'),
('Дюна', 'Фрэнк Герберт', 1965, 'Фантастика', 4, 20, 17, 'Великая научно-фантастическая сага.', '37.jpg'),
('Хоббит', 'Дж. Р. Р. Толкин', 1937, 'Фэнтези', 4, 25, 25, 'Путешествие Бильбо Бэггинса.', '38.jpg'),
('Властелин колец', 'Дж. Р. Р. Толкин', 1954, 'Фэнтези', 4, 30, 24, 'Эпическое фэнтези.', '39.jpg'),
('Марсианские хроники', 'Рэй Брэдбери', 1950, 'Фантастика', 4, 15, 15, 'Рассказы о Марсе.', '40.jpg'),
('451 градус по Фаренгейту', 'Рэй Брэдбери', 1953, 'Антиутопия', 4, 20, 18, 'Мир без книг.', '41.jpg'),
('Цветы для Элджернона', 'Дэниел Киз', 1966, 'Драма', 6, 12, 10, 'История об изменении интеллекта.', '42.jpg'),
('Повелитель мух', 'Уильям Голдинг', 1954, 'Классика', 4, 10, 10, 'Одичание детей на острове.', '43.jpg'),
('Над пропастью во ржи', 'Джером Сэлинджер', 1951, 'Классика', 4, 15, 14, 'История подростка Холдена.', '44.jpg'),
('Портрет Дориана Грея', 'Оскар Уайльд', 1890, 'Классика', 4, 18, 16, 'Вечная молодость и грех.', '45.jpg'),
('Герой нашего времени', 'Михаил Лермонтов', 1840, 'Классика', 4, 20, 20, 'Психологический портрет поколения.', '46.jpg'),
('Евгений Онегин', 'Александр Пушкин', 1833, 'Классика', 4, 25, 25, 'Энциклопедия русской жизни.', '47.jpg'),
('Мертвые души', 'Николай Гоголь', 1842, 'Классика', 4, 15, 15, 'Поэма о России.', '48.jpg'),
('Отцы и дети', 'Иван Тургенев', 1862, 'Классика', 4, 12, 12, 'Конфликт поколений.', '49.jpg'),
('Обломов', 'Иван Гончаров', 1859, 'Классика', 4, 10, 10, 'Роман о лени и душе.', '50.jpg');


INSERT INTO book (title, author, book_year, edition, genre_id, total_copies, available_copies, book_description, cover_path) VALUES
('Что такое математика?', 'Рихард Курант, Герберт Роббинс', 1999, '3-е издание', 2, 12, 10, 'Введение в математические концепции и методы.', '1.1.jpg'),
('Начала', 'Евклид', 2019, 'Классика', 2, 8, 8, 'Фундаментальный труд по геометрии и теории чисел.', '1.2.jpg'),
('Искусство счета', 'Владимир Арнольд', 2003, '2-е издание', 2, 10, 7, 'Сборник задач и лекций по математике.', '1.3.jpg'),
('Математический анализ', 'Владимир Зорич', 2019, '7-е издание', 2, 15, 12, 'Классический учебник математического анализа для университетов.', '1.4.jpg'),
('Теория вероятностей', 'Андрей Колмогоров', 2005, '4-е издание', 2, 10, 10, 'Базовый курс теории вероятностей.', '1.5.jpg'),
('Наглядная геометрия', 'Владимир Арнольд', 2004, '1-е издание', 2, 12, 9, 'Интуитивное введение в геометрию.', '1.6.jpg'),
('Математика. Ее содержание, методы и значение', 'А. Д. Александров, А. Н. Колмогоров, М. А. Лаврентьев', 1956, '1-е издание', 5, 7, 5, 'Трехтомный труд о сути и истории математики.', '1.7.jpg'),
('Введение в теорию графов', 'Фрэнк Харари', 2003, '2-е издание', 2, 14, 11, 'Классический учебник по теории графов.', '1.8.jpg'),
('Высшая математика для начинающих и ее приложения к физике', 'Я. Б. Зельдович, И. М. Яглом', 2015, '3-е издание', 2, 20, 18, 'Отличное введение в матанализ для физиков и инженеров.', '1.9.jpg'),
('Лекции по математическому анализу', 'Л. Д. Кудрявцев', 2008, '2-е издание', 2, 9, 6, 'Подробный курс математического анализа.', '1.10.jpg');


CREATE TABLE book_analytics (
    book_id INT PRIMARY KEY,
    total_issues INT DEFAULT 0,
    avg_loan_days DECIMAL(5,2) DEFAULT 0,
    last_issue_date DATE,
    popularity_score DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE
);


CREATE TABLE genre_analytics (
    genre_id INT PRIMARY KEY,
    total_issues INT DEFAULT 0,
    avg_loan_days DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);


CREATE TABLE daily_stats (
    stat_date DATE PRIMARY KEY,
    total_issues INT DEFAULT 0,
    total_returns INT DEFAULT 0,
    active_loans INT DEFAULT 0,
    new_users INT DEFAULT 0
);
ALTER TABLE users ADD COLUMN is_confirmed BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN verification_code VARCHAR(6);
ALTER TABLE users ADD COLUMN code_expires_at DATETIME;