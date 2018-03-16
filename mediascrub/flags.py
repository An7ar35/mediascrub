from enum import Enum, auto


class PrefixType(Enum):
    DOMAIN = auto()
    URL = auto()

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return self.name

    @staticmethod
    def translate( string):
        if string is 'domain':
            return PrefixType.DOMAIN
        elif string is 'url':
            return PrefixType.URL
        else:
            raise ValueError('Prefix type \'' + string + '\' is not valid.')
