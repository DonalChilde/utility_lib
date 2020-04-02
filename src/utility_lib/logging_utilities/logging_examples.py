import logging
from logging.handlers import RotatingFileHandler
import os


LOGGER = logging.getLogger(__name__)


# NOTE library logging
# Use this in libraries to allow parent app control over logging
handler = logging.NullHandler()
LOGGER.addHandler(handler)


# NOTE console logging
# NOTE https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
# 2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
console_handler.setFormatter(formatter)

# add ch to logger
LOGGER.addHandler(console_handler)


if LOGGER.isEnabledFor(logging.DEBUG):
    LOGGER.debug("Message with %s, %s", foo(), foo())


def foo():
    pass


app = foo()

if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler(
    "logs/pbs_detective.log", maxBytes=102400, backupCount=10
)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s:%(funcName)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
)
# 2019-12-09 21:28:11,369 DEBUG:get_query_filter_model_from_key: with key: pairing_report_between [in /app/pbs_detective/blueprints/query_filters/actions.py:101]

file_handler.setLevel(app.config.get("LOG_LEVEL"))
# pylint: disable=no-member
app.logger.addHandler(file_handler)
app.logger.setLevel(app.config.get("LOG_LEVEL"))
app.logger.info("pbs_detective Startup")
