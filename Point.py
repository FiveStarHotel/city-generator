class Point:

    def __init__(self, i:int, j:int):
        self.i = i # Строка (Y)
        self.j = j # Столбец (X)

    def __str__(self):
        """
        Возвращает строковое представление точки в формате:
        (x,y)
        """

        return f"({self.j},{self.i})"

    def get_tuple(self) -> tuple:
        """
        Возвращает точку в виде кортежа, который имеет следующую структуру:
        (x,y)
        """

        return self.j, self.i