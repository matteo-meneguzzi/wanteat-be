from enum import Enum

class PermissionEnum(str, Enum):
    READ_RESTAURANTS = "read_restaurants"
    WRITE_RESTAURANTS = "write_restaurants"
    DELETE_RESTAURANTS = "delete_restaurants"
    READ_USERS = "read_users"
    WRITE_USERS = "write_users"
    DELETE_USERS = "delete_users"
    ADMIN = "admin"
