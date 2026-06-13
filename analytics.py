# Количество дней в месяце
MAX_DAYS = 31

def build_prefix_sums(expenses):
    """
    Строит массив префиксных сумм по дням.

    Префиксная сумма — это массив, где prefix[i] хранит сумму расходов
    за все дни с 1 по i. Это позволяет находить сумму за любой период
    за O(1) с помощью вычитания: sum(A, B) = prefix[B] - prefix[A-1].

    Параметры:
        expenses (list): список расходов (словари с ключами day, amount, category)

    Возвращает:
        list: массив префиксных сумм длиной MAX_DAYS + 1 (индекс 0 не используется)
    """
    # Создаём массив сумм по дням (индекс = день, значение = сумма за этот день)
    daily_sums = [0.0] * (MAX_DAYS + 1)

    for expense in expenses:
        day = expense["day"]
        daily_sums[day] += expense["amount"]

    # Строим массив префиксных сумм
    # prefix[i] = сумма расходов с 1-го по i-й день включительно
    prefix = [0.0] * (MAX_DAYS + 1)
    for i in range(1, MAX_DAYS + 1):
        prefix[i] = prefix[i - 1] + daily_sums[i]

    return prefix


def get_sum_for_period(prefix, day_a, day_b):
    """
    Вычисляет сумму расходов за период с дня A по день B включительно.
    Работает за O(1) благодаря префиксным суммам.

    Параметры:
        prefix (list): массив префиксных сумм (от build_prefix_sums)
        day_a (int): начальный день периода (1–31)
        day_b (int): конечный день периода (1–31)

    Возвращает:
        float: сумма расходов за период, или None если дни некорректны
    """
    # Проверяем корректность дней
    if not (1 <= day_a <= MAX_DAYS) or not (1 <= day_b <= MAX_DAYS):
        print(f"Ошибка: дни должны быть от 1 до {MAX_DAYS}.")
        return None

    if day_a > day_b:
        print("Ошибка: начальный день не может быть больше конечного.")
        return None

    # Формула для вычисления суммы за период: prefix[B] - prefix[A-1]
    return prefix[day_b] - prefix[day_a - 1]


def find_max_expense_day(expenses):
    """
    Находит день с максимальными суммарными расходами.
    Используется линейный поиск по всем дням.

    Параметры:
        expenses (list): список расходов

    Возвращает:
        tuple: (день, сумма) или (None, 0) если расходов нет
    """
    if not expenses:
        return None, 0

    # Считаем суммарные расходы по каждому дню
    daily_sums = [0.0] * (MAX_DAYS + 1)
    for expense in expenses:
        daily_sums[expense["day"]] += expense["amount"]

    # Линейный поиск дня с максимальной суммой
    max_day = None
    max_sum = 0.0

    for day in range(1, MAX_DAYS + 1):
        if daily_sums[day] > max_sum:
            max_sum = daily_sums[day]
            max_day = day

    return max_day, max_sum


def get_categories_sorted(expenses):
    """
    Собирает категории с суммами и сортирует их по убыванию суммы
    с помощью алгоритма сортировки вставками.

    Параметры:
        expenses (list): список расходов

    Возвращает:
        list: список кортежей (category, total) отсортированный по убыванию суммы
    """
    if not expenses:
        return []

    # Собираем суммы по категориям в словарь
    category_totals = {}
    for expense in expenses:
        cat = expense["category"]
        if cat in category_totals:
            category_totals[cat] += expense["amount"]
        else:
            category_totals[cat] = expense["amount"]

    # Преобразуем в список кортежей для сортировки
    pairs = list(category_totals.items())  # [(category, total), ...]

    # Сортировка вставками по убыванию суммы
    # Идём по массиву начиная со второго элемента
    for i in range(1, len(pairs)):
        current = pairs[i]
        j = i - 1

        # Сдвигаем элементы, которые меньше текущего, вправо
        while j >= 0 and pairs[j][1] < current[1]:
            pairs[j + 1] = pairs[j]
            j -= 1

        # Вставляем текущий элемент на нужное место
        pairs[j + 1] = current

    return pairs

