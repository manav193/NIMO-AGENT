import re
from dataclasses import dataclass

_PLUGIN_RE = re.compile(r"(?<!\w)@([a-zA-Z0-9_-]+)")

@dataclass(frozen=True)
class PluginInvocation:
    provider: str
    task: str

def parse_plugin_invocations(text: str) -> list[PluginInvocation]:
    matches = list(_PLUGIN_RE.finditer(text))
    if not matches:
        return []
    result: list[PluginInvocation] = []
    for index, match in enumerate(matches):
        task_start = match.end()
        task_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        task = text[task_start:task_end].strip()
        if task:
            result.append(PluginInvocation(match.group(1).lower(), task))
    return result
