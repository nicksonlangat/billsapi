from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database import (
    add_transaction,
    retrieve_my_transactions,
    retrieve_transactions,
    retrieve_transaction,
    update_transaction,
    delete_transaction,
    add_detail,
    retrieve_details,
    retrieve_my_details,
    delete_detail
)
from transaction import (
    ErrorResponseModel,
    ResponseModel,
    TransactionSchema,
    UpdateTransactionModel,
)
from user import UserSchema

router = APIRouter()

@router.post("/", response_description="Transaction data added into the database")
async def add_transaction_data(transaction: TransactionSchema = Body(...)):
    transaction = jsonable_encoder(transaction)
    new_transaction = await add_transaction(transaction)
    return ResponseModel(new_transaction, "Transaction added successfully.")


@router.get("/", response_description="Transactions retrieved")
async def get_transactions():
    transactions = await retrieve_transactions()
    if transactions:
        return ResponseModel(transactions, "Transactions data retrieved successfully")
    return ResponseModel(transactions, "Empty list returned")


@router.get("/{id}", response_description="Transaction data retrieved")
async def get_transaction_data(id):
    transaction = await retrieve_transaction(id)
    if transaction:
        return ResponseModel(transaction, "Transaction data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Transaction doesn't exist.")


@router.get("/{device_id}/user", response_description="Transactions data retrieved")
async def get_user_transaction_data(device_id):
    transactions = await retrieve_my_transactions(device_id)
    if transactions:
        return ResponseModel(transactions, "Transactions data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Fetch failed")


@router.put("/{id}")
async def update_transaction_data(id: str, req: UpdateTransactionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_transaction = await update_transaction(id, req)
    if updated_transaction:
        return ResponseModel(
            "Transaction with ID: {}  updated successful".format(id),
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the transaction data.",
    )


@router.delete("/{id}", response_description="Transaction data deleted from the database")
async def delete_transaction_data(id: str):
    deleted_transaction = await delete_transaction(id)
    if deleted_transaction:
        return ResponseModel(
            "Transaction with ID: {} removed".format(id), "Transaction deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "TTransaction with id {0} doesn't exist".format(id)
    )


@router.post("/details/", response_description="Detail data added into the database")
async def add_detail_data(detail: UserSchema = Body(...)):
    detail = jsonable_encoder(detail)
    new_detail = await add_detail(detail)
    return ResponseModel(new_detail, "Detail added successfully.")


@router.get("/details", response_description="Details retrieved")
async def get_details():
    details = await retrieve_details()
    if details:
        return ResponseModel(details, "Data retrieved successfully")
    return ResponseModel(details, "Empty list returned")


@router.get("/{device_id}/user/details", response_description="Data retrieved")
async def get_my_details(device_id):
    details = await retrieve_my_details(device_id)
    if details:
        return ResponseModel(details, "Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Fetch failed")


@router.delete("/details/{id}", response_description="Data deleted from the database")
async def delete_a_detail(id: str):
    detail = await delete_detail(id)
    if detail:
        return ResponseModel(
            "Detail with ID: {} removed".format(id), " deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Detail with id {0} doesn't exist".format(id)
    )