import os
from abc import abstractmethod
from typing import Optional, Text, Any


class MandatoryEnvVarNotFound(Exception):

    def __init__(self, message: Text):
        super().__init__(message)

    @classmethod
    def with_env_var(cls, env_var_name: Text) -> 'MandatoryEnvVarNotFound':
        return cls(f'{env_var_name} environment variable is not set')


class EnvironmentVarGetter:

    @abstractmethod
    def get(self, var_name: Text, default: Optional[Any] = None) -> Optional[Text]:
        pass

    @abstractmethod
    def get_or_fail(self, var_name: Text) -> Optional[Text]:
        pass


class OSEnvironmentVarGetter(EnvironmentVarGetter):

    def get(self, var_name: Text, default: Optional[Any] = None) -> Optional[Text]:
        try:
            return os.environ[var_name]
        except KeyError:
            return default

    def get_or_fail(self, var_name: Text) -> Optional[Text]:
        if var_name in os.environ:
            return os.environ[var_name]

        raise MandatoryEnvVarNotFound.with_env_var(var_name)
