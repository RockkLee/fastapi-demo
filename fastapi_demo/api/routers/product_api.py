from fastapi import APIRouter, Depends, status, HTTPException, Response


router = APIRouter(
    prefix="/product",
    tags=['product_api']
)