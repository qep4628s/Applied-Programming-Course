from icecream import ic


class SimpleDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        ic("Before function")
        result = self.func()
        ic("After function")
        return result


@SimpleDecorator
def say_hello():
    ic("Hello from the function")


say_hello()