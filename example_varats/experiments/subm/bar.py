class ThisIsMyOtherClass:

    def __new__(cls):
        instance = super(ThisIsMyOtherClass, cls).__new__(cls)

        print(f"---> Loaded ThisIsMyOtherClass")

        return instance


a = ThisIsMyOtherClass()
