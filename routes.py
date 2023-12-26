from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_custom_category, get_custom_categories, get_custom_category, update_custom_category, delete_custom_category,
    create_custom_item, get_custom_items, get_custom_item, update_custom_item, delete_custom_item,
    create_custom_user, get_custom_users, get_custom_user, update_custom_user, delete_custom_user
)

router_websocket = APIRouter()
router_custom_categories = APIRouter(prefix='/custom_categories', tags=['custom_category'])
router_custom_items = APIRouter(prefix='/custom_items', tags=['custom_item'])
router_custom_users = APIRouter(prefix='/custom_users', tags=['custom_user'])


# WebSocket
class CustomConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = CustomConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


# Custom Categories
@router_custom_categories.post("/", response_model=schemas.Category)
async def create_custom_category_route(category_data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = create_custom_category(db, category_data)
    await notify_clients(f"Custom Category added: {category.name}")
    return category


@router_custom_categories.get("/", response_model=List[schemas.Category])
async def read_custom_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = get_custom_categories(db, skip=skip, limit=limit)
    return categories


@router_custom_categories.get("/{category_id}", response_model=schemas.Category)
async def read_custom_category(category_id: int, db: Session = Depends(get_db)):
    category = get_custom_category(db, category_id)
    return category


@router_custom_categories.patch("/{category_id}", response_model=schemas.Category)
async def update_custom_category_route(category_id: int, category_data: schemas.CategoryUpdate,
                                       db: Session = Depends(get_db)):
    updated_category = update_custom_category(db, category_id, category_data)
    if updated_category:
        await notify_clients(f"Custom Category updated: {updated_category.name}")
        return updated_category
    return {"message": "Custom Category not found"}


@router_custom_categories.delete("/{category_id}")
async def delete_custom_category_route(category_id: int, db: Session = Depends(get_db)):
    deleted = delete_custom_category(db, category_id)
    if deleted:
        await notify_clients(f"Custom Category deleted: ID {category_id}")
        return {"message": "Custom Category deleted"}
    return {"message": "Custom Category not found"}


# Custom Items
@router_custom_items.post("/", response_model=schemas.Item)
async def create_custom_item_route(schema: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = create_custom_item(db, schema)
    await notify_clients(f"Custom Item added: {item.name}")
    return item


@router_custom_items.get("/", response_model=List[schemas.Item])
async def read_custom_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = get_custom_items(db, skip=skip, limit=limit)
    return items


@router_custom_items.get("/{item_id}", response_model=schemas.Item)
async def read_custom_item(item_id: int, db: Session = Depends(get_db)):
    item = get_custom_item(db, item_id)
    return item


@router_custom_items.patch("/{item_id}")
async def update_custom_item_route(item_id: int, schema: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated_item = update_custom_item(db, item_id, schema)
    if updated_item:
        await notify_clients(f"Custom Item updated: {updated_item.name}")
        return updated_item
    return {"message": "Custom Item not found"}


@router_custom_items.delete("/{item_id}")
async def delete_custom_item_route(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_custom_item(db, item_id)
    if deleted:
        await notify_clients(f"Custom Item deleted: ID {item_id}")
        return {"message": "Custom Item deleted"}
    return {"message": "Custom Item not found"}


# Custom Users
@router_custom_users.post("/", response_model=schemas.User)
async def create_custom_user_route(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = create_custom_user(db, user_data)
    return user


@router_custom_users.get("/", response_model=List[schemas.User])
async def read_custom_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_custom_users(db, skip=skip, limit=limit)
    return users


@router_custom_users.get("/{user_id}", response_model=schemas.User)
async def read_custom_user(user_id: int, db: Session = Depends(get_db)):
    user = get_custom_user(db, user_id)
    return user


@router_custom_users.put("/{user_id}", response_model=schemas.User)
async def update_custom_user_route(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_custom_user(db, user_id, user_data)
    return updated_user


@router_custom_users.delete("/{user_id}")
async def delete_custom_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_custom_user(db, user_id)
    if deleted:
        return {"message": "Custom User deleted"}
    return {"message": "Custom User not found"}
