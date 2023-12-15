'''
В цьому модулі знаходяться функції допомагають та вирішують задачу комівояжера
'''
from copy import deepcopy

def read_file(file_path:str):
    '''
    Ця функція повинна читати .csv файл та повертати дані з якими можна працювати.
    В .csv файлі дані задані у форматі x1,x2,l1, де x1 - перше місто,
    x2 - друге місто, l1 - вага ребра між ними (довжина шляху між містами)
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode = 'w', delete=False) as tmpfile:
    ...     _ = tmpfile.write('a,b,12\\n\
a,c,10\\n\
a,g,12\\n\
b,d,12\\n\
b,c,8\\n\
b,a,12\\n\
c,b,8\\n\
c,a,10\\n\
c,g,9\\n\
c,e,3\\n\
c,d,11\\n\
g,a,12\\n\
g,c,9\\n\
g,e,7\\n\
g,f,9\\n\
e,g,7\\n\
e,c,3\\n\
e,d,11\\n\
e,f,6\\n\
d,e,11\\n\
d,b,12\\n\
d,c,11\\n\
d,f,10\\n\
f,e,6\\n\
f,d,10\\n\
f,g,9')
    >>> read_file(tmpfile.name)
    {'a': [('b', 12), ('c', 10), ('g', 12)], \
'b': [('d', 12), ('c', 8), ('a', 12)], 'c': [('b', 8), ('a', 10), \
('g', 9), ('e', 3), ('d', 11)], 'g': [('a', 12), ('c', 9), ('e', 7), ('f', 9)], \
'e': [('g', 7), ('c', 3), ('d', 11), ('f', 6)], 'd': [('e', 11), ('b', 12), \
('c', 11), ('f', 10)], 'f': [('e', 6), ('d', 10), ('g', 9)]}
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

memo = {} #Пам'ять про вже пройдені шляхи

def precise_alg(graph:dict, start:str | int, dest:str | int,
                go_through:list, flag:bool = True)->tuple:
    '''
    Ця функція вирішує задачу комівояжера точним алгоритмом (Held-Karp algorythm)
    Ця функція повертає кортеж значень з яких перше значення це довжина (вага) шляху,
    а друге сам шлях поданий списком
    >>> precise_alg({'a': [('b', 2), ('c', 15), ('d', 6)], \
'b': [('a', 2), ('c', 7), ('d', 3)], \
'c': [('a', 15), ('b', 7), ('d', 12)], \
'd': [('a', 6), ('b', 3), ('c', 12)]}, 'a', 'a', \
['b', 'c', 'd'])
    (27, ['a', 'd', 'c', 'b', 'a'])
    >>> precise_alg({'a': [('b', 10), ('c', 15), ('d', 20)], 'b': [('a', 10),\
('c', 35), ('d', 25)], 'c': [('a', 15), ('b', 35), ('d', 30)],\
'd': [('a', 20), ('b', 25), ('c', 30)]}, 'a', 'a', \
['b', 'c', 'd'])
    (80, ['a', 'c', 'd', 'b', 'a'])
    >>> precise_alg({'a': [('b', 12), ('c', 10), ('g', 12)], \
'b': [('d', 12), ('c', 8), ('a', 12)], 'c': [('b', 8), ('a', 10), \
('g', 9), ('e', 3), ('d', 11)], 'g': [('a', 12), ('c', 9), ('e', 7), ('f', 9)], \
'e': [('g', 7), ('c', 3), ('d', 11), ('f', 6)], 'd': [('e', 11), ('b', 12), \
('c', 11), ('f', 10)], 'f': [('e', 6), ('d', 10), ('g', 9)]}, 'a', 'a',\
['b', 'c', 'd', 'e', 'f', 'g'])
    (63, ['a', 'c', 'e', 'g', 'f', 'd', 'b', 'a'])
    '''
    # Підготовчі роботи
    ## Якщо функція запущена вперше то пам'ять про шляхи очищується
    if flag:
        memo.clear()
    ## Заміна неіснуючих ребер на ребра з довжиною inf
    for vertex in graph:
        pos_to_go = [x[0] for x in graph[vertex]]
        for vert in graph:
            if vert != vertex:
                if vert not in pos_to_go:
                    graph[vertex].append((vert, float('inf')))

    path = [] #Найвигідніший шлях поданий списком
    the_way = str((start, dest, go_through))
    # base case
    if len(go_through) < 1:
        try:
            path.append(start)
            path.append(dest)
            return memo[the_way]
        except KeyError:
            path.append(start)
            path.append(dest)
            for city in graph[start]:
                if city[0] == dest:
                    memo[the_way] = (city[1], path)
                    return (city[1], path)
    # general case
    elif len(go_through) >= 1:
        try:
            return memo[the_way]
        except KeyError:
            routes = []
            path = []
            for city in go_through:
                val1 = precise_alg(graph, city, dest, [])[0]
                subset_needed = [x for x in go_through if x != city]
                val2 = precise_alg(graph, start, city, subset_needed, False)[0]
                path.append(start)
                path.extend(precise_alg(graph, start, city, subset_needed, False)[1])
                path.append(city)
                path_copy = deepcopy(path)
                path.clear()
                for el in path_copy:
                    if path_copy.count(el) >= 1 and el not in path:
                        path.append(el)
                path.append(dest)
                routes.append((val1 + val2, path))
                path = []
            routes.sort(key=lambda x: x[0])
            return routes[0]

def greedy_alg():
    '''
    Ця функція вирішує задачу комівояжера "жадібним" приблизним алгоритмом 
    (Nearest neighbour algorithm)
    '''
    return

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
