import pickle


def gen_pickle(source):
    for item in source:
        yield pickle.dumps(item)


def gen_unpickle(file):
    while True:
        try:
            item = pickle.load(file)
            yield item
        except EOFError:
            return
