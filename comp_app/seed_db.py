from datetime import date
from app import create_app  # Импортируем твою функцию создания приложения
from db.Connection import db
from models.users import User
from models.genres import Genre
from models.book import Book

def seed_data():
    app = create_app()
    with app.app_context():
        # 1. Проверяем, есть ли уже данные, чтобы не дублировать
        if User.query.filter_by(email='admin@mail.com').first():
            print("База уже содержит тестовые данные.")
            return

        print("Начинаю заполнение базы данных...")

        # 2. Добавляем администратора
        admin = User(
            full_name="Иван Иванов (Админ)",
            email="admin@mail.com",
            user_role="admin",
            faculty="ИТ",
            phone="+79991234567",
            reg_date=date.today(),
            is_active=True
        )

        # 3. Добавляем тестового студента
        student = User(
            full_name="Петр Петров (Студент)",
            email="student@mail.com",
            user_role="student",
            faculty="Экономика",
            phone="+79997654321",
            reg_date=date.today(),
            is_active=True
        )

        # 4. Добавляем тестового преподавателя
        teacher = User(
            full_name="Сергей Сергеев (Преподаватель)",
            email="teacher@mail.com",
            user_role="teacher",
            faculty="Физика",
            phone="+79990000000",
            reg_date=date.today(),
            is_active=True
        )

        # Добавляем пользователей в сессию
        db.session.add_all([admin, student, teacher])

        # 5. Можно также добавить пару жанров и книг, если их нет
        # Проверим наличие жанра
        prog_genre = Genre.query.filter_by(genre_name='Программирование').first()
        if not prog_genre:
            prog_genre = Genre(genre_name='Программирование')
            db.session.add(prog_genre)
            db.session.flush() # Получаем ID жанра перед сохранением


        # Сохраняем всё в базу
        try:
            db.session.commit()
            print("Успех! Тестовые пользователи и данные добавлены.")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при заполнении: {e}")

if __name__ == '__main__':
    seed_data()