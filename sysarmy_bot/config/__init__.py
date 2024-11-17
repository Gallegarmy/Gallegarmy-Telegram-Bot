from dataclasses import dataclass
from enum import StrEnum, unique, auto

from sysarmy_bot.shared.yaml_utils import yaml_as_dict


class ConfigFileNotFound(Exception):
    pass


@dataclass(frozen=True)
class TelegramConfig:
    telegram_read_timeout_seconds: int
    telegram_write_timeout_seconds: int


@unique
class Environment(StrEnum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()
    TEST = auto()

    def is_testing(self) -> bool:
        return self.__eq__(Environment.TEST)


@dataclass(frozen=True)
class Config:
    environment: Environment
    telegram: TelegramConfig

    @classmethod
    def from_yaml(cls, env: str, config_file_path: str) -> "Config":
        try:
            environment = Environment(env.lower())
            config_yaml = yaml_as_dict(config_file_path)
            return cls(
                environment=environment,
                telegram=TelegramConfig(**config_yaml.get("telegram", {})),
            )
        except FileExistsError as exc:
            raise ConfigFileNotFound from exc
