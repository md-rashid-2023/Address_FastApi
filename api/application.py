from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(bind=engine)


import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("applications.log"),
        logging.StreamHandler()
    ]
)

# Create a logger
logger = logging.getLogger(__name__)



def get_db():

    """
    Function to get a database session.

    Returns:
        Generator: A generator yielding the database session.
    """

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):

    """
    Address model class.
    """

    street :str = Field(min_length=1)
    city : str = Field(min_length=1, max_length=100)
    latitude : float 
    longitude : float




@app.get("/address")
def list_address(db: Session = Depends(get_db)):

    """
    Get all addresses.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list: A list of all addresses.
    """
    logger.info("Listing all addresses...")

    return db.query(models.Address).all()




@app.get("/search/{street}")
def filter_address(street: str, db: Session = Depends(get_db)):

    """
    Filter addresses by street.

    Args:
        street (str): The street to search for.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list: A list of filtered addresses.
    """
    
    addresses = db.query(models.Address).filter(models.Address.street.ilike(f"%{street}%"))
    results = addresses.all()

    logger.info(f"Filtering addresses by street: {street}")

    return results


@app.post("/address")
def create_address(address: Address, db: Session = Depends(get_db)):

    """
    Create a new address.

    Args:
        address (Address): The address details.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Address: The created address.
    """

    address_model = models.Address()
    address_model.street = address.street
    address_model.city = address.city
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude

    db.add(address_model)
    db.commit()

    logger.info("Creating a new address")
    
    return address

@app.put("/address/{address_id}")
def update_address(address_id: int, address: Address, db: Session = Depends(get_db)):

    """
    Update an address by ID.

    Args:
        address_id (int): The ID of the address to update.
        address (Address): The updated address details.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A message indicating the success of the update.
    """
    
    address_model = db.query(models.Address).filter(models.Address.id == address_id).first()

    if address_model is None:
    
        raise HTTPException(
            status_code=404,
            detail="ID Does Not Exists!"
        )
    
    address_model.street = address.street
    address_model.city = address.city
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude

    db.add(address_model)
    db.commit()

    logger.info(f"Updating address with ID: {address_id}")

    return { 'message' : 'Address sucessfully updated' }


@app.delete("/address/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):

    """
    Delete an address by ID.

    Args:
        address_id (int): The ID of the address to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the address ID does not exist.

    Returns:
        dict: A message indicating the success of the delete operation.
    """

    address_model = db.query(models.Address).filter(models.Address.id==address_id).first()

    if address_model is None:

        raise HTTPException(
            status_code=404,
            detail="ID does not exists"
        )
    
    db.query(models.Address).filter(models.Address.id == address_id).delete()
    db.commit()
    logger.info(f"Deleting address with ID: {address_id}")