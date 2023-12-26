from sqlalchemy.orm import Session

import schemas
from models import Category, Item, User


# Category
def create_custom_category(db: Session, schema: schemas.CategoryCreate):
    db_category = Category(**schema.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_custom_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def get_custom_category(db: Session, category_id: int):
    return db.query(Category).filter_by(id=category_id).first()


def update_custom_category(db: Session, category_id: int, category_data: schemas.CategoryUpdate | dict):
    db_category = db.query(Category).filter_by(id=category_id).first()

    category_data = category_data if isinstance(category_data, dict) else category_data.model_dump()

    if db_category:
        for key, value in category_data.items():
            if hasattr(db_category, key):
                setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)

    return db_category


def delete_custom_category(db: Session, category_id: int):
    db_category = db.query(Category).filter_by(id=category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# Item
def create_custom_item(db: Session, schema: schemas.ItemCreate):
    db_item = Item(**schema.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_custom_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def get_custom_item(db: Session, item_id: int):
    return db.query(Item).filter_by(id=item_id).first()


def update_custom_item(db: Session, item_id: int, item_data: schemas.ItemUpdate | dict):
    db_item = db.query(Item).filter_by(id=item_id).first()

    item_data = item_data if isinstance(item_data, dict) else item_data.model_dump()

    if db_item:
        for key, value in item_data.items():
            if hasattr(db_item, key):
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    return None


def delete_custom_item(db: Session, item_id: int):
    db_item = db.query(Item).filter_by(id=item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# User
def create_custom_user(db: Session, user_data: schemas.UserCreate):
    db_user = User(**user_data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_custom_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_custom_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).first()


def update_custom_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = db.query(User).filter_by(id=user_id).first()

    user_data = user_data.model_dump()

    if db_user:
        for key, value in user_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_custom_user(db: Session, user_id: int):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
