class Environment:
    def __init__(self, enclosing_env=None):
        self._enclosing_env = enclosing_env
        self._dict = {}

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        env = self
        while env:
            if key in env._dict:
                return env._dict[key]
            env = env._enclosing_env
        raise ValueError(f"environment: key {key} not defined")
