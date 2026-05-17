from qcircuit_relayer.core.interfaces import ExecutionJob, JobType


class IonQJob(ExecutionJob):
    def __init__(self, ionq_job):
        self._job = ionq_job

    @property
    def id(self) -> str:
        return self._job.job_id()

    @property
    def status(self) -> str:
        return str(self._job.status()).lower()

    @property
    def type(self) -> JobType:
        return JobType.SAMPLER

    def result(self, timeout: float | None = None):
        return self._job.result()

    def cancel(self):
        return self._job.cancel()
