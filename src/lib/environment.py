class Environment:
    def __init__(self, enclosing_env=None):
        self._enclosing_env = enclosing_env
        self._dict = {}

    def declare(self, key, value):
        if self._get_impl(key):
            raise ValueError(f"environment: key {key} already declare")
        return self._set_impl(key, value)

    def assign(self, key, value):
        if not self._get_impl(key):
            raise ValueError(
                f"environment: cannot assign to {key}, variable not declared"
            )
        return self._set_impl(key, value)

    def get(self, key):
        value = self._get_impl(key)
        if not value:
            raise ValueError(f"environment: key {key} not defined")
        return value

    def _get_impl(self, key):
        env = self
        while env:
            if key in env._dict:
                return env._dict[key]
            env = env._enclosing_env
        return None

    def _set_impl(self, key, value):
        self._dict[key] = value
        return value
