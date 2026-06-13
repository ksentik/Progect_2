class BSTNode:
    """
    Узел бинарного дерева поиска.

    Атрибуты:
        category (str): название категории
        total (float): общая сумма расходов по этой категории
        left: левый дочерний узел
        right: правый дочерний узел
    """

    def __init__(self, category, amount):
        """
        Создаёт новый узел дерева.

        Параметры:
            category (str): название категории
            amount (float): начальная сумма
        """
        self.category = category
        self.total = amount
        self.left = None
        self.right = None


class BudgetTree:
    """
    Бинарное дерево поиска для хранения категорий расходов.

    Категории хранятся в алфавитном порядке (по ключу — название категории).
    Каждый узел содержит название категории и общую сумму расходов по ней.
    """

    def __init__(self):
        """Инициализация пустого дерева."""
        self.root = None

    def insert(self, category, amount):
        """
        Добавляет новый расход в дерево.
        Если категория уже существует — прибавляет сумму к существующей.

        Параметры:
            category (str): название категории
            amount (float): сумма расхода
        """
        if self.root is None:
            # Дерево пустое — создаём корень
            self.root = BSTNode(category, amount)
        else:
            # Иначе вставляем рекурсивно
            self._insert_recursive(self.root, category, amount)

    def _insert_recursive(self, node, category, amount):
        """
        Вспомогательная рекурсивная функция для вставки.

        Параметры:
            node: текущий узел
            category (str): название категории
            amount (float): сумма расхода
        """
        if category == node.category:
            # Категория уже есть — просто добавляем сумму
            node.total += amount

        elif category < node.category:
            # Идём в левое поддерево
            if node.left is None:
                node.left = BSTNode(category, amount)
            else:
                self._insert_recursive(node.left, category, amount)

        else:
            # Идём в правое поддерево
            if node.right is None:
                node.right = BSTNode(category, amount)
            else:
                self._insert_recursive(node.right, category, amount)

    def find(self, category):
        """
        Ищет категорию в дереве.

        Параметры:
            category (str): название категории для поиска

        Возвращает:
            BSTNode или None если категория не найдена
        """
        return self._find_recursive(self.root, category)

    def _find_recursive(self, node, category):
        """
        Вспомогательная рекурсивная функция для поиска.

        Параметры:
            node: текущий узел
            category (str): искомая категория

        Возвращает:
            BSTNode или None
        """
        if node is None:
            return None

        if category == node.category:
            return node
        elif category < node.category:
            return self._find_recursive(node.left, category)
        else:
            return self._find_recursive(node.right, category)

    def inorder_traversal(self):
        """
        Обходит дерево в порядке inorder (левый — корень — правый).
        Это даёт категории в алфавитном порядке.

        Возвращает:
            list: список кортежей (category, total) в алфавитном порядке
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """
        Вспомогательная рекурсивная функция для inorder-обхода.

        Параметры:
            node: текущий узел
            result (list): список для накопления результатов
        """
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.category, node.total))
            self._inorder_recursive(node.right, result)

    def subtract(self, category, amount):
        """
        Уменьшает сумму по категории (используется при отмене действия).
        Если сумма становится 0 или меньше — узел помечается как пустой (total=0).

        Параметры:
            category (str): название категории
            amount (float): сумма для вычитания
        """
        node = self.find(category)
        if node is not None:
            node.total -= amount
            # Если сумма стала нулевой или отрицательной — обнуляем
            if node.total < 0:
                node.total = 0

    def is_empty(self):
        """
        Проверяет, пустое ли дерево.

        Возвращает:
            bool: True если дерево пустое
        """
        return self.root is None

