import random

# Генерация списка из 20 случайных целых чисел от 0 до 9
a = [random.randrange(11) for _ in range(5)]

# Проверка и добавление трех 4 после каждого 5
i = 0
while i < len(a):
    if a[i] == 5:  # Проверяем на 5
        a.insert(i + 1, 4)
        a.insert(i + 2, 4)
        a.insert(i + 3, 4)
        i += 3  # Пропускаем следующие три индекса
    i += 1

print(a)
