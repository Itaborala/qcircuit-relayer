from qiskit_ionq import IonQProvider

from qcircuit_relayer.core.interfaces import QuantumPlatform
from .engine import IonQEngine
from .credentials import resolve_token

import warnings
from qiskit_ionq.exceptions import IonQTranspileLevelWarning
warnings.filterwarnings("ignore", category=IonQTranspileLevelWarning)


class IonQPlatform(QuantumPlatform):
    name = "ionq"

    def __init__(self):
        self._provider = None

    def connect(self, project_name: str = "default", token: str | None = None, **_):
        self._provider = IonQProvider(token=resolve_token(project_name, token))

    def backends(self):
        return self._provider.backends()

    def get_backend(self, name: str = "simulator", gateset: str = "qis", **kwargs):
        return self._provider.get_backend(name, gateset=gateset, **kwargs)

    def engine(self, backend, mode: str = "default") -> IonQEngine:
        return IonQEngine(backend)
