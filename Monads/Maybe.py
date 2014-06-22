'''
Maybe monad for python.

Since I've found that having positive control over potentially failing computations makes me a more reliable coder,
I've taken to using monads whenever possible. In this case, the Maybe monad represents computations that can fail,
either for unknown or obvious reasons. If one chains together such computations, and any of them fails, rather than
getting an exception or a null-object to worry about, the entire chain will simply return a Nothing() object.
Otherwise, it will return a Just(answer) object. To use this in a OO environment, you start by creating a Just(question)
object, then call bind(comp) for each computational step, and finish by unwrapping the monad with fromMaybe(default).

For example: Just("Hello there!").bind(lambda x: x.toUpper()).fromMaybe("") should return "HELLO THERE!", while
Just("Hello there!").bind(lambda x: Nothing()).fromMaybe("Nada!") should return "Nada". Within each bind's lambda,
one may assume that one will never see a null value, since the previous computation would have prevented us from
running in that case.
'''


class Maybe:
    def pure(self, arg):
        return NotImplemented
    def bind(self, func):
        return NotImplemented
    def fromMaybe(self, default):
        return NotImplemented
    def liftM2(self,f,m2):
        '''Lift a two-argument function, with self as first argument, into the Maybe monad.'''
        return self.bind(lambda x: m2.bind(lambda y: Just(f(x,y))))

class Just(Maybe):
    def __init__(self, arg):
        self.arg = arg

    def pure(self, arg):
        self.arg = arg

    def bind(self, func):
        return func(self.arg)

    def fromMaybe(self, default):
        return self.arg

    def __str__(self):
        return "Just {}".format(self.arg)

class Nothing(Maybe):
    def __init__(self):
        ''' Do nothing '''

    def pure(self, arg):
        ''' Do nothing '''
        return Nothing()

    def bind(self, func):
        ''' Do nothing '''
        return Nothing()

    def fromMaybe(self, default):
        return default

    def __str__(self):
        return "Nothing"
