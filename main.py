from fastapi import FastAPI, HTTPException
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select

app = FastAPI()

class MenuItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class Sale(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    quantity: int
    total_bill: float

class OrderRequest(SQLModel):
    name: str
    quantity: int = Field(gt=0)

class RestockRequest(SQLModel):
    name: str
    amount_to_add: int = Field(gt=0)

sqlite_file_name = "CafeDatabase.db" 
sqlite_url = f"sqlite:///{sqlite_file_name}" 

engine = create_engine(sqlite_url, echo=True) 
SQLModel.metadata.create_all(engine)

#========================================================================================
@app.get("/menu")
def show_menu():
    with Session(engine) as session:
        statement = select(MenuItem)
        item = session.exec(statement).all()
        return item
#========================================================================================
@app.get("/sale")
def show_sale():
    with Session(engine) as session:
        statement =  select(Sale)
        item = session.exec(statement).all()
        return item
#========================================================================================
@app.post("/menu", status_code=201)
def add_item(new_item: MenuItem):

    with Session(engine) as session:
        statement = select(MenuItem).where(MenuItem.name == new_item.name)
        item = session.exec(statement).first()

        if item:
                raise HTTPException(status_code=409, detail=f"'{new_item.name}' is already on the menu!")

        session.add(new_item)
        session.commit()
        session.refresh(new_item)

        return {
        "message": "New item successfully added",
        "item": new_item
        }

#========================================================================================
@app.post("/order", status_code=201)
def order_item(order_item: OrderRequest):
    with Session(engine) as session:
        statement = select(MenuItem).where(MenuItem.name == order_item.name)
        item = session.exec(statement).first() 
        if not item:
            raise HTTPException(status_code=404, detail=f"'{order_item.name}' was not in the menu!")
        if order_item.quantity > item.stock:
            raise HTTPException(status_code=400, detail=f"Exceeds available stock. Available stock: {item.stock}")
        item.stock -= order_item.quantity
        total_price = item.price * order_item.quantity
        new_sale = Sale(
            item_name=item.name,
            quantity=order_item.quantity,
            total_bill=total_price
        )
        session.add(new_sale)
        session.commit()
        return {
            "message": "Order was successful",
            "item": item.name
        }
#========================================================================================
@app.delete("/menu/{item_name}")
def delete_item(item_name: str):
    with Session(engine) as session:
        statement = select(MenuItem).where(MenuItem.name == item_name)
        item = session.exec(statement).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"'{item_name}' is not on the menu!")
        session.delete(item)
        session.commit()
        return {
            "message": "Item was deleted",
            "item": item_name
            }
#========================================================================================
@app.patch("/menu/restock")
def restock_item(restock_item: RestockRequest):
    with Session(engine) as session:
        statement = select(MenuItem).where(MenuItem.name == restock_item.name)
        item = session.exec(statement).first()

        if not item:
            raise HTTPException(status_code=404, detail=f"'{restock_item.name}' is not in the menu!")

        item.stock += restock_item.amount_to_add
        session.commit()
        return {
            "message": "Item was restocked",
            "item_quantity_added": restock_item.amount_to_add
            }
   
#========================================================================================