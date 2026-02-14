import logging
logger1 = logging.getLogger('logger1')
logger2 = logging.getLogger('logger2')
logging.basicConfig(filename='common_log.txt', format='%(name)s %(levelname)s: %(message)s')

def log_variables_and_exceptions():
    
    logger2.debug('debug message')
    logger1.info("info message")
    logger1.warning("warning message")
    logger2.error("error message")

log_variables_and_exceptions()