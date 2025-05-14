from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, HttpUrl, RootModel


class HealthStatus(str, Enum):
    passing = "passing"
    warning = "warning"
    critical = "critical"
    maintenance = "maintenance"


class AddressValue(RootModel[Annotated[str, Field(min_length=1, max_length=255)]]):
    pass


class PortValue(RootModel[Annotated[int, Field(ge=1, le=65535)]]):
    pass


class DurationValue(RootModel[Annotated[str, Field(pattern=r"^\d+(ms|s|m|h)$")]]):
    pass


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
    Meta: dict[str, str] = Field(...)
    Check: Optional[CheckConfig] = Field(None)


class ServiceDeregistration(BaseModel):
    service_id: str = Field(...)


class ServiceEntry(BaseModel):
    ID: str = Field(...)
    Service: str = Field(...)
    Address: AddressValue = Field(...)
    Port: PortValue = Field(...)
    Tags: List[str] = Field(default_factory=list)
    Meta: dict[str, str] = Field(...)


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
