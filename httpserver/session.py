from collections.abc import MutableMapping

class BaseSession(MutableMapping):
    pass

class Session(BaseSession):
    def __delitem__(self, v):
        print(v)
    def __getitem__(self, k):
        print(k)
        return super().__getitem__(k)
    def __iter__(self):
        print("iter")
    def __len__(self):
        print("len")
    def __setitem__(self, k, v):
        print(k,v)
        super().__setitem__(k, v)
        

session = Session()

session["name"] = "Bexruz"

# print(session.get("name"))