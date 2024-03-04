from __future__ import annotations
import logging
from typing import Union
from logging import Logger as BaseLogger
from .settings import LogSettings, LogLevel, LogTarget
# ---------------------------------------------------------


class Logger(BaseLogger):
    def log(self, msg : str, level : Union[int, LogLevel] = LogLevel.INFO, leading_newline : bool = False, *args, **kwargs):
        if isinstance(level, LogLevel):
            level = level.value
        if leading_newline:
            msg = '\n' + msg

        super().log(msg=msg, level=level, *args, **kwargs)

    def setLevel(self, level : Union[int, LogLevel]):
        if isinstance(level, LogLevel):
            level = level.value
        super().setLevel(level)


class LoggerFactory:
    _default_settings : LogSettings = LogSettings()

    @classmethod
    def set_defaults(cls, settings : LogSettings):
        cls._default_settings = settings

    @classmethod
    def make_logger(cls, name : str, settings : LogSettings) -> Logger:
        settings = settings or cls._default_settings

        logger = Logger(name=name)
        logger.propagate = False
        logger.setLevel(settings.threshold)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.CONSOLE))
        logger.addHandler(console_handler)

        if settings.log_fpath:
            file_handler = logging.FileHandler(settings.log_fpath)
            file_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.FILE))
            logger.addHandler(file_handler)


        return logger


class Formatter(logging.Formatter):
    custom_file_name = 'custom_file_name'
    custom_line_no = 'custom_lineno'

    colors: dict = {
        logging.DEBUG: '\033[20m',
        logging.INFO: '\033[20m',
        logging.WARNING: '\033[93m',
        logging.ERROR: '\033[91m',
        logging.CRITICAL: '\x1b[31;1m'  # Bold Red
    }

    def __init__(self, settings : LogSettings, log_target : LogTarget):
        self.settings : LogSettings = settings
        self.log_target : LogTarget = log_target
        super().__init__()


    def format(self, record):
        log_fmt = "%(message)s"

        if self.settings.timestamp:
            custom_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            conditional_millis = f" {int(record.msecs)}ms" if self.settings.include_ms else ""
            timestamp = f"[{custom_time}{conditional_millis}]"
            log_fmt = f"{timestamp}: {log_fmt}"

        if self.settings.call_location:
            filename = getattr(record, Formatter.custom_file_name, record.filename)
            lineno = getattr(record, Formatter.custom_line_no, record.lineno)
            log_fmt += f" {filename}:{lineno}"

        if self.log_target == LogTarget.CONSOLE:
            color_prefix = Formatter.colors.get(record.levelno, "")
            color_suffix = "\033[0m"
            log_fmt = color_prefix + log_fmt + color_suffix

        self._style._fmt = log_fmt
        return super().format(record)