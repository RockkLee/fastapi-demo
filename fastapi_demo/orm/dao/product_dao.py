from fastapi_demo.orm.connection import Session
from fastapi_demo.orm.models.product import Product


def add_streamer(session: Session, product: Product):
    session.add(product)