from knowledge.connector import KnowledgeConnector
def test_knowledge_rejects_unsanitized():
    class S:
        def search(self,q,limit): return [{"sanitized":False,"status":"active"},{"sanitized":True,"status":"approved","id":"2"}]
    assert [x["id"] for x in KnowledgeConnector(S()).search("x")] == ["2"]
def test_memory_context_bounded():
    from memory.context import MemoryContext
    class H: record_id="1"; text="abc"
    assert "memory:1" in MemoryContext().build([H()])
