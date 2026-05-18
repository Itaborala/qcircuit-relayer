from qcircuit_relayer.core.interfaces import ExecutionEngine, JobType
from .job import IonQJob


_NOISE_MODEL_QUBIT_LIMITS = {
    "ideal": 29,
    "aria-1": 25,
    "aria-2": 25,
    "forte-1": 29,
    "forte-enterprise-1": 29,
}


class IonQEngine(ExecutionEngine):
    name = "ionq"

    def __init__(self, backend):
        self._backend = backend

    def capabilities(self) -> dict:
        is_sim = "simulator" in self._backend.name
        return {
            "supported_types": [JobType.SAMPLER],
            "synchronous": False,
            "simulator": is_sim,
            "max_qubits": 29 if is_sim else None,
            "noise_models": list(_NOISE_MODEL_QUBIT_LIMITS) if is_sim else None,
            "server_side_optimization": True,
            "all_to_all_connectivity": True,
        }

    def submit(self, circuit, job_type: JobType, **kwargs):
        circs = circuit if isinstance(circuit, list) else [circuit]
        if job_type != JobType.SAMPLER:
            raise ValueError(f"IonQ is sampler-only; got {type}")

        is_sim = "simulator" in self._backend.name
        noise_model = kwargs.pop("noise_model", None)

        if noise_model is not None:
            if not is_sim:
                raise ValueError("noise_model is simulator-only")
            if noise_model not in _NOISE_MODEL_QUBIT_LIMITS:
                raise ValueError(
                    f"Unknown noise_model {noise_model!r}; "
                    f"expected one of {list(_NOISE_MODEL_QUBIT_LIMITS)}"
                )
            self._backend.set_options(noise_model=noise_model)

        if is_sim:
            limit = _NOISE_MODEL_QUBIT_LIMITS.get(noise_model or "ideal", 29)
            for c in circs:
                if c.num_qubits > limit:
                    raise ValueError(
                        f"Circuit uses {circuit.num_qubits} qubits; "
                        f"simulator limit with noise_model={noise_model or 'ideal'!r} is {limit}"
                    )

        return IonQJob(self._backend.run(circs, **kwargs))
