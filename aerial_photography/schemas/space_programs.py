from pydantic import BaseModel


class SpacePrograms(BaseModel):
    name: str


class SpaceProgramsUpdate(SpacePrograms):
    id: int


class SpaceProgramsCreate(SpacePrograms):
    pass


class SpaceProgramsSearch(SpacePrograms):
    pass


class SpaceProgramsSearchById(SpacePrograms):
    id: int
