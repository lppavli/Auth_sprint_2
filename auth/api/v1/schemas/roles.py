from pydantic import BaseModel, UUID4


class RoleBase(BaseModel):
    name: str


class RoleUser(BaseModel):
    user_id: UUID4
    role_id: UUID4
