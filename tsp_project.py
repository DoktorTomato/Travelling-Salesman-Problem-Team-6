'''
В цьому модулі знаходяться функції допомагають та вирішують задачу комівояжера
'''

def read_file(file_path:str):
    '''
    Ця функція повинна читати .csv файл та повертати дані з якими можна працювати.
    В .csv файлі дані задані у форматі x1,x2,l1, де x1 - перше місто,
    x2 - друге місто, l1 - вага ребра між ними (довжина шляху між містами)
    '''
    with open (file_path, 'r', encoding= 'utf-8') as file:
        content = file.read().splitlines()
    content = [i.split(',') for i in content]

    new_dict = {}
    for i in content:
        if not i[0] in new_dict:
            new_dict[i[0]] = [tuple((i[1],i[2]))]
        else:
            new_dict[i[0]].append(tuple((i[1],i[2])))

    for key, value in new_dict.items():
        new_dict[key] = [(i[0], int(i[1])) for i in value]
    return new_dict

def precise_alg():
    '''
    Ця функція вирішує задачу комівояжера точним алгоритмом (Held-Karp algorythm)
    '''
    return

def greedy_alg(graph: dict, start_point: str):
    '''
    Ця функція вирішує задачу комівояжера "жадібним" приблизним алгоритмом 
    (Nearest neighbour algorithm)
    '''
    path = [] # список, у який будуть додаватися відвідані точки
    current_point = start_point # позначаємо її як поточну
    path.append(current_point) # додаємо до списку, як відвідану

    # поки всі точки не будуть відвідані продорвжуємо ітерацію
    while len(path) < len(graph):
        min_distance = float('inf') # ініціалізуємо мінімальну відстать між точками як нескінченність
        next_point = None # ініціалізуємо наступну точку як None
        for neighbor, distance in graph.get(current_point, []): # ітерація через сусідів поточної точки та їх відстані від неї
            if neighbor not in path and distance < min_distance: # перевірка, чи сусід не є відвіданий і його відстань менша за поточну мінімальну відстань.
                min_distance = distance # оновлення мінімальної відстанні
                next_point = neighbor # оновлення наступної точки для поточного сусіда

        if next_point is None: # перевірка чи є сусід, якого ще не відвідали
            break

        path.append(next_point) # додаємо знайденого сусіда до списку відвіданих точок
        current_point = next_point # оновлюємо поточну точки

    path.append(start_point) # додаємо початкову точку до списку відвіданих, щрб завершити цикл
    return path

if __name__ == '__main__':
    import doctest
    print(doctest.testmod)
    #тут може бути запуск функцій вручну
