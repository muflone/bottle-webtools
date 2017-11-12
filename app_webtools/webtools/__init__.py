# Import standard modules
import logging

db_engine_modules = (
    'engine_sqlite3',
)


def detect_db_engines():
    """Dynamic import of engines modules"""
    engines = {}
    # Dynamic import of engines modules
    for module_name in db_engine_modules:
        try:
            module = __import__(
                'app_webtools.webtools.%s' % module_name)
            engine_classes = getattr(getattr(module.webtools, module_name),
                                     'engine_classes')
            # Cycle each engine class
            for engine_class in engine_classes:
                engines[engine_class.descriptor] = engine_class
        except Exception as error:
            logging.info('Skipping DB engine %s' % module_name)
            if not isinstance(error, ImportError):
                logging.error('Unexpected exception: %s' % error.value)
    return engines
