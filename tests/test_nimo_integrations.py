from integrations.nimo_projects import NIMO_PROJECTS
from integrations.promotion import Promotion, PromotionChannel, PromotionPolicy


def test_nimo_projects_are_registered():
    ids = {project.id for project in NIMO_PROJECTS}
    assert {"nimo-core", "nimo-agent", "nimo-web", "nimo-autolab", "nimo-knowledge"} <= ids

def test_promotion_policy_requires_enabled_destination():
    item = Promotion("nimo-agent", "NIMO Agent", "Try it", PromotionChannel.IN_APP, "project")
    assert PromotionPolicy().allowed(item, "relevant")
