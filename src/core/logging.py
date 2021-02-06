
import logging


class LoggerHandler:
    log = None

    def __init__(self):
        self.set_log_config(level=logging.DEBUG)

    def set_log_config(self, level):
        logging.basicConfig(
            level=level,
            format=(
                '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - '
                '%(funcName)s: %(message)s'
            ),
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.log = logging.getLogger(name=self.__class__.__name__)

    def info(self, msg, *args, **kwargs):
        return self.log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self.log.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return self.log.debug(msg, *args, **kwargs)


log = LoggerHandler()
