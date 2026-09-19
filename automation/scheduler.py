from dataclasses import dataclass
from datetime import datetime, timezone
import sqlite3

@dataclass(frozen=True)
class ScheduleSpec:
    automation_id: str
    run_at: datetime
    job_id: str | None = None

class Scheduler:
    """Timezone-aware scheduler with SQLite persistence and one-shot claiming."""
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db = sqlite3.connect(db_path)
        self.db.execute("CREATE TABLE IF NOT EXISTS jobs (job_id TEXT PRIMARY KEY, automation_id TEXT NOT NULL, run_at TEXT NOT NULL, claimed INTEGER NOT NULL DEFAULT 0)")
        self.db.commit()

    def schedule(self, job: ScheduleSpec) -> str:
        if job.run_at.tzinfo is None:
            raise ValueError("Scheduled times must include a timezone.")
        job_id = job.job_id or f"{job.automation_id}:{job.run_at.isoformat()}"
        self.db.execute("INSERT OR IGNORE INTO jobs(job_id,automation_id,run_at) VALUES(?,?,?)",
                        (job_id, job.automation_id, job.run_at.astimezone(timezone.utc).isoformat()))
        self.db.commit()
        return job_id

    def due(self, now: datetime | None = None) -> list[ScheduleSpec]:
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        rows = self.db.execute("SELECT job_id,automation_id,run_at FROM jobs WHERE claimed=0 AND run_at<=? ORDER BY run_at",
                               (current.isoformat(),)).fetchall()
        return [ScheduleSpec(a, datetime.fromisoformat(r), j) for j,a,r in rows]

    def claim(self, job_id: str) -> bool:
        cur = self.db.execute("UPDATE jobs SET claimed=1 WHERE job_id=? AND claimed=0", (job_id,))
        self.db.commit()
        return cur.rowcount == 1

    def close(self) -> None:
        self.db.close()
