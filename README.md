main.py
from storage import load_books, add_book, delete_book, save_books
from stats import average_rating, stats_by_author


def show_menu():
    """Выводит главное меню."""
    print("\n" + "=" * 40)
    print("📚 ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
    print("=" * 40)
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Показать среднюю оценку")
    print("4. Статистика по авторам")
    print("5. Удалить книгу")
    print("6. Выход")
    print("=" * 40)


def add_book_interactive(books):
    """Интерактивное добавление книги."""
    print("\n📖 Добавление новой книги")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    
    while True:
        try:
            rating = int(input("Оценка (от 1 до 5): ").strip())
            if 1 <= rating <= 5:
                break
            else:
                print("⚠️ Оценка должна быть от 1 до 5!")
        except ValueError:
            print("⚠️ Введите целое число!")
    
    date_read = input("Дата прочтения (ГГГГ-ММ-ДД, Enter — сегодня): ").strip()
    if not date_read:
        date_read = None
    
    if add_book(books, author, title, rating, date_read):
        print(f"✅ Книга \"{title}\" успешно добавлена!")
    else:
        print("❌ Книга не добавлена (дубликат).")


def show_all_books(books):
    """Показывает все книги."""
    if not books:
        print("\n📭 Список книг пуст.")
        return
    
    print("\n📚 ВСЕ КНИГИ:")
    for i, book in enumerate(books, 1):
        print(f"{i}. {book}")


def show_average_rating(books):
    """Показывает среднюю оценку."""
    avg = average_rating(books)
    if avg == 0:
        print("\n📭 Нет книг для расчёта средней оценки.")
    else:
        print(f"\n⭐ Средняя оценка всех книг: {avg}")


def show_author_stats(books):
    """Показывает статистику по авторам."""
    stats = stats_by_author(books)
    if not stats:
        print("\n📭 Нет книг для статистики.")
        return
    
    print("\n📊 СТАТИСТИКА ПО АВТОРАМ:")
    for author, data in stats.items():
        print(f"  • {author}: {data['count']} книг, средняя оценка {data['avg_rating']}")


def delete_book_interactive(books):
    """Интерактивное удаление книги."""
    if not books:
        print("\n📭 Нет книг для удаления.")
        return
    
    print("\n🗑️ Удаление книги")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    
    if delete_book(books, author, title):
        print(f"✅ Книга \"{title}\" автора {author} удалена!")
    else:
        print(f"❌ Книга \"{title}\" автора {author} не найдена.")


def main():
    """Главная функция приложения."""
    books = load_books()
    
    while True:
        show_menu()
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            add_book_interactive(books)
        elif choice == "2":
            show_all_books(books)
        elif choice == "3":
            show_average_rating(books)
        elif choice == "4":
            show_author_stats(books)
        elif choice == "5":
            delete_book_interactive(books)
        elif choice == "6":
            print("\n👋 До свидания!")
            break
        else:
            print("⚠️ Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
