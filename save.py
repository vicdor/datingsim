import pickle

# Default path to save and access game data
DEFAULT_PATH = ".datingsimsave"

class SaveData():
    """
    An instance of this class will be used to hold all datingsim save data
    in picklable format. It's important to note that locational functions will
    be a hassle to save... so there should be designated save spots that can be
    named by string/number and to which play can be restored.
    """
    def __init__(self):
        self.dict = {}  # dict will probably be private later with access fns
    

    def BURN_BABY_BURN(self, path=DEFAULT_PATH):
        """
        for less whimsy, see write()
        """
        _write_pickle(self, path)


    def write(self):
        self.BURN_BABY_BURN()


def _write_pickle(obj, path):
    f = open(path, 'wb')
    pickle.dump(obj, f)
    f.close()


def _read_pickle(path):
    """
    returns an unpickled object from path
    """
    f = open(path, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj


if __name__ == '__main__':
    path = DEFAULT_PATH + 'test'
    print("Test save to be written to {p}".format(p=path))
    test_string = input("Please input test string to be stored: ")

    data = SaveData()
    data.dict['test'] = test_string
    data.BURN_BABY_BURN(path)

    loadedData = _read_pickle(path)
    print("Loaded {obj} from {p}".format(p=path, obj=loadedData))
    print("Dictionary data follows: " + str(data.dict))


