class For:
    def __init__(self, *args):
        self.lists = args
        for i, e in enumerate(args):
            setattr(self, f'list{i}', e)

    def index(self, e, i):
        try:
            return e[i]
        except IndexError:
            return None

    def max_len(self, tab):
        return max([len(e) for e in self.lists])

    def __iter__(self):
        for i in range(self.max_len(self.lists)):
            yield [self.index(e, i) for e in self.lists]


if __name__ == '__main__':
    for a, b, h in For('test', 'amaury', range(5, 10)):
        print(a, b, h)
