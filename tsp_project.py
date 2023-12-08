'''
В цьому модулі знаходяться функції допомагають та вирішують задачу комівояжера
'''
import itertools as it

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

def all_subsets(gen_set:set)->list:
    '''
    Ця функція знаходить всі можливі підмножини даної множини (задана списком)
    і повертає їх список
    >>> all_subsets(['b', 'c', 'd', 'e', 'f', 'g'])
    [('b',), ('c',), ('d',), ('e',), ('f',), ('g',), \
('b', 'c'), ('b', 'd'), ('b', 'e'), ('b', 'f'), ('b', 'g'), \
('c', 'd'), ('c', 'e'), ('c', 'f'), ('c', 'g'), ('d', 'e'), \
('d', 'f'), ('d', 'g'), ('e', 'f'), ('e', 'g'), ('f', 'g'), \
('b', 'c', 'd'), ('b', 'c', 'e'), ('b', 'c', 'f'), ('b', 'c', 'g'), \
('b', 'd', 'e'), ('b', 'd', 'f'), ('b', 'd', 'g'), ('b', 'e', 'f'), \
('b', 'e', 'g'), ('b', 'f', 'g'), ('c', 'd', 'e'), ('c', 'd', 'f'), \
('c', 'd', 'g'), ('c', 'e', 'f'), ('c', 'e', 'g'), ('c', 'f', 'g'), \
('d', 'e', 'f'), ('d', 'e', 'g'), ('d', 'f', 'g'), ('e', 'f', 'g'), \
('b', 'c', 'd', 'e'), ('b', 'c', 'd', 'f'), ('b', 'c', 'd', 'g'), \
('b', 'c', 'e', 'f'), ('b', 'c', 'e', 'g'), ('b', 'c', 'f', 'g'), \
('b', 'd', 'e', 'f'), ('b', 'd', 'e', 'g'), ('b', 'd', 'f', 'g'), \
('b', 'e', 'f', 'g'), ('c', 'd', 'e', 'f'), ('c', 'd', 'e', 'g'), \
('c', 'd', 'f', 'g'), ('c', 'e', 'f', 'g'), ('d', 'e', 'f', 'g'), \
('b', 'c', 'd', 'e', 'f'), ('b', 'c', 'd', 'e', 'g'), \
('b', 'c', 'd', 'f', 'g'), ('b', 'c', 'e', 'f', 'g'), \
('b', 'd', 'e', 'f', 'g'), ('c', 'd', 'e', 'f', 'g')]
    '''
    res_lst = []
    for i in range(1, len(gen_set)):
        res_lst.extend(list(it.combinations(gen_set, i)))
    return res_lst

def ispath(graph:dict, start:str | int, destination:str | int)->bool:
    '''
    Ця функція приймає на вхід словник з даними про шляхи який можна створити
    за допомогою функції read_csv, початкову точку та ціль.
    На вихід ця функція повертає True чи False взалежності від того чи існує такий
    шлях між даними точками
    >>> ispath({'a': [('b', 12), ('c', 10), ('g', 12)], \
'b': [('d', 12), ('c', 8), ('a', 12)], 'c': [('b', 8), ('a', 10), \
('g', 9), ('e', 3), ('d', 11)], 'g': [('a', 12), ('c', 9), ('e', 7), ('f', 9)], \
'e': [('g', 7), ('c', 3), ('d', 11), ('f', 6)], 'd': [('e', 11), ('b', 12), \
('c', 11), ('f', 10)], 'f': [('e', 6), ('d', 10), ('g', 9)]}, 'a', 'c')
    True
    >>> ispath({'a': [('b', 12), ('c', 10), ('g', 12)], \
'b': [('d', 12), ('c', 8), ('a', 12)], 'c': [('b', 8), ('a', 10), \
('g', 9), ('e', 3), ('d', 11)], 'g': [('a', 12), ('c', 9), ('e', 7), ('f', 9)], \
'e': [('g', 7), ('c', 3), ('d', 11), ('f', 6)], 'd': [('e', 11), ('b', 12), \
('c', 11), ('f', 10)], 'f': [('e', 6), ('d', 10), ('g', 9)]}, 'a', 'f')
    False
    '''
    for route in graph[start]:
        if route[0] == destination:
            return True
    return False

def precise_alg(graph:dict, start:str | int, dest:str | int, go_through:list, memo:dict)->list:
    '''
    Ця функція вирішує задачу комівояжера точним алгоритмом (Held-Karp algorythm)
    Ця функція повертає значення що дорівнює найкоротшому шляху
    >>> precise_alg({'a': [('b', 12), ('c', 10), ('g', 12)], \
'b': [('d', 12), ('c', 8), ('a', 12)], 'c': [('b', 8), ('a', 10), \
('g', 9), ('e', 3), ('d', 11)], 'g': [('a', 12), ('c', 9), ('e', 7), ('f', 9)], \
'e': [('g', 7), ('c', 3), ('d', 11), ('f', 6)], 'd': [('e', 11), ('b', 12), \
('c', 11), ('f', 10)], 'f': [('e', 6), ('d', 10), ('g', 9)]}, 'a', 'a', \
['b', 'c', 'd', 'e', 'f', 'g'], {})
    '''
    try:
        if go_through is None:
            go_through = []
    except AttributeError:
        pass
    if len(go_through) < 1:
        if not ispath(graph, start, dest):
            return None
        for route in graph[start]:
            if route[0] == dest:
                memo[str((start, dest, []))] = route[1]
                return route[1]
    else:
        routes = []
        for subset in all_subsets(go_through):
            for ind, city in enumerate(subset):
                try:
                    val1 = memo[str((dest, city, []))]
                except KeyError:
                    val1 = precise_alg(graph, dest, city, [], memo)
                    if str(val1).isnumeric():
                        memo[str((dest, city, []))] = val1
                try:
                    val2 = memo[str((start, city, subset[ind+1:]))]
                except KeyError:
                    val2 = precise_alg(graph, start, city, subset[ind+1:], memo)
                    if str(val2).isnumeric():
                        memo[str((start, city, subset))] = val2
                try:
                    routes.append(val1 + val2)
                except TypeError:
                    pass
    if len(routes)>0:
        return min(routes)

def greedy_alg():
    '''
    Ця функція вирішує задачу комівояжера "жадібним" приблизним алгоритмом 
    (Nearest neighbour algorithm)
    '''
    return

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    #тут може бути запуск функцій вручну
