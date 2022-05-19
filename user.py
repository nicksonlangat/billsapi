from typing import Optional

from pydantic import BaseModel, Field

from datetime import datetime


class UserSchema(BaseModel):
    device_id: str = Field(...)
    number_string: str = Field(...)
    date: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "device_id":"9cf2-6481-fca-88f1",
                "number_string": "0722345641",
            }
        }