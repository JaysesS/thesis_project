import logging.config
import os


def init_logger(app):
    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)8s - %(message)s",
                "datefmt": "%d-%m-%Y %H:%M:%S"
            },
            "extended": {
                "format": "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
            }
        },
        "handlers": {
            "console":{
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream" : "ext://sys.stdout"
            },
            "file_handler_Thesis": {
                "level": "NOTSET",
                "class": "logging.handlers.WatchedFileHandler",
                "formatter": "simple",
                "filename": os.path.join(app.config['LOG_DIR'], "thesis.log"),
                "mode": "a",
                "encoding": "utf-8"
            },
            # "smtp_Thesis": {
            #     "level": "ERROR",
            #     "class": "logging.handlers.SMTPHandler",
            #     "formatter": "simple",
            #     "mailhost": ["smtp.gmail.com", 587],
            #     "fromaddr": "",
            #     "toaddrs": [""],
            #     "subject": "ERROR ON THESIS WORK #red",
            #     "credentials" : ["",""],
            #     "secure" : []
            # },
        },

        "loggers": {
            "THESIS": {
                "level": "NOTSET",
                "handlers": [ "file_handler_Thesis"],
                "propagate": False
            }
        },
        "root": {
            "level": "NOTSET",
            "handlers": ["console"]
        }
    }
    if app.config["LOCAL"]:
        for logger, settings in conf['loggers'].items():
            settings['handlers'] = [handler for handler in settings['handlers'] if "smtp_" not in handler]

        conf['root']['handlers'] = [handler for handler in conf['root']['handlers'] if "smtp_" not in handler]

    if not os.path.exists(app.config['LOG_DIR']):
        os.mkdir(app.config['LOG_DIR'])
    logging.config.dictConfig(conf)