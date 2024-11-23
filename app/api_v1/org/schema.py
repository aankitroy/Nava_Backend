from pydantic import BaseModel
class OrganizationCreateRequest(BaseModel):
    organization_name: str