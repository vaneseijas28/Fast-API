from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


db = {}  # Almacenamiento en memoria

class Item(BaseModel):
    id: str
    data: dict

@app.post("/json/", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id in db:
        raise HTTPException(status_code=409, detail="El ID ya existe")
    db[item.id] = item.dict()
    return item

@app.get("/json/{item_id}")
async def read_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="JSON no encontrado")
    return db[item_id]

@app.put("/json/{item_id}")
async def update_item(item_id: str, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="JSON no encontrado")
    db[item_id] = item.dict()
    return item

@app.delete("/json/{item_id}")
async def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="JSON no encontrado")
    del db[item_id]
    return {"message": "JSON eliminado", "id": item_id}