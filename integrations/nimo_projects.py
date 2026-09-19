from dataclasses import dataclass
from enum import Enum

class ProjectAction(str, Enum):
    OPEN = "open"
    STATUS = "status"
    HELP = "help"
    PROMOTE = "promote"

@dataclass(frozen=True)
class NimoProject:
    id: str
    name: str
    repository: str
    description: str
    actions: tuple[ProjectAction, ...] = (
        ProjectAction.OPEN,
        ProjectAction.STATUS,
        ProjectAction.HELP,
    )

NIMO_PROJECTS: tuple[NimoProject, ...] = (
    NimoProject("nimo-core", "NIMO Core", "manav193/NIMO-CORE", "AI infrastructure and model/API backend."),
    NimoProject("nimo-agent", "NIMO Agent", "manav193/NIMO-AGENT", "Personal computer-agent and automation runtime."),
    NimoProject("nimo-web", "NIMO Web", "manav193/NIMO-WEB", "NIMO user-facing web client."),
    NimoProject("nimo-autolab", "NIMO AutoLab", "manav193/NIMO-AUTOLAB", "Automation workflows for labs and computer environments."),
    NimoProject("nimo-knowledge", "NIMO Knowledge", "manav193/NIMO-KNOWLEDGE", "Structured knowledge foundation for NIMO."),
    NimoProject("prompt-aii", "Prompt-Aii", "257q1a0304-arch/Prompt-Aii", "Prompt generation and optimization product."),
)
