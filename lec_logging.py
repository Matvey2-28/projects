import logging

def main():
    logging.basicConfig(format='%(threadName)s %(name)s %(levelname)s: %(message)s')
    logger = logging.getLogger('astromodel')
    
    logger.debug('debug message')
    logger.log(level=logging.DEBUG, msg="second debug message")

    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("у тебя сейчас комп бахнет")


if __name__ == "__main__":
    main()