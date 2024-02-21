from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from pymongo import ReturnDocument

from app.db.models.restaurants.restaurants_models import RestaurantCollection, RestaurantCreate, RestaurantUpdate

from app.database import restaurant_collection
from app.db.models.restaurants.restaurants_models import RestaurantBase

router = APIRouter(
    tags=['public']
)


@router.get(
    "",
    response_description="List all restaurants",
    response_model=RestaurantCollection,
    response_model_by_alias=False,
)
async def get_restaurants():
    return RestaurantCollection(restaurants=await restaurant_collection.find().to_list(100))

@router.get(
    "/{restaurant_id}", 
    response_description="Get single restaurant",
    response_model=RestaurantBase,    
    response_model_by_alias=False,
)
async def get_single_restaurant(restaurant_id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        restaurant := await restaurant_collection.find_one({"_id": ObjectId(restaurant_id)})
    ) is not None:
        return restaurant

    raise HTTPException(status_code=404, detail=f"restaurant {restaurant_id} is not found")

@router.post(
    "",
    response_description="Add new restaurant",
    response_model=RestaurantBase,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_restaurant(restaurant: RestaurantCreate = Body(...)):
    """
    Insert a new restaurant record.

    A unique `id` will be created and provided in the response.
    """
    new_restaurant = await restaurant_collection.insert_one(
        restaurant.model_dump(by_alias=True, exclude=["id"])        
    )
    created_restaurant = await restaurant_collection.find_one(
        {'_id': new_restaurant.inserted_id}
    )
    return created_restaurant


@router.put(
    "/{restaurant_id}",
    response_description="Update a restaurant",
    response_model=RestaurantBase,
)
async def update_restaurant(restaurant_id: str, new_restaurant: RestaurantUpdate = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    restaurant  = {
        k: v for k, v in new_restaurant.model_dump(by_alias=True).items() if v is not None
    }

    if len(restaurant) >= 1:
        update_result = await restaurant_collection.find_one_and_update(
            {"_id": ObjectId(restaurant_id)},
            {"$set": restaurant},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"restaurant {restaurant_id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_restaurant := await restaurant_collection.find_one({"_id": restaurant_id})) is not None:
        return existing_restaurant

    raise HTTPException(status_code=404, detail=f"Student {restaurant_id} not found")

@router.delete("/{restaurant_id}", response_description="Delete a restaurant")
async def delete_restaurant(restaurant_id: str):
    delete_result = await restaurant_collection.delete_one({"_id": ObjectId(restaurant_id)})
    
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"restaurant {restaurant_id} is not found")

@router.get("/trending_restaurants?zone={zone_id}")
async def get_trending_restaurants(zone_id: str):
    restaurants = []
    return {"trending_restaurants": restaurants}
