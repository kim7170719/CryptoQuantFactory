import importlib
import os
import logging

class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        for fname in os.listdir(self.plugin_dir):
            if fname.endswith('.py') and fname != '__init__.py':
                name = fname[:-3]
                try:
                    module = importlib.import_module(f'plugins.{name}')
                    self.plugins[name] = module
                except Exception as e:
                    logging.error(f'Failed to load plugin {name}: {e}')

    def get_plugin(self, name):
        return self.plugins.get(name)

    def reload_plugins(self):
        self.plugins = {}
        self.load_plugins()
