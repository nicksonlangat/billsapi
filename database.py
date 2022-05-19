import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("prod_string") 

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.transactions
user_database = client.users
transaction_collection = database.get_collection("transactions_collection")
user_collection = user_database.get_collection("users_collection")


# helpers
def transaction_helper(transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "device_id": transaction["device_id"],
        "phone_number": transaction["phone_number"],
        "meter_number": transaction["meter_number"],
        "amount": transaction["amount"],
        "transaction_date": transaction["transaction_date"]
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "device_id": user["device_id"],
        "number_string": user["number_string"],
        "date": user["date"]
    }


# Retrieve all transactions present in the database
async def retrieve_transactions():
    transactions = []
    async for transaction in transaction_collection.find():
        transactions.append(transaction_helper(transaction))
    return transactions


# Add a new transaction into to the database
async def add_transaction(transaction_data: dict) -> dict:
    transaction = await transaction_collection.insert_one(transaction_data)
    new_transaction = await transaction_collection.find_one({"_id": transaction.inserted_id})
    return transaction_helper(new_transaction)


# Retrieve a transaction with a matching ID
async def retrieve_transaction(id: str) -> dict:
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        return transaction_helper(transaction)


# Retrieve transactions for one user
async def retrieve_my_transactions(device_id: str) -> dict:
    transactions_list = []
    # transactions = 
    async for transaction in transaction_collection.find({"device_id": device_id}).sort([('transaction_date', -1)]):
        transactions_list.append(transaction_helper(transaction))
    return transactions_list


# Update a transaction with a matching ID
async def update_transaction(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        updated_transaction = await transaction_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            return True
        return False


# Delete a transaction from the database
async def delete_transaction(id: str):
    transaction = await transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        await transaction_collection.delete_one({"_id": ObjectId(id)})
        return True



# Retrieve all user_details present in the database
async def retrieve_details():
    details = []
    async for detail in user_collection.find():
        details.append(user_helper(detail))
    return details

# Add a new detail into the database
async def add_detail(user_data: dict) -> dict:
    detail = await user_collection.insert_one(user_data)
    new_detail = await user_collection.find_one({"_id": detail.inserted_id})
    return user_helper(new_detail)


# Retrieve details for one user
async def retrieve_my_details(device_id: str) -> dict:
    details_list = []
    async for detail in user_collection.find({"device_id": device_id}):
        details_list.append(user_helper(detail))
    return details_list


# Delete a detail from the database
async def delete_detail(id: str):
    detail = await user_collection.find_one({"_id": ObjectId(id)})
    if detail:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True