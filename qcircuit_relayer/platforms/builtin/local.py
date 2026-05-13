# qcircuit_relayer/platforms/builtin/aer.py

import uuid
from qiskit_aer import AerProvider
from qiskit_aer.primitives import SamplerV2, EstimatorV2

from qcircuit_relayer.core.interfaces import (
    QuantumPlatform, ExecutionEngine, ExecutionJob, JobType,
)


class AerPlatform(QuantumPlatform):
    name = "aer"

    def __init__(self):
        self._provider = None

    def connect(self, **credentials):
        self._provider = AerProvider()

    def backends(self):
        return self._provider.backends()

    def get_backend(self, name="aer_simulator"):
        return self._provider.get_backend(name)

    def engine(self, backend, mode="default"):
        return AerEngine(backend)


class AerEngine(ExecutionEngine):
    name = "aer"

    def __init__(self, backend= None):
        self._backend = backend


    def capabilities(self):
        return {
            "supported_types": [JobType.SAMPLER, JobType.ESTIMATOR],
            "synchronous": True,
            "simulator": True,
        }

    def submit(self, circuit, type: JobType, **kwargs):
        if type == JobType.SAMPLER:
            sampler = SamplerV2.from_backend(self._backend)
            primitive_job = sampler.run([circuit], **kwargs)
        elif type == JobType.ESTIMATOR:
            observables = kwargs.pop("observables")
            estimator = EstimatorV2.from_backend(self._backend)
            primitive_job = estimator.run([(circuit, observables)], **kwargs)
        else:
            raise ValueError(f"Unsupported JobType: {type}")
        return AerJob(primitive_job, type)
    

class AerJob(ExecutionJob):
    def __init__(self, primitive_job, job_type: JobType):
        self._job = primitive_job
        self._type = job_type
        self._id = str(uuid.uuid4())

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._job.status().name.lower()

    @property
    def type(self):
        return self._type

    def result(self, timeout=None):
        return self._job.result()


    def cancel(self):
        pass

