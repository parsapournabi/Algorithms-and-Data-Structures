"""training some graph example: by city traveling"""


class Graph:
    adj_dict: dict = {}
    adj_matrix: list = []
    grid: list = []

    def __init__(self, edges, routs=None):
        if routs is None:
            routs = []
        self.edges = edges
        self.sorting = routs
        self.create_adj_list()
        self.create_adj_matrix()
        print(self.adj_dict, '\n')
        print('\n'.join(list(map(str, self.adj_matrix))), '\n')

    def create_adj_list(self):
        for start, dist, _, _ in self.edges:
            if start in self.adj_dict.keys():
                self.adj_dict[start].append(dist)
            else:
                self.adj_dict[start] = [dist]
            if dist in self.adj_dict.keys():
                if start not in self.adj_dict[dist]:
                    self.adj_dict[dist].append(start)
            else:
                self.adj_dict[dist] = [start]
        return True

    def create_adj_matrix(self):
        self.adj_matrix = [[0 for _ in range(len(self.adj_dict.keys()))] for _ in range(len(self.adj_dict.keys()))]
        self.grid = self.sorting if self.sorting else list(self.adj_dict.keys())
        for start, dist, cost, cost_rev in self.edges:
            index_start = self.grid.index(start)
            index_dist = self.grid.index(dist)
            self.adj_matrix[index_start][index_dist] = cost
            self.adj_matrix[index_dist][index_start] = cost_rev

    def get_paths(self, start, dist, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start == dist:
            return [path]
        if start not in self.adj_dict:
            return []
        ret: list = []
        for vertex in self.adj_dict[start]:
            if vertex not in path:
                new_paths = self.get_paths(vertex, dist, path)
                for p in new_paths:
                    ret.append(p)
        return ret

    def get_costs(self, start, dist):
        all_ways = self.get_paths(start, dist)
        for j, ways in enumerate(all_ways):
            cost = []
            for i in range(len(ways) - 1):
                y_start = self.grid.index(ways[i])
                x_dist = self.grid.index(ways[i + 1])
                cost.append(self.adj_matrix[y_start][x_dist])
            all_ways[j].append(sum(cost))
        return all_ways

    def shortest_way(self, start, dist):
        all_ways = self.get_paths(start, dist)
        sorting_ways = sorted(all_ways, key=lambda x: len(x))
        sorting_ways_length = [len(w) for w in sorting_ways]
        if sorting_ways_length.count(sorting_ways_length[0]) > 1:
            ret: list = []
            for s in sorting_ways:
                if len(s) == len(sorting_ways[0]):
                    ret.append(s)
            return ret
        return sorting_ways[0]

    def lowest_cost(self, start, dist):
        all_ways = self.get_costs(start, dist)
        sorting_ways = sorted(all_ways, key=lambda x: x[-1])
        prices = [price[-1] for price in sorting_ways]
        if prices.count(sorting_ways[0][-1]) > 1:
            ret: list = []
            for way in sorting_ways:
                if way[-1] == sorting_ways[0][-1]:
                    ret.append(way)
            return ret
        return sorting_ways[0]


if __name__ == '__main__':
    sorting = ['Mashhad', 'Tehran', 'Karaj', 'Amol', 'Kerman', 'Qazvin', 'Rasht']
    df = [('Mashhad', 'Tehran', 100, 120),
          ('Mashhad', 'Amol', 150, 30),
          ('Tehran', 'Amol', 90, 45),
          ('Tehran', 'Karaj', 60, 50),
          ('Tehran', 'Kerman', 135, 90),
          ('Amol', 'Rasht', 17, 30),
          ('Amol', 'Karaj', 20, 85),
          ('Karaj', 'Qazvin', 100, 75),
          ('Karaj', 'Kerman', 120, 40),
          ('Qazvin', 'Rasht', 50, 40),
          ('Qazvin', 'Kerman', 25, 33)]

    graph = Graph(df, sorting)
    # all_ways = graph.get_paths('Tehran', 'Rasht')
    # print(all_ways, '\n')
    # print(sorted(all_ways, key=lambda x: len(x)))
    # print([len(w) for w in sorted(all_ways, key=lambda x: len(x))])
    # print(graph.get_costs('Mashhad', 'Rasht'), '\n')
    print(graph.shortest_way('Mashhad', 'Rasht'))
    print(graph.lowest_cost('Mashhad', 'Rasht'))
