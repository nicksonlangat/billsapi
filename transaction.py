from typing import Optional

from pydantic import BaseModel, Field

from datetime import datetime


class TransactionSchema(BaseModel):
    device_id: str = Field(...)
    phone_number: str = Field(...)
    meter_number: str = Field(...)
    amount: float = Field(...)
    transaction_date: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "device_id":"9cf2-6481-fca-88f1",
                "phone_number": "0722345641",
                "meter_number": "34547654210",
                "amount": "100.00",
            }
        }


class UpdateTransactionModel(BaseModel):
    phone_number: Optional[str]
    meter_number: Optional[str]
    amount: Optional[float]
    phone_number: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "device_id":"9cf2-6481-fca-88f1",
                "phone_number": "0722345641",
                "meter_number": "34547654210",
                "amount": "100.00",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}