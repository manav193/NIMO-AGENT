from integrations.plugin_router import parse_plugin_invocations


def test_single_plugin_invocation():
    items = parse_plugin_invocations("@gmail summarize unread mail")
    assert items == [type(items[0])("gmail", "summarize unread mail")]

def test_multiple_plugin_invocations():
    items = parse_plugin_invocations("@gmail find mail @calendar schedule follow-up")
    assert [(x.provider, x.task) for x in items] == [
        ("gmail", "find mail"),
        ("calendar", "schedule follow-up"),
    ]

def test_plain_text_has_no_plugin():
    assert parse_plugin_invocations("hello NIMO") == []
