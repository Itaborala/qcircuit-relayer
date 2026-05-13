from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from qiskit import QuantumCircuit

class JobType(Enum):
    SAMPLER = "sampler"
    ESTIMATOR = "estimator"


class ExecutionJob(ABC):
    
    @property
    @abstractmethod
    def id(self) -> str:
        ...


    @property
    @abstractmethod
    def status(self) -> str:
        ...


    @property
    @abstractmethod
    def type(self) -> JobType:
        ...

    @abstractmethod
    def result(self)-> Any:
        ...


    @abstractmethod
    def cancel(self):
        ...
class ExecutionEngine(ABC):

    @abstractmethod
    def __init__(self, name:str):
        self.name: str = name
        
    @abstractmethod
    def submit(self, circuit: QuantumCircuit, job_type: JobType, **kwargs) -> ExecutionJob:
        ...

    @abstractmethod
    def capabilities(self) -> dict:
        ...

class QuantumPlatform(ABC):

    @abstractmethod
    def __init__(self):
        self.name: str

    @abstractmethod
    def connect(self, **credentials):
        ...

    @abstractmethod
    def backends(self):
        ...

    @abstractmethod
    def get_backend(self, name: str):
        ...

    @abstractmethod
    def engine(self, backend, mode: str = 'default') -> ExecutionEngine:
        ...



    

