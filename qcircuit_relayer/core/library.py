import importlib
from pathlib import Path


class PlatformLibrary:
    def __init__(self):
        self._platforms = {}
        self._register_builtins()
        self._load_from_folder(Path(__file__).parent.parent / "platforms")

    def register(self, platform_cls):
        self._platforms[platform_cls.name] = platform_cls

    def get(self, name):
        if name not in self._platforms:
            raise KeyError(f"'{name}' not registered. Available: {list(self._platforms)}")
        return self._platforms[name]()

    def available(self):
        return list(self._platforms)

    def _register_builtins(self):
        from qcircuit_relayer.platforms.builtin.local import AerPlatform
        self.register(AerPlatform)

    def _load_from_folder(self, folder):
        for entry in folder.iterdir():
            if entry.is_dir() and entry.name != "builtin" and (entry / "register.py").exists():
                module_path = f"qcircuit_relayer.platforms.{entry.name}.register"
                importlib.import_module(module_path).register(self)
