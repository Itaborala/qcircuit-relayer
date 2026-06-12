# qcircuit_relayer/platforms/builtin/aer.py

import uuid
from qiskit_aer import AerProvider, AerSimulator
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
        method = name if name and name != "aer_simulator" else 'automatic'
        return AerSimulator(method=method)
        #return self._provider.get_backend(name)

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

    def submit(self, circuit, job_type: JobType, **kwargs):
        pubs = circuit if isinstance(circuit, (list, tuple)) else [circuit]
        if job_type == JobType.SAMPLER:
            sampler = SamplerV2.from_backend(self._backend)
            primitive_job = sampler.run(pubs, **kwargs)
        elif job_type == JobType.ESTIMATOR:
            observables = kwargs.pop("observables")
            estimator = EstimatorV2.from_backend(self._backend)
            pub_list = [(c, observables) for c in pubs]
            primitive_job = estimator.run(pub_list, **kwargs)
        else:
            raise ValueError(f"Unsupported JobType: {job_type}")
        return AerJob(primitive_job, job_type)
    
    def retrieve(self, job_id: str):
        raise NotImplementedError("Retrieval by ID is not supported in AerEngine, which is designed for synchronous execution.")
    

class AerJob(ExecutionJob):
    def __init__(self, primitive_job, job_type: JobType):
        self._job = primitive_job
        self._type = job_type
        self._id = str(uuid.uuid4())
        self._cached = None

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
        if self._cached is None:
            self._cached = self._job.result()
        return self._cached

    def memory(self, pub_index: int = 0)-> list[str]:
        if self._type != JobType.SAMPLER:
            raise ValueError("Memory is only available for sampler jobs.")
        return list(self.result()[pub_index].data.meas.get_bitstrings())


    def cancel(self):
        pass

