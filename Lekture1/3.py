from typing import List, Dict
from fastapi import APIRouter
from starlette.responses import JSONResponse

from Lekture1.hw.database import products_table, database
from Lekture1.hw.models import Product, ProductIn

router = APIRouter()


async def check_product(product_id: int):
    query = products_table.select().where(products_table.c.id == product_id, tags=["products"])
    return await database.fetch_one(query)


@router.get('/get_all_products/', response_model=List[Product], tags=["products"])
async def get_all_products():
    query = products_table.select()
    return await database.fetch_all(query)


@router.get('/get_product/{product_id}', response_model=Product | Dict, tags=["products"])
async def get_product(product_id: int):
    query = products_table.select().where(products_table.c.id == product_id)
    result = await database.fetch_one(query)
    if result:
        return result
    return JSONResponse(status_code=404, content={'error': 'Product Not Found'})


@router.post('/add_product/', response_model=Product, tags=["products"])
async def add_product(product: ProductIn):
    query = products_table.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@router.put('/update_product/{product_id}', response_model=Product, tags=["products"])
async def update_product(new_product: ProductIn, product_id: int):
    if not check_product(product_id):
        return JSONResponse(status_code=404, content={'error': 'Product Not Found'})
    query = products_table.update().where(products_table.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete('/delete_product/{product_id}', tags=["products"])
async def delete_product(product_id: int):
    if not check_product(product_id):
        return JSONResponse(status_code=404, content={'error': 'Product Not Found'})
    query = products_table.delete().where(products_table.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted"}