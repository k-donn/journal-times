"""Store all of the types associated with Day One entries."""

from typing import TypedDict, List, Dict, Union, Tuple


class WeatherProps(TypedDict):
    """Represents weather data for an entry."""

    sunsetDate: str
    weatherCode: str
    weatherServiceName: str
    temperatureCelsius: int
    windBearing: int
    sunriseDate: str
    conditionsDescription: str
    pressureMB: int
    moonPhase: int
    visibilityKM: float
    relativeHumidity: int
    windSpeedKPH: float
    windChillCelsius: int


class Coordinates(TypedDict):
    """Day One coordinates description."""

    longitude: float
    latitude: float


class RegionProps(TypedDict):
    """Day One location region description."""

    center: Coordinates
    identifier: str
    radius: float


class LocationProps(TypedDict):
    """Day One location properties."""

    localityName: str
    country: str
    timeZoneName: str
    administrativeArea: str
    longitude: float
    placeName: str
    latitude: float


class Entry(TypedDict):
    """Properties of a JSON entry."""

    richText: str
    starred: bool
    duration: int
    weather: WeatherProps
    creationDeviceType: str
    uuid: str
    creationDate: str
    creationOSName: str
    creationOSVersion: str
    modifiedDate: str
    text: str
    creationDeviceModel: str
    creationDevice: str
    location: LocationProps
    timeZone: str
    tags: List[str]


class MetadataProps(TypedDict):
    """Day One export metadata info."""

    version: str


class Export(TypedDict):
    """Structure of an exported journal."""

    metadata: MetadataProps
    entries: List[Entry]


# Mapping of tag names to unique colors
ColorMap = Dict[str, Tuple[float, float, float, float]]

# Represents a point's color and x & y values
PointColorVal = Dict[str, Union[str, float]]
