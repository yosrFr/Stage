from sqlalchemy.orm import joinedload

from models.customer import Customer

def create_many_customers(db, data: list[dict]):
    many_customers = [Customer(**item) for item in data]

    try:
        db.add_all(many_customers)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    for customer in many_customers:
        db.refresh(customer)

    return many_customers
