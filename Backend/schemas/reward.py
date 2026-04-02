from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Base Class: Common attributes
class RewardBase(BaseModel):
    name: str
    points_cost: int
    description: Optional[str] = None
    is_active: bool = True

# 2. Create Class: Used for POST /rewards/
# Inherits from Base to ensure 'name' and 'points_cost' are REQUIRED.
class RewardCreate(RewardBase):
    pass

# 3. Update Class: Used for PUT /rewards/{reward_id}
# Everything is Optional so you can update just one field (like is_active).
class RewardUpdate(BaseModel):
    name: Optional[str] = None
    points_cost: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

# 4. Response Class: What the API returns to the user
class RewardResponse(RewardBase):
    id: int
    user_id: int

    # Pydantic V2 configuration to read from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)