DATA = {"name": "Alex", "age": "too old to be employed, but old-school works)))"}


class User:
    def __str__(self):
        return f"\n{self.__class__.__name__} - {self.name} - {self.age}"


class User_setattr(User):
    def __init__(self, d: dict):
        for key in d:
            setattr(self, key, d[key])


class User_magic_dict(User):
    def __init__(self, d: dict):
        self.__dict__.update(d)


users = (User_setattr(DATA), User_magic_dict(DATA))

for user in users:
    print(user)
