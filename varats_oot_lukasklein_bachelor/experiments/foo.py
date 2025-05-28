class ThisIsMyClass:

    def __new__(cls):
        instance = super(ThisIsMyClass, cls).__new__(cls)

        print(f"---> Loaded ThisIsMyClass")

        return instance


a = ThisIsMyClass()
