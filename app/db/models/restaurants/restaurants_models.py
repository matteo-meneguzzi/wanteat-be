from typing_extensions import Annotated
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from typing import Dict, List, Optional, Union

from app.db.models.users import Owner
PyObjectId = Annotated[str, BeforeValidator(str)]

class RestaurantBase(BaseModel):
    """
    Container for a single restaurant record.
    """
    
    #cuisines: List[str] = Field(...)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    description: str = Field(...)
    location: str = Field(...)
    name: str = Field(...)
    new: bool = Field(...)
    #owner: Optional[Owner] = None
    #rating: Union[int, None] = None
    #trendy: bool = False
    zone: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "description": "cowncowcwoc eiwuicwe eiuwcuweicwe",
                "location": "firenze",
                "name": "ciaone",
                "new": True,
                "zone": 1,
            }
        },
    )
    
    """ model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "cuisines": ["italian", "tuscan"],
                "description": "cowncowcwoc eiwuicwe eiuwcuweicwe",
                "location": "firenze",
                "name": "Field(...)",
                "new": True,
                "owner": None,
                "rating": 4,
                "trendy": False,
                "zone": 1,
            }
        },
    ) """
    
    """  class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "cuisines": ["italian", "tuscan"],
                "description": "cowncowcwoc eiwuicwe eiuwcuweicwe",
                "id": "102j21n138108",
                "location": "firenze",
                "name": "Field(...)",
                "new": True,
                "rating": 4,
                "trendy": False,
                "zone": 1,
            }
        } 
    """

    
    # meta: Dict {
    #     'db_alias': 'core',
    #     'collection': 'restaurants'
    # }

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    
    #cuisines: Optional[List[str]]
    description: Optional[str] = None
    location: Optional[str] = None
    name: Optional[str] = None
    new: Optional[bool] = None
    #trendy: Optional[bool]
    zone: Optional[int] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "description": "cowncowcwoc eiwuicwe eiuwcuweicwe",
                "location": "firenze",
                "name": "Field(...)",
                "new": True,
                "zone": 1,
            }
        },
    )
    
    """ class Config:
        json_schema_extra = {
            "example": {
                "cuisines": ["italian", "tuscan"],
                "description": "cowncowcwoc eiwuicwe eiuwcuweicwe",
                "location": "firenze",
                "name": "Field(...)",
                "new": True,
                "owner": "Mario Ross",
                "rating": 4,
                "trendy": True,
                "zone": 1,
            }
        } """

class TrendyList(BaseModel):
    restaurants: List[RestaurantBase]

class RestaurantRating(BaseModel):
    restaurant_id: int
    rating: int

class RestaurantCollection(BaseModel):
    """
    A container holding a list of `RestaurantModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    restaurants: List[RestaurantBase]