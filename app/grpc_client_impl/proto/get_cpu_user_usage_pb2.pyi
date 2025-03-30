from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetCpuUserUsageRequest(_message.Message):
    __slots__ = ("date_from", "date_to")
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    date_from: int
    date_to: int
    def __init__(self, date_from: _Optional[int] = ..., date_to: _Optional[int] = ...) -> None: ...

class CpuUsage(_message.Message):
    __slots__ = ("cpu", "avg_usage", "max_usage", "min_usage")
    CPU_FIELD_NUMBER: _ClassVar[int]
    AVG_USAGE_FIELD_NUMBER: _ClassVar[int]
    MAX_USAGE_FIELD_NUMBER: _ClassVar[int]
    MIN_USAGE_FIELD_NUMBER: _ClassVar[int]
    cpu: str
    avg_usage: float
    max_usage: float
    min_usage: float
    def __init__(self, cpu: _Optional[str] = ..., avg_usage: _Optional[float] = ..., max_usage: _Optional[float] = ..., min_usage: _Optional[float] = ...) -> None: ...

class GetCpuUserUsageResponse(_message.Message):
    __slots__ = ("usages",)
    USAGES_FIELD_NUMBER: _ClassVar[int]
    usages: _containers.RepeatedCompositeFieldContainer[CpuUsage]
    def __init__(self, usages: _Optional[_Iterable[_Union[CpuUsage, _Mapping]]] = ...) -> None: ...
