from abc import ABC
from typing import Optional, Type

import pydantic


class AbstractAds(pydantic.BaseModel, ABC):
    title: str
    description: str
    owner: str

    @pydantic.field_validator("title")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Maxima length of title is 100")
        return v

    @pydantic.field_validator("description")
    @classmethod
    def description_length(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError("Maxima length of description is 200")
        return v


    @pydantic.field_validator("owner")
    @classmethod
    def owner_length(cls, v: str) -> str:
        if len(v) > 50:
            raise ValueError(f"Maxima length of owner is 50")
        return v


class CreateAds(AbstractAds):
    title: str
    description: str
    owner: str


class UpdateAds(AbstractAds):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None


SCHEMA_CLASS = Type[CreateAds | UpdateAds]
SCHEMA = CreateAds | UpdateAds
