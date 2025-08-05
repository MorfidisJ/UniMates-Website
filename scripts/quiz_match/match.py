import networkx as nx

# ai generated from static/pages/quiz-bills-lifestyle.html
compatibility_matrices = [
    # 0. Bills and utilities
    [
        [2, 1, 1],
        [1, 2, 0],
        [1, 0, 2],
    ],
    # 1. Sharing stuff
    [
        [2, 1, 0],
        [1, 2, 0],
        [0, 0, 2],
    ],
    # 2. Food and common items
    [
        [2, 2, 1],
        [2, 2, 1],
        [1, 1, 2],
    ],
    # 3. How clean are you?
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 4. Cleaning frequency
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 5. Dishes
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 6. Smoking
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 7. Pets
    [
        [2, 2, 0],
        [2, 2, 1],
        [0, 1, 2],
    ],
    # 8. Sleep schedule
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 9. Quiet preference
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 10. Guests
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 11. Parties
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ],
    # 12. Cooking
    [
        [2, 2, 2],
        [2, 2, 2],
        [2, 2, 2],
    ],
    # 13. Drinking
    [
        [2, 2, 1, 0],
        [2, 2, 1, 0],
        [1, 1, 2, 1],
        [0, 0, 1, 2],
    ],
    # 14. Roommate relationship
    [
        [2, 1, 0],
        [1, 2, 1],
        [0, 1, 2],
    ]
]



class Person:
    cities = []

    def __init__(self, arr):
        self.name = arr[0]
        self.email = arr[1]
        
        self.city = arr[2]
        if self.city not in Person.cities:
            Person.cities.append(self.city)

        self.phone = arr[3]
        self.gender = arr[4]

        self.answers = {}
        for i, ans in enumerate(arr[5:]):
            self.answers[i] = int(ans)

    def __repr__(self):
        return f"{self.name} @ {self.city}"

    @property
    def id(self):
        return self.email


def getScore(p1, p2):
    assert(len(p1) == len(p2) == len(compatibility_matrices))

    s = 0
    for i, m in enumerate(compatibility_matrices):
        s += m[p1[i]][p2[i]]

    return s/(2*len(compatibility_matrices))


def buildGraph(graph, people):
    for i, person1 in enumerate(people):
        for person2 in people[i+1:]:
            if person1.city != person2.city:
                continue
            score = round(getScore(person1.answers, person2.answers), 4)
            graph.add_edge(person1.id, person2.id, weight=score)



if __name__ == "__main__":
    import os
    import sys
    import csv

    if len(sys.argv) < 2:
        print("no file")
        exit(1)

    fpath = sys.argv[1]

    if not os.path.exists(fpath):
        print(f"{fpath} does not exist")
        exit(1)

    matrix = []
    with open(fpath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            matrix.append(row)

    people = [Person(x) for x in matrix[1:]]

    graph = nx.Graph()
    buildGraph(graph, people)
    matches = nx.algorithms.matching.max_weight_matching(graph, maxcardinality=False)

    print(matches)

