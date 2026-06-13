# Максимальное количество дней в месяце
MAX_DAYS = 31

class ExpenseStorage:
    """
    Класс для хранения расходов пользователя за месяц.

    Хранит список расходов и стек для отмены последнего действия.
    Каждый расход — это словарь с ключами: day, amount, category.
    """

    def __init__(self):
        """Инициализация хранилища: пустой список расходов и пустой стек."""
        # Список всех расходов (каждый элемент — словарь)
        self.expenses = []

        # Стек для отмены последнего добавленного расхода
        # Каждый элемент стека — это копия добавленного расхода
        self.undo_stack = []

    def add_expense(self, day, amount, category):
        """
        Добавляет новый расход в хранилище.

        Параметры:
            day (int): день месяца от 1 до 31
            amount (float): сумма расхода (положительная)
            category (str): название категории

        Возвращает:
            True если расход добавлен успешно, False если данные некорректны.
        """
        # Проверяем корректность дня
        if not (1 <= day <= MAX_DAYS):
            print(f"Ошибка: день должен быть от 1 до {MAX_DAYS}.")
            return False

        # Проверяем что сумма положительная
        if amount <= 0:
            print("Ошибка: сумма должна быть больше нуля.")
            return False

        # Проверяем что категория не пустая
        if not category.strip():
            print("Ошибка: категория не может быть пустой.")
            return False

        # Создаём запись о расходе
        expense = {
            "day": day,
            "amount": amount,
            "category": category.strip()
        }

        # Добавляем в основной список
        self.expenses.append(expense)

        # Кладём в стек для возможности отмены
        self.undo_stack.append(expense)

        return True

    def undo_last(self):
        """
        Отменяет последнее добавленное действие (использует стек).

        Возвращает:
            Удалённый расход (словарь) или None если стек пуст.
        """
        # Проверяем, есть ли что отменять
        if not self.undo_stack:
            print("Нечего отменять: стек пуст.")
            return None

        # Извлекаем последний расход из стека
        last_expense = self.undo_stack.pop()

        # Удаляем этот расход из основного списка
        # Ищем с конца, чтобы удалить именно последний совпадающий элемент
        for i in range(len(self.expenses) - 1, -1, -1):
            if self.expenses[i] == last_expense:
                self.expenses.pop(i)
                break

        return last_expense

    def get_all_expenses(self):
        """
        Возвращает все расходы в виде списка.

        Возвращает:
            list: список словарей с расходами
        """
        return self.expenses

    def get_expenses_by_day(self, day):
        """
        Возвращает все расходы за конкретный день.

        Параметры:
            day (int): номер дня

        Возвращает:
            list: список расходов за указанный день
        """
        return [e for e in self.expenses if e["day"] == day]

    def is_empty(self):
        """
        Проверяет, есть ли вообще какие-то расходы.

        Возвращает:
            bool: True если расходов нет
        """
        return len(self.expenses) == 0

