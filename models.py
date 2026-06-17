class Book:
    """Класс для представления книги"""
    
    def __init__(self, title, author, year, pages, genre):
        """
        Конструктор класса Book
        
        Аргументы:
            title (str): Название книги
            author (str): Автор книги
            year (int): Год издания
            pages (int): Количество страниц
            genre (str): Жанр книги
        """
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.genre = genre
        self.is_available = True  # По умолчанию книга доступна
    
    def __str__(self):
        """Строковое представление книги для пользователя"""
        return f"'{self.title}' - {self.author} ({self.year})"
    
    def __repr__(self):
        """Строковое представление для разработчиков"""
        return f"Book('{self.title}', '{self.author}', {self.year}, {self.pages}, '{self.genre}')"
    
    def borrow(self):
        """Взять книгу (если она доступна)"""
        if self.is_available:
            self.is_available = False
            return f"Книга '{self.title}' выдана"
        else:
            return f"Книга '{self.title}' уже занята"
    
    def return_book(self):
        """Вернуть книгу"""
        self.is_available = True
        return f"Книга '{self.title}' возвращена"
    
    def get_info(self):
        """Получить полную информацию о книге"""
        status = "доступна" if self.is_available else "занята"
        return f"""
Название: {self.title}
Автор: {self.author}
Год: {self.year}
Страниц: {self.pages}
Жанр: {self.genre}
Статус: {status}
"""
    
    def is_long(self, threshold=300):
        """Проверить, является ли книга длинной (больше threshold страниц)"""
        return self.pages > threshold
    
    def __eq__(self, other):
        """Сравнение книг по названию и автору"""
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author
