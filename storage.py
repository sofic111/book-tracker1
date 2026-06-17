"""
Модуль для хранения данных библиотеки
Поддерживает JSON, Pickle и CSV форматы
"""

import json
import pickle
import csv
import os
from datetime import datetime
from book import Book


class Storage:
    """Базовый класс для хранения данных"""
    
    def __init__(self, filename="library_data"):
        self.filename = filename
        self.extension = ""
    
    def save(self, books):
        """Сохранить список книг"""
        raise NotImplementedError("Метод должен быть переопределен")
    
    def load(self):
        """Загрузить список книг"""
        raise NotImplementedError("Метод должен быть переопределен")


class JSONStorage(Storage):
    """Хранение данных в JSON формате"""
    
    def __init__(self, filename="library_data.json"):
        super().__init__(filename)
        self.extension = ".json"
        if not self.filename.endswith('.json'):
            self.filename += '.json'
    
    def _book_to_dict(self, book):
        """Преобразовать книгу в словарь для JSON"""
        return {
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'pages': book.pages,
            'genre': book.genre,
            'is_available': book.is_available
        }
    
    def _dict_to_book(self, data):
        """Преобразовать словарь в объект Book"""
        book = Book(
            data['title'],
            data['author'],
            data['year'],
            data['pages'],
            data['genre']
        )
        book.is_available = data.get('is_available', True)
        return book
    
    def save(self, books):
        """Сохранить книги в JSON файл"""
        try:
            data = [self._book_to_dict(book) for book in books]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return f"✅ Данные сохранены в {self.filename}"
        except Exception as e:
            return f"❌ Ошибка сохранения: {e}"
    
    def load(self):
        """Загрузить книги из JSON файла"""
        try:
            if not os.path.exists(self.filename):
                return [], f"⚠️ Файл {self.filename} не найден"
            
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            books = [self._dict_to_book(item) for item in data]
            return books, f"✅ Загружено {len(books)} книг из {self.filename}"
        except json.JSONDecodeError:
            return [], f"❌ Ошибка: файл {self.filename} поврежден"
        except Exception as e:
            return [], f"❌ Ошибка загрузки: {e}"


class PickleStorage(Storage):
    """Хранение данных в Pickle формате (бинарный)"""
    
    def __init__(self, filename="library_data.pkl"):
        super().__init__(filename)
        self.extension = ".pkl"
        if not self.filename.endswith('.pkl'):
            self.filename += '.pkl'
    
    def save(self, books):
        """Сохранить книги в Pickle файл"""
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(books, f)
            return f"✅ Данные сохранены в {self.filename}"
        except Exception as e:
            return f"❌ Ошибка сохранения: {e}"
    
    def load(self):
        """Загрузить книги из Pickle файла"""
        try:
            if not os.path.exists(self.filename):
                return [], f"⚠️ Файл {self.filename} не найден"
            
            with open(self.filename, 'rb') as f:
                books = pickle.load(f)
            return books, f"✅ Загружено {len(books)} книг из {self.filename}"
        except Exception as e:
            return [], f"❌ Ошибка загрузки: {e}"


class CSVStorage(Storage):
    """Хранение данных в CSV формате"""
    
    def __init__(self, filename="library_data.csv"):
        super().__init__(filename)
        self.extension = ".csv"
        if not self.filename.endswith('.csv'):
            self.filename += '.csv'
    
    def save(self, books):
        """Сохранить книги в CSV файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # Заголовки
                writer.writerow(['title', 'author', 'year', 'pages', 'genre', 'is_available'])
                # Данные
                for book in books:
                    writer.writerow([
                        book.title,
                        book.author,
                        book.year,
                        book.pages,
                        book.genre,
                        book.is_available
                    ])
            return f"✅ Данные сохранены в {self.filename}"
        except Exception as e:
            return f"❌ Ошибка сохранения: {e}"
    
    def load(self):
        """Загрузить книги из CSV файла"""
        try:
            if not os.path.exists(self.filename):
                return [], f"⚠️ Файл {self.filename} не найден"
            
            books = []
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(
                        row['title'],
                        row['author'],
                        int(row['year']),
                        int(row['pages']),
                        row['genre']
                    )
                    book.is_available = row['is_available'] == 'True'
                    books.append(book)
            return books, f"✅ Загружено {len(books)} книг из {self.filename}"
        except Exception as e:
            return [], f"❌ Ошибка загрузки: {e}"


class StorageManager:
    """Менеджер для управления разными типами хранения"""
    
    def __init__(self, storage_type='json', filename=None):
        """
        Инициализация менеджера хранения
        
        Аргументы:
            storage_type (str): Тип хранилища ('json', 'pickle', 'csv')
            filename (str): Имя файла (опционально)
        """
        self.storage_type = storage_type
        self.filename = filename
        
        if filename is None:
            filename = f"library_data.{storage_type}"
            if storage_type == 'json':
                filename = "library_data.json"
            elif storage_type == 'pickle':
                filename = "library_data.pkl"
            elif storage_type == 'csv':
                filename = "library_data.csv"
        
        # Создаем соответствующее хранилище
        if storage_type == 'json':
            self.storage = JSONStorage(filename)
        elif storage_type == 'pickle':
            self.storage = PickleStorage(filename)
        elif storage_type == 'csv':
            self.storage = CSVStorage(filename)
        else:
            raise ValueError(f"Неизвестный тип хранения: {storage_type}")
    
    def save(self, books):
        """Сохранить данные"""
        return self.storage.save(books)
    
    def load(self):
        """Загрузить данные"""
        return self.storage.load()
    
    def backup(self, books, backup_dir="backups"):
        """Создать резервную копию"""
        try:
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{backup_dir}/backup_{timestamp}.{self.storage_type}"
            
            # Создаем временное хранилище для бэкапа
            if self.storage_type == 'json':
                backup_storage = JSONStorage(backup_filename)
            elif self.storage_type == 'pickle':
                backup_storage = PickleStorage(backup_filename)
            elif self.storage_type == 'csv':
                backup_storage = CSVStorage(backup_filename)
            
            return backup_storage.save(books)
        except Exception as e:
            return f"❌ Ошибка создания резервной копии: {e}"
    
    def get_info(self):
        """Получить информацию о хранилище"""
        exists = os.path.exists(self.storage.filename)
        size = 0
        if exists:
            size = os.path.getsize(self.storage.filename)
        
        return {
            'type': self.storage_type,
            'filename': self.storage.filename,
            'exists': exists,
            'size_bytes': size,
            'size_kb': round(size / 1024, 2)
        }
