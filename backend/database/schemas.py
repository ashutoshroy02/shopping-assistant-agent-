import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseSchema):
    id: uuid.UUID
    name: str
    email: str
    role: str
    preferences: dict[str, Any]
    created_at: datetime


class UserUpdate(BaseModel):
    name: str | None = None
    preferences: dict[str, Any] | None = None


# Auth schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


# Product schemas
class ProductBase(BaseModel):
    title: str = Field(..., max_length=500)
    description: str | None = None
    price: float = Field(..., gt=0)
    original_price: float | None = None
    rating: float | None = Field(None, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    category: str = Field(..., max_length=100)
    brand: str = Field(..., max_length=100)
    specifications: dict[str, Any] = {}
    images: list[str] = []
    availability: bool = True
    source_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: uuid.UUID
    created_at: datetime


# Review schemas
class ReviewBase(BaseModel):
    review_text: str
    rating: float | None = Field(None, ge=1, le=5)
    sentiment_score: float | None = Field(None, ge=-1, le=1)
    metadata_: dict[str, Any] = Field(default={}, alias="metadata")
    source: str | None = None


class ReviewCreate(ReviewBase):
    product_id: uuid.UUID


class ReviewResponse(ReviewBase):
    id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


# Recommendation schemas
class RecommendationBase(BaseModel):
    score: float = Field(..., ge=0, le=1)
    reasoning: str | None = None
    metadata_: dict[str, Any] = Field(default={}, alias="metadata")


class RecommendationCreate(RecommendationBase):
    user_id: uuid.UUID
    product_id: uuid.UUID


class RecommendationResponse(RecommendationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


# Price History schemas
class PriceHistoryBase(BaseModel):
    price: float = Field(..., gt=0)
    source: str = Field(..., max_length=100)


class PriceHistoryCreate(PriceHistoryBase):
    product_id: uuid.UUID


class PriceHistoryResponse(PriceHistoryBase):
    id: uuid.UUID
    product_id: uuid.UUID
    recorded_at: datetime


# Chat schemas
class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    metadata_: dict[str, Any] = Field(default={}, alias="metadata")

    class Config:
        populate_by_name = True


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: uuid.UUID | None = None
    context: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: uuid.UUID
    products: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}


class ChatSessionResponse(BaseSchema):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str | None
    messages: list[ChatMessage] = []
    created_at: datetime
    updated_at: datetime


# Recommendation request schemas
class RecommendRequest(BaseModel):
    category: str
    budget: dict[str, float] | None = None
    preferences: dict[str, Any] | None = None
    limit: int = Field(default=10, ge=1, le=50)


class RecommendResponse(BaseModel):
    recommendations: list[dict[str, Any]]
    categories: dict[str, str]


# Comparison schemas
class CompareRequest(BaseModel):
    product_ids: list[uuid.UUID] = Field(..., min_length=2, max_length=5)


class CompareResponse(BaseModel):
    comparison: dict[str, Any]


# Price Tracking schemas
class PriceTrackingCreate(BaseModel):
    product_id: uuid.UUID
    target_price: float = Field(..., gt=0)
    alert_on_drop: bool = True


class PriceTrackingResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    product_id: uuid.UUID
    target_price: float
    current_price: float | None = None
    status: str
    created_at: datetime


# Price History request
class PriceHistoryRequest(BaseModel):
    period: str = Field(default="30d", pattern="^(7d|30d|90d|1y)$")
    source: str = Field(default="all")


class PriceHistoryResponse(BaseModel):
    product_id: uuid.UUID
    history: list[dict[str, Any]]
    statistics: dict[str, Any]
    prediction: dict[str, Any] | None = None


# Autonomous Research schemas
class AutonomousResearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    options: dict[str, Any] | None = None


class AutonomousResearchResponse(BaseModel):
    research_id: uuid.UUID
    status: str
    report: dict[str, Any]
    metadata: dict[str, Any]


# Analytics schemas
class AnalyticsResponse(BaseModel):
    user_analytics: dict[str, Any]
    platform_analytics: dict[str, Any]


# Error schemas
class ErrorResponse(BaseModel):
    error: dict[str, Any]
