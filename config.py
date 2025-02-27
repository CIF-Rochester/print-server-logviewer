
import os
import sys
import configparser
from dataclasses import dataclass

@dataclass
class Logging:
    log_path: os.PathLike
    file_storage_path: os.PathLike
    file_storage_time: int

@dataclass
class Config:
    logging: Logging

def load_config(config_path: os.PathLike):
    try:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
    except Exception as e:
        print(f"Failed to load config file from {config_path}: {e}", file=sys.stderr)
        exit(1)
    try:
        logging = Logging(log_path=cfg.get("logging","log_path"), file_storage_path=cfg.get("logging","file_storage_path"), file_storage_time=cfg.getint("logging","file_storage_time"))
        config = Config(logging=logging)
    except Exception as e:
        print(f"Error in config file {config_path}: {e}", file=sys.stderr)
        exit(1)
    return config