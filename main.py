from storage import ExpenseStorage
from analytics import build_prefix_sums, get_sum_for_period, find_max_expense_day, get_categories_sorted
from tree import BudgetTree

def print_menu():
    """Выводит главное меню программы."""
    print("БЮДЖЕТНЫЙ ПОМОЩНИК")
    print("1. Добавить расход")
    print("2. Показать сумму за период")
    print("3. Показать день с максимальными расходами")
    print("4. Показать категории по сумме расходов")
    print("5. Отменить последнее действие")
    print("6. Показать дерево категорий")
    print("7. Выход")
    
def input_int(prompt):
    """
    Спрашивает у пользователя число, возвращает int или None, если введено не число
    """
    try:
        return int(input(prompt))
    except ValueError:
        print("Ошибка: введите целое число.")
        return None

def input_float(prompt):
    """
    Просит пользователя ввести число (можно с копейками)
    Если ввод не число - выводит ошибку и возвращает None
    """
    try:
        return float(input(prompt))
    except ValueError:
        print("Ошибка: введите число (например, 150 или 99.90).")
        return None

def handle_add_expense(storage, tree):
    """
    Добавляет новый расход
    Спрашивает у пользователя день, сумму и категорию
    """
    print("\n Добавление расхода")

    day = input_int("Введите день (1–31): ")
    if day is None:
        return

    amount = input_float("Введите сумму: ")
    if amount is None:
        return

    category = input("Введите категорию (например: еда, транспорт): ").strip()

    # Добавляем в хранилище
    success = storage.add_expense(day, amount, category)

    if success:
        # Добавляем категорию и сумму в дерево
        tree.insert(category, amount)
        print(f"Расход добавлен: {day}-й день, {amount:.2f} руб., категория «{category}».")

def handle_sum_for_period(storage):
    """
    Обрабатывает запрос суммы расходов за период
    """
    print("\n--- Сумма за период ---")

    if storage.is_empty():
        print("Расходов пока нет.")
        return

    day_a = input_int("Введите начальный день периода: ")
    if day_a is None:
        return

    day_b = input_int("Введите конечный день периода: ")
    if day_b is None:
        return

    # Строим префиксные суммы и считаем результат
    prefix = build_prefix_sums(storage.get_all_expenses())
    result = get_sum_for_period(prefix, day_a, day_b)

    if result is not None:
        print(f"Сумма расходов с {day_a}-го по {day_b}-й день: {result:.2f} руб.")


def handle_max_day(storage):
    """
    Находит и выводит день с максимальными расходами
    """
    print("\n--- День с максимальными расходами ---")

    if storage.is_empty():
        print("Расходов пока нет.")
        return

    day, total = find_max_expense_day(storage.get_all_expenses())

    if day is not None:
        print(f"День с максимальными расходами: {day}-й день, сумма: {total:.2f} руб.")
    else:
        print("Не удалось определить день.")


def handle_show_categories(storage):
    """
    Обрабатывает вывод категорий, отсортированных по сумме расходов
    """
    print("\n Категории по сумме расходов (по убыванию)")

    if storage.is_empty():
        print("Расходов пока нет")
        return

    sorted_categories = get_categories_sorted(storage.get_all_expenses())

    if not sorted_categories:
        print("Категорий нет")
        return

    print(f"{'Категория':<20} {'Сумма (руб.)':>15}")
    print("-" * 37)
    for category, total in sorted_categories:
        print(f"{category:<20} {total:>15.2f}")


def handle_undo(storage, tree):
    """
    Обрабатывает отмену последнего добавленного расхода
    """
    print("\n--- Отмена последнего действия ---")

    removed = storage.undo_last()

    if removed is not None:
        # Уменьшаем сумму в дереве категорий
        tree.subtract(removed["category"], removed["amount"])
        print(f"Отменён расход: {removed['day']}-й день, "
            f"{removed['amount']:.2f} руб., категория «{removed['category']}».")


def handle_show_tree(tree):
    """
    Обрабатывает вывод дерева категорий (inorder-обход)
    """
    print("\n--- Дерево категорий (алфавитный порядок) ---")

    if tree.is_empty():
        print("Категорий пока нет.")
        return

    categories = tree.inorder_traversal()

    print(f"{'Категория':<20} {'Сумма (руб.)':>15}")
    print("-" * 37)
    for category, total in categories:
        # Пропускаем категории с нулевой суммой (были полностью отменены)
        if total > 0:
            print(f"{category:<20} {total:>15.2f}")


def main():
    """
    Главная функция программы
    Создаёт хранилище и дерево, запускает главное меню
    """
    print("Добро пожаловать в Бюджетный помощник!")
    print("Программа поможет вам отслеживать расходы за месяц")

    # Создаём хранилище расходов и дерево категорий
    storage = ExpenseStorage()
    tree = BudgetTree()

    # Основной цикл программы
    while True:
        print_menu()

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            handle_add_expense(storage, tree)

        elif choice == "2":
            handle_sum_for_period(storage)

        elif choice == "3":
            handle_max_day(storage)

        elif choice == "4":
            handle_show_categories(storage)

        elif choice == "5":
            handle_undo(storage, tree)

        elif choice == "6":
            handle_show_tree(tree)

        elif choice == "7":
            print("\nДо свидания! Удачи с бюджетом!")
            break

        else:
            print("Неверный выбор. Введите число от 1 до 7.")


# Запускаем программу
if __name__ == "__main__":
    main()

