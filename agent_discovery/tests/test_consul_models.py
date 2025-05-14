import pytest
from pydantic import ValidationError

from agent_discovery.app.models.consul_models import (
    AddressValue,
    CheckConfig,
    ConsulServiceDefinition,
    DurationValue,
    HealthCheckResult,
    HealthServiceEntry,
    HealthStatus,
    PortValue,
    ServiceDeregistration,
    ServiceEntry,
)


# --- Fixtures for common values ---
@pytest.fixture
def address():
    return "127.0.0.1"


@pytest.fixture
def port():
    return 8080


@pytest.fixture
def agent_card_url(address, port):
    return f"http://{address}:{port}/.well-known/agent.json"


# --- HealthStatus enum tests ---
def test_health_status_valid():
    assert HealthStatus("passing") == HealthStatus.passing
    assert HealthStatus.warning.value == "warning"


def test_health_status_invalid():
    with pytest.raises(ValueError):
        HealthStatus("unknown")


# --- AgentServiceMeta tests ---
def test_agent_service_meta_success(agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    assert meta["agent_card_url"].startswith("http://")


# --- CheckConfig tests ---
def test_check_config_success():
    cfg = CheckConfig(
        HTTP="http://health",
        Interval=DurationValue("10s"),
        Timeout=DurationValue("5s"),
    )
    assert str(cfg.HTTP).startswith("http")


def test_check_config_missing_field():
    with pytest.raises(ValidationError):
        CheckConfig(HTTP="h", Interval=DurationValue("i"))  # Timeout missing


# --- ConsulServiceDefinition tests ---
def test_consul_service_definition_success(address, port, agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    svc = ConsulServiceDefinition(
        Name="svc",
        ID="svc1",
        Address=AddressValue(address),
        Port=PortValue(port),
        Meta=meta,
    )
    assert svc.Port.root == port
    assert svc.Tags == []


def test_consul_service_definition_port_bounds(address, agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    # too low
    with pytest.raises(ValidationError):
        ConsulServiceDefinition(
            Name="a",
            ID="b",
            Address=AddressValue(address),
            Port=PortValue(0),
            Meta=meta,
        )
    # too high
    with pytest.raises(ValidationError):
        ConsulServiceDefinition(
            Name="a",
            ID="b",
            Address=AddressValue(address),
            Port=PortValue(70000),
            Meta=meta,
        )


# --- ServiceDeregistration tests ---
def test_service_deregistration_success():
    obj = ServiceDeregistration(service_id="abc")
    assert obj.service_id == "abc"


def test_service_deregistration_missing():
    with pytest.raises(ValidationError):
        ServiceDeregistration()


# --- ServiceEntry tests ---
def test_service_entry_success(address, port, agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    entry = ServiceEntry(
        ID="e1",
        Service="svc",
        Address=AddressValue("host"),
        Port=PortValue(1234),
        Meta=meta,
    )
    assert entry.Service == "svc"


def test_service_entry_invalid_port(address, agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    with pytest.raises(ValidationError):
        ServiceEntry(
            ID="e1",
            Service="svc",
            Address=AddressValue("host"),
            Port=PortValue(-1),
            Meta=meta,
        )


# --- HealthCheckResult tests ---
def test_health_check_result_success():
    result = HealthCheckResult(
        CheckID="c1", Name="chk", Status=HealthStatus.critical, ServiceID="sid"
    )
    assert result.Status == HealthStatus.critical


def test_health_check_result_invalid_status():
    with pytest.raises(ValidationError):
        HealthCheckResult(CheckID="c1", Name="chk", Status="down", ServiceID="sid")


# --- HealthServiceEntry tests ---
def test_health_service_entry_success(agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    svc = ServiceEntry(
        ID="e2",
        Service="s",
        Address=AddressValue("a"),
        Port=PortValue(1),
        Meta=meta,
    )
    chk = HealthCheckResult(
        CheckID="c2", Name="c", Status=HealthStatus.passing, ServiceID="e2"
    )
    hse = HealthServiceEntry(
        AggregatedStatus=HealthStatus.passing, Service=svc, Checks=[chk]
    )
    assert hse.Checks[0].ServiceID == "e2"


def test_health_service_entry_empty_checks(agent_card_url):
    meta = {"agent_card_url": agent_card_url}
    svc = ServiceEntry(
        ID="e3",
        Service="s",
        Address=AddressValue("a"),
        Port=PortValue(1),
        Meta=meta,
    )
    # Business logic may allow empty list; assert attribute type
    hse = HealthServiceEntry(
        AggregatedStatus=HealthStatus.warning, Service=svc, Checks=[]
    )
    assert isinstance(hse.Checks, list)
