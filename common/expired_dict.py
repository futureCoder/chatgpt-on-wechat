from datetime import datetime, timedelta


# 为Python内建Dict增加了过期时间的功能
class ExpiredDict(dict):
    def __init__(self, expires_in_seconds):
        super().__init__()
        self.expires_in_seconds = expires_in_seconds

    # 如果当前时间超过了过期时间，那么这个键值对会被删除，并且抛出一个 "key expired" 的异常。否则，它会返回该键的值。
    def __getitem__(self, key):
        value, expiry_time = super().__getitem__(key)
        if datetime.now() > expiry_time:
            del self[key]
            raise KeyError("expired {}".format(key))
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        expiry_time = datetime.now() + timedelta(seconds=self.expires_in_seconds)
        super().__setitem__(key, (value, expiry_time))
    # 获取该键的值，如果失败（因为键不存在或已过期）则返回默认值。
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    # 返回字典中的所有键，但只返回那些还没过期的键。
    def keys(self):
        keys = list(super().keys())
        return [key for key in keys if key in self]

    # 返回字典中的所有键值对，但只返回那些还没过期的键值对。
    def items(self):
        return [(key, self[key]) for key in self.keys()]

    # 使得 ExpiredDict 对象可以被迭代，迭代的是所有还没过期的键。
    def __iter__(self):
        return self.keys().__iter__()
