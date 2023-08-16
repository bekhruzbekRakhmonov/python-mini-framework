class Octopus:
    __instance = None

    def __new__(cls,name: str):
        if cls.__instance != None:
            raise Exception("App already registered.")
        cls.__instance = name
        return cls

    @classmethod
    def run(self):
        print("Running",self.__instance)


octo = Octopus(__name__)
octo.run()

octo2 = Octopus(__name__)