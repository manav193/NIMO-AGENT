from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class ScheduleSpec:
    automation_id: str
    run_at: datetime

class Scheduler:
    """Minimal scheduler boundary; execution is delegated to approved automation handlers."""
    def __init__(self) -> None:
        self._jobs: list[ScheduleSpec] = []

    def schedule(self, job: ScheduleSpec) -> None:
        if job.run_at.tzinfo is None:
            raise ValueError("Scheduled times must include a timezone.")
        self._jobs.append(job)

    def due(self, now: datetime | None = None) -> list[ScheduleSpec]:
        current = now or datetime.now(timezone.utc)
        return [job for job in self._jobs if job.run_at <= current]
