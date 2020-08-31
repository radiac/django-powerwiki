from django.utils.module_loading import import_string

from .. import app_settings


engines = {}


def load_engines():
    for class_name in app_settings.MARKUP_ENGINES:
        engines[class_name] = import_string(class_name)
    return engines


def get_engine(class_name):
    # Just sanity check to make sure something odd isn't going on
    if class_name not in engines:
        raise ValueError(f"Unknown wiki markup engine: {class_name}")
    return engines[class_name]


def engine_field_choices():
    return [
        (engine_name, engines[engine_name].label)
        for engine_name in app_settings.MARKUP_ENGINES
    ]
