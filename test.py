import importlib
mod = importlib.import_module('plugins.hello')
print mod.__name__
