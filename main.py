"""
Библиотечная система
Главный файл для запуска приложения
"""

from book import Book
from library import Library
import sys
import os


def clear_screen():
    """Очистка экрана (для Windows и Unix-систем)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Печать красивого заголовка"""
    print("=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)


def print_menu():
    """Отображение главного меню"""
    clear_screen()
    print_header("📚 БИБЛИОТЕЧНАЯ СИСТЕМА")
    print("\n" + "=" * 60)
    print("1.  Добавить книгу")
    print("2.  Показать все книги")
    print("3.  Найти книгу по названию")
    print("4.  Найти книги по автору")
    print("5.  Найти книги по жанру")
    print("6.  Взять книгу (выдать читателю)")
    print("7.  Вернуть книгу")
    print("8.  Показать доступные книги")
    print("9.  Удалить книгу")
    print("10. Статистика библиотеки")
    print("0.  Выход")
    print("=" * 60)


def add_book_menu(library):
    """Меню добавления книги"""
    print_header("📖 ДОБАВЛЕНИЕ НОВОЙ КНИГИ")
    
    title = input("Введите название книги: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    author = input("Введите автора: ").strip()
    if not author:
        print("❌ Автор не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    try:
        year = int(input("Введите год издания: "))
        pages = int(input("Введите количество страниц: "))
    except ValueError:
        print("❌ Год и страницы должны быть числами!")
        input("Нажмите Enter для продолжения...")
        return
    
    genre = input("Введите жанр: ").strip()
    if not genre:
        genre = "Не указан"
    
    book = Book(title, author, year, pages, genre)
    result = library.add_book(book)
    print(f"\n✅ {result}")
    input("\nНажмите Enter для продолжения...")


def show_all_books(library):
    """Показать все книги"""
    print_header("📚 ВСЕ КНИГИ В БИБЛИОТЕКЕ")
    
    if not library.books:
        print("\n📭 В библиотеке пока нет книг.")
    else:
        print(f"\nВсего книг: {len(library.books)}\n")
        print("-" * 60)
        for i, book in enumerate(library.books, 1):
            status = "✅ Доступна" if book.is_available else "❌ Занята"
            print(f"{i}. {book}")
            print(f"   Жанр: {book.genre} | Страниц: {book.pages} | Статус: {status}")
            print("-" * 60)
    
    input("\nНажмите Enter для продолжения...")


def find_book_by_title(library):
    """Поиск книги по названию"""
    print_header("🔍 ПОИСК КНИГИ ПО НАЗВАНИЮ")
    
    title = input("Введите название книги: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    found = False
    print("\nРезультаты поиска:\n")
    print("-" * 60)
    
    for book in library.books:
        if title.lower() in book.title.lower():
            print(book.get_info())
            print("-" * 60)
            found = True
    
    if not found:
        print(f"❌ Книга '{title}' не найдена.")
    
    input("\nНажмите Enter для продолжения...")


def find_books_by_author(library):
    """Поиск книг по автору"""
    print_header("🔍 ПОИСК КНИГ ПО АВТОРУ")
    
    author = input("Введите имя автора: ").strip()
    if not author:
        print("❌ Имя автора не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    found_books = library.find_by_author(author)
    
    print(f"\nРезультаты поиска (автор: {author}):\n")
    print("-" * 60)
    
    if found_books:
        for book in found_books:
            status = "✅ Доступна" if book.is_available else "❌ Занята"
            print(f"📖 {book}")
            print(f"   Жанр: {book.genre} | Страниц: {book.pages} | Статус: {status}")
            print("-" * 60)
    else:
        print(f"❌ Книги автора '{author}' не найдены.")
    
    input("\nНажмите Enter для продолжения...")


def find_books_by_genre(library):
    """Поиск книг по жанру"""
    print_header("🔍 ПОИСК КНИГ ПО ЖАНРУ")
    
    genre = input("Введите жанр: ").strip()
    if not genre:
        print("❌ Жанр не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    found_books = library.find_by_genre(genre)
    
    print(f"\nРезультаты поиска (жанр: {genre}):\n")
    print("-" * 60)
    
    if found_books:
        for book in found_books:
            status = "✅ Доступна" if book.is_available else "❌ Занята"
            print(f"📖 {book}")
            print(f"   Автор: {book.author} | Страниц: {book.pages} | Статус: {status}")
            print("-" * 60)
    else:
        print(f"❌ Книги жанра '{genre}' не найдены.")
    
    input("\nНажмите Enter для продолжения...")


def borrow_book(library):
    """Взять книгу"""
    print_header("📤 ВЗЯТЬ КНИГУ")
    
    title = input("Введите название книги, которую хотите взять: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    for book in library.books:
        if book.title.lower() == title.lower():
            result = book.borrow()
            print(f"\n{result}")
            input("\nНажмите Enter для продолжения...")
            return
    
    print(f"\n❌ Книга '{title}' не найдена.")
    input("\nНажмите Enter для продолжения...")


def return_book(library):
    """Вернуть книгу"""
    print_header("📥 ВЕРНУТЬ КНИГУ")
    
    title = input("Введите название книги, которую возвращаете: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    for book in library.books:
        if book.title.lower() == title.lower():
            result = book.return_book()
            print(f"\n{result}")
            input("\nНажмите Enter для продолжения...")
            return
    
    print(f"\n❌ Книга '{title}' не найдена.")
    input("\nНажмите Enter для продолжения...")


def show_available_books(library):
    """Показать доступные книги"""
    print_header("✅ ДОСТУПНЫЕ КНИГИ")
    
    available = library.list_available()
    
    if not available:
        print("\n📭 В данный момент все книги заняты.")
    else:
        print(f"\nДоступно книг: {len(available)}\n")
        print("-" * 60)
        for i, book in enumerate(available, 1):
            print(f"{i}. {book}")
            print(f"   Автор: {book.author} | Жанр: {book.genre} | Страниц: {book.pages}")
            print("-" * 60)
    
    input("\nНажмите Enter для продолжения...")


def delete_book(library):
    """Удалить книгу"""
    print_header("🗑️ УДАЛЕНИЕ КНИГИ")
    
    title = input("Введите название книги для удаления: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return
    
    result = library.remove_book(title)
    print(f"\n{result}")
    input("\nНажмите Enter для продолжения...")


def show_statistics(library):
    """Показать статистику библиотеки"""
    print_header("📊 СТАТИСТИКА БИБЛИОТЕКИ")
    
    total = len(library.books)
    available = len(library.list_available())
    borrowed = total - available
    
    print(f"\n📚 Всего книг: {total}")
    print(f"✅ Доступно: {available}")
    print(f"❌ Занято: {borrowed}")
    
    if total > 0:
        # Статистика по жанрам
        genres = {}
        for book in library.books:
            genres[book.genre] = genres.get(book.genre, 0) + 1
        
        print("\n📊 Книги по жанрам:")
        for genre, count in sorted(genres.items()):
            print(f"   {genre}: {count} шт.")
        
        # Самая длинная книга
        longest = max(library.books, key=lambda b: b.pages)
        print(f"\n📖 Самая длинная книга: {longest} ({longest.pages} стр.)")
        
        # Самая короткая книга
        shortest = min(library.books, key=lambda b: b.pages)
        print(f"📖 Самая короткая книга: {shortest} ({shortest.pages} стр.)")
    
    input("\nНажмите Enter для продолжения...")


def main():
    """Главная функция - точка входа"""
    
    # Создаем библиотеку с начальными книгами для демонстрации
    library = Library("Центральная городская библиотека")
    
    # Добавляем несколько книг для примера
    initial_books = [
        Book("Война и мир", "Лев Толстой", 1869, 1300, "роман-эпопея"),
        Book("Преступление и наказание", "Фёдор Достоевский", 1866, 650, "роман"),
        Book("Мастер и Маргарита", "Михаил Булгаков", 1967, 450, "роман"),
        Book("Три мушкетёра", "Александр Дюма", 1844, 700, "приключения"),
        Book("Маленький принц", "Антуан де Сент-Экзюпери", 1943, 96, "сказка"),
    ]
    
    for book in initial_books:
        library.add_book(book)
    
    # Главный цикл программы
    while True:
        print_menu()
        
        try:
            choice = input("\nВыберите пункт меню (0-10): ").strip()
            
            if choice == '0':
                print_header("👋 ДО СВИДАНИЯ!")
                print("\nСпасибо за использование библиотечной системы!")
                sys.exit(0)
            
            elif choice == '1':
                add_book_menu(library)
            
            elif choice == '2':
                show_all_books(library)
            
            elif choice == '3':
                find_book_by_title(library)
            
            elif choice == '4':
                find_books_by_author(library)
            
            elif choice == '5':
                find_books_by_genre(library)
            
            elif choice == '6':
                borrow_book(library)
            
            elif choice == '7':
                return_book(library)
            
            elif choice == '8':
                show_available_books(library)
            
            elif choice == '9':
                delete_book(library)
            
            elif choice == '10':
                show_statistics(library)
            
            else:
                print("\n❌ Неверный выбор! Пожалуйста, введите число от 0 до 10.")
                input("Нажмите Enter для продолжения...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Программа завершена пользователем.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")
            input("Нажмите Enter для продолжения...")


# Точка входа в программу
if __name__ == "__main__":
    main()
