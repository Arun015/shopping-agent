from pydantic import BaseModel, Field
from typing import List, Optional


class CameraSpecs(BaseModel):
    main_mp: int
    ultrawide_mp: Optional[int] = None
    macro_mp: Optional[int] = None
    features: List[str] = []


class PhoneSpecs(BaseModel):
    camera: CameraSpecs
    battery_mah: int
    fast_charging_w: int
    processor: str
    ram_gb: int
    storage_gb: int
    display_inches: float
    refresh_rate_hz: int
    weight_g: int


class PhoneDTO(BaseModel):
    id: int
    brand: str
    model: str
    price: int
    specs: PhoneSpecs
    features: List[str]
    pros: List[str]
    cons: List[str]


class PhoneSearchRequest(BaseModel):
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    brand: Optional[str] = None
    features: Optional[List[str]] = None
    sort_by: str = "price"


class PhoneComparisonRequest(BaseModel):
    phone_ids: List[int] = Field(..., min_length=2, max_length=3)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    phones: Optional[List[PhoneDTO]] = None
    comparison: Optional[dict] = None
    session_id: str



