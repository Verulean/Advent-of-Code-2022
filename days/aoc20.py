from collections import deque


fmt_dict = {"cast_type": int}


class EncryptedList:
    def __init__(self, data, decryption_key=1):
        self.__base_order = data.copy()
        self.__z = (self.__base_order.index(0), 0)
        self.__n = len(self.__base_order) - 1
        self.reset(decryption_key)

    def reset(self, decryption_key=1):
        self.__order = [v * decryption_key for v in self.__base_order]
        self.__q = deque(enumerate(self.__order))

    def mix(self):
        for node in enumerate(self.__order):
            self.__q.rotate(-self.__q.index(node))
            self.__q.popleft()
            self.__q.rotate(-node[1] % self.__n)
            self.__q.appendleft(node)

    @property
    def coordinates(self):
        iz = self.__q.index(self.__z)
        return sum(
            self.__q[(iz + i) % (self.__n + 1)][1] for i in (1000, 2000, 3000)
        )


def solve(data):
    l = EncryptedList(data)
    l.mix()
    ans1 = l.coordinates
    l.reset(811589153)
    for _ in range(10):
        l.mix()
    return ans1, l.coordinates
