from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from agents.common.types import (
    AgentAuthentication,
    AgentCapabilities,
    AgentProvider,
    AgentSkill,
)


class HealthStatus(str, Enum):
    passing = "passing"
    warning = "warning"
    critical = "critical"
    maintenance = "maintenance"


class AgentServiceMeta(BaseModel):
    provider: AgentProvider = Field(...)
    modalities: List[str] = Field(default_factory=list)
    version: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    documentation_url: Optional[str] = Field(None)
    capabilities: AgentCapabilities = Field(...)
    authentication: Optional[AgentAuthentication] = Field(None)
    default_input_modes: List[str] = Field(default_factory=list)
    default_output_modes: List[str] = Field(default_factory=list)
    skills: List[AgentSkill] = Field(default_factory=list)


class AddressValue(BaseModel):
    value: str = Field(..., min_length=1, max_length=255)


class PortValue(BaseModel):
    value: int = Field(..., ge=1, le=65535)


class DurationValue(BaseModel):
    value: str = Field(..., pattern=r"^\d+(ms|s|m|h)$")


class CheckConfig(BaseModel):
    HTTP: HttpUrl = Field(...)
    Interval: DurationValue = Field(...)
    Timeout: DurationValue = Field(...)


class ConsulServiceDefinition(BaseModel):
    Name: str = Field(...)
    ID: str = Field(...)
    Address: AddressValue = Field(...)
    Port: PortValue = Field(...)
    Tags: List[str] = Field(default_factory=list)
    Meta: AgentServiceMeta = Field(...)
    Check: Optional[CheckConfig] = Field(None)


class ServiceDeregistration(BaseModel):
    service_id: str = Field(...)


class ServiceEntry(BaseModel):
    ID: str = Field(...)
    Service: str = Field(...)
    Address: AddressValue = Field(...)
    Port: PortValue = Field(...)
    Tags: List[str] = Field(default_factory=list)
    Meta: AgentServiceMeta = Field(...)


class HealthCheckResult(BaseModel):
    CheckID: str = Field(...)
    Name: str = Field(...)
    Status: HealthStatus = Field(...)
    Output: Optional[str] = Field(None)
    ServiceID: str = Field(...)


class HealthServiceEntry(BaseModel):
    AggregatedStatus: HealthStatus = Field(...)
    Service: ServiceEntry = Field(...)
    Checks: List[HealthCheckResult] = Field(...)
