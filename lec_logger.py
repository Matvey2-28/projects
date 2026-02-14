import logging

logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def log_variables_and_exceptions():
    try:

        a = 10
        b = 'Hello, world!'
        logging.debug(f'Значение переменной 1: {a}')
        logging.debug(f'Значение переменной 2: {b}')
        
        result = a / 0  
    except Exception as e:

        logging.error(f'Произошло исключение: {e}', exc_info=True)

log_variables_and_exceptions()