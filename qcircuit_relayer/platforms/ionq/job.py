from qcircuit_relayer.core.interfaces import ExecutionJob, JobType
import random


class IonQJob(ExecutionJob):
    def __init__(self, ionq_job):
        self._job = ionq_job
        self._cached_result = None

    @property
    def id(self) -> str:
        return self._job.job_id()

    @property
    def status(self) -> str:
        return str(self._job.status()).lower()

    @property
    def type(self) -> JobType:
        return JobType.SAMPLER

    def _result(self):
        if self._cached_result is None:
            self._cached_result = self._job.result()
        return self._cached_result



    def result(self, timeout: float | None = None):
        return self._result()


    def memory(self, pub_index: int = 0, shots: int | None = None)-> list[str]:
        counts = self._result().get_counts(pub_index)
        print(counts)
        mem = []
        for key, n in counts.items():
           mem.extend([key] * n) 
        random.shuffle(mem)
        print(mem)
        return mem
        # mem = self._result().get_memory(pub_index)
        # return [str(bitstring) for bitstring in mem]

    def cancel(self):
        return self._job.cancel()
