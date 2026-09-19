from integrations.nimo_core import NimoCoreClient

def test_core_endpoints():
    client = NimoCoreClient("https://example.test")
    assert client.health_endpoint() == "https://example.test/api/health"
