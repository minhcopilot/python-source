class MyClass():
    def __init__(self) :
        self.__superprivate ="hello"
        self._superprivate=", word!"
mc=MyClass()
print(mc.__superprivate)
print(mc._superprivate)