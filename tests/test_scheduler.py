from datetime import UTC, datetime, timedelta

from automation.scheduler import Scheduler, ScheduleSpec


def test_scheduler_requires_timezone():
    scheduler = Scheduler()
    try:
        scheduler.schedule(ScheduleSpec("x", datetime(2030, 1, 1, tzinfo=UTC).replace(tzinfo=None)))
        assert False
    except ValueError:
        pass

def test_scheduler_returns_due_jobs():
    scheduler = Scheduler()
    now = datetime.now(UTC)
    scheduler.schedule(ScheduleSpec("x", now - timedelta(seconds=1)))
    assert len(scheduler.due(now)) == 1
