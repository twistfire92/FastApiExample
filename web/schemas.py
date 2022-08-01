from pydantic import BaseModel, Field, validator
from enum import Enum


class Group(Enum):
    romashka = "Ромашка"
    raketa = "Ракета"
    tulpan = "Тюльпан"


class ToyBase(BaseModel):
    name: str
    description: str | None # описание - необязательное поле


class ToyCreate(ToyBase):
    user_id: int


class ToyOutShort(ToyBase):
    class Config:
        orm_mode = True


class ToyOut(ToyBase):
    id: int
    # флагом alias помечено как это поле будет называться при импорте
    user: "UserOutShort" = Field(alias='owner')

    class Config:
        orm_mode = True
        # этим флагом разрешили получать значение поля по его имени, а не по alias
        allow_population_by_field_name = True


class UserBase(BaseModel):
    name: str
    group: Group


class UserCreate(UserBase):
    age: int

    @validator('age')
    def age_validator(cls, value):
        if value > 6:
            raise ValueError('Взрослый уже! Пора бы в школу!')
        return value


class UserOut(UserCreate):
    id: int
    toys: list[ToyOutShort]

    class Config:
        orm_mode = True


class UserOutShort(UserBase):
    class Config:
        orm_mode = True


ToyOut.update_forward_refs()
