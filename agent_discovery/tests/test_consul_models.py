import pytest
from pydantic import ValidationError

from agent_discovery.app.models.consul_models import (
    AddressValue,
    AgentServiceMeta,
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
from agents.common.types import (
    AgentAuthentication,
    AgentCapabilities,
    AgentProvider,
    AgentSkill,
)


# --- Fixtures for nested models ---
@pytest.fixture
def valid_provider():
    return AgentProvider(organization="TestOrg", url="https://api.test.org")


@pytest.fixture
def valid_capabilities():
    return AgentCapabilities(
        streaming=True, pushNotifications=False, stateTransitionHistory=True
    )


@pytest.fixture
def valid_authentication():
    return AgentAuthentication(schemes=["basic"], credentials="secret")


@pytest.fixture
def valid_skill():
    return AgentSkill(
        id="skill1", name="Skill One", description="A test skill", tags=["a", "b"]
    )


# --- HealthStatus enum tests ---
def test_health_status_valid():
    assert HealthStatus("passing") == HealthStatus.passing
    assert HealthStatus.warning.value == "warning"


def test_health_status_invalid():
    with pytest.raises(ValueError):
        HealthStatus("unknown")


# --- AgentServiceMeta tests ---
def test_agent_service_meta_success(
    valid_provider, valid_capabilities, valid_authentication, valid_skill
):
    meta = AgentServiceMeta(
        provider=valid_provider,
        capabilities=valid_capabilities,
        authentication=valid_authentication,
        modalities=["m1", "m2"],
        version="1.0",
        description="desc",
        documentation_url="http://doc",
        default_input_modes=["in"],
        default_output_modes=["out"],
        skills=[valid_skill],
    )
    assert meta.provider.organization == "TestOrg"
    assert isinstance(meta.modalities, list) and meta.modalities == ["m1", "m2"]


def test_agent_service_meta_missing_required(valid_provider):
    # capabilities is required
    with pytest.raises(ValidationError):
        AgentServiceMeta(provider=valid_provider)


# --- CheckConfig tests ---
def test_check_config_success():
    cfg = CheckConfig(
        HTTP="http://health",
        Interval=DurationValue(value="10s"),
        Timeout=DurationValue(value="5s"),
    )
    assert str(cfg.HTTP).startswith("http")


def test_check_config_missing_field():
    with pytest.raises(ValidationError):
        CheckConfig(HTTP="h", Interval=DurationValue(value="i"))  # Timeout missing


# --- ConsulServiceDefinition tests ---
def test_consul_service_definition_success(
    valid_provider, valid_capabilities, valid_authentication, valid_skill
):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    svc = ConsulServiceDefinition(
        Name="svc",
        ID="svc1",
        Address=AddressValue(value="127.0.0.1"),
        Port=PortValue(value=8080),
        Meta=meta,
    )
    assert svc.Port.value == 8080
    assert svc.Tags == []


def test_consul_service_definition_port_bounds(valid_provider, valid_capabilities):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    # too low
    with pytest.raises(ValidationError):
        ConsulServiceDefinition(
            Name="a", ID="b", Address=AddressValue(value="x"), Port=0, Meta=meta
        )
    # too high
    with pytest.raises(ValidationError):
        ConsulServiceDefinition(
            Name="a", ID="b", Address=AddressValue(value="x"), Port=70000, Meta=meta
        )


# --- ServiceDeregistration tests ---
def test_service_deregistration_success():
    obj = ServiceDeregistration(service_id="abc")
    assert obj.service_id == "abc"


def test_service_deregistration_missing():
    with pytest.raises(ValidationError):
        ServiceDeregistration()


# --- ServiceEntry tests ---
def test_service_entry_success(valid_provider, valid_capabilities):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    entry = ServiceEntry(
        ID="e1",
        Service="svc",
        Address=AddressValue(value="host"),
        Port=PortValue(value=1234),
        Meta=meta,
    )
    assert entry.Service == "svc"


def test_service_entry_invalid_port(valid_provider, valid_capabilities):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    with pytest.raises(ValidationError):
        ServiceEntry(
            ID="e1",
            Service="svc",
            Address=AddressValue(value="host"),
            Port=-1,
            Meta=meta,
        )


# --- HealthCheckResult tests ---
def test_health_check_result_success(valid_provider, valid_capabilities):
    result = HealthCheckResult(
        CheckID="c1", Name="chk", Status=HealthStatus.critical, ServiceID="sid"
    )
    assert result.Status == HealthStatus.critical


def test_health_check_result_invalid_status():
    with pytest.raises(ValidationError):
        HealthCheckResult(CheckID="c1", Name="chk", Status="down", ServiceID="sid")


# --- HealthServiceEntry tests ---
def test_health_service_entry_success(valid_provider, valid_capabilities):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    svc = ServiceEntry(
        ID="e2",
        Service="s",
        Address=AddressValue(value="a"),
        Port=PortValue(value=1),
        Meta=meta,
    )
    chk = HealthCheckResult(
        CheckID="c2", Name="c", Status=HealthStatus.passing, ServiceID="e2"
    )
    hse = HealthServiceEntry(
        AggregatedStatus=HealthStatus.passing, Service=svc, Checks=[chk]
    )
    assert hse.Checks[0].ServiceID == "e2"


def test_health_service_entry_empty_checks(valid_provider, valid_capabilities):
    meta = AgentServiceMeta(provider=valid_provider, capabilities=valid_capabilities)
    svc = ServiceEntry(
        ID="e3",
        Service="s",
        Address=AddressValue(value="a"),
        Port=PortValue(value=1),
        Meta=meta,
    )
    # Business logic may allow empty list; assert attribute type
    hse = HealthServiceEntry(
        AggregatedStatus=HealthStatus.warning, Service=svc, Checks=[]
    )
    assert isinstance(hse.Checks, list)
