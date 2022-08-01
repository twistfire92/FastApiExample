from enum import Enum

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from pydantic import BaseModel, Field, SecretStr, validator

app = FastAPI()


class ChangePassword(BaseModel):
    new_password: SecretStr = Field(min_length=8, max_length=250)

    @validator('new_password')
    def check_password(cls, value):
        all_letters = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        lowercase_set = set(all_letters)
        uppercase_set = set(all_letters.upper())
        digits_set = set('1234567890')
        set_to_check = set(value.get_secret_value())
        if all(
                [
                    set_to_check & lowercase_set,
                    set_to_check & uppercase_set,
                    set_to_check & digits_set,
                ]
        ):
            return value
        raise ValueError('The password must contain numbers,'
                         ' lowercase and uppercase letters')


class ModelName(Enum):
    model_one = 'one'
    model_two = 'two'
    model_three = 'three'


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/items/{item_id}")
async def path_params_int(item_id: int):
    return {"item_id": item_id}


@app.get("/model/{model_name}")
async def path_params_enum(
        model_name: ModelName,
):
    if model_name == ModelName.model_one:
        return {'model_name': model_name, 'message': 'Your choise - one'}

    if model_name.value == 'two':
        return {'model_name': model_name, 'message': 'Your choise - two'}

    return {'message': 'third variant'}


@app.get('/items')
async def query_params_sample(
        id: int,
        model: ModelName,
        offset: int | None = None
):
    result = {'id': id, 'model': f'model name - {model}'}
    if offset:
        result.update({'offset': offset})
    return result


@app.post('/items')
async def body_params_sample(
        item: ChangePassword
):
    return item


@app.post('/foo')
def body_params_one_more_sample(
        item_id: int = Body(),
        foo: int = Body()
):
    return {"item_id": item_id, "foo": foo}


# ============================ DEPENDENCIES ====================================


"""
    Опишем несколько функций и классов, которые будем использовать в дальнейших примерах
"""


class Input(BaseModel):
    x: int
    y: int


def get_summ_one(x: int, y: int):
    return x + y


def get_summ_two(input_param: Input):
    return input_param.x + input_param.y


def check_less_then_ten(s: int):
    if s > 10:
        raise HTTPException(
            status_code=422,
            detail="value greater than 10"
        )


"""
    Далее уже описываем необходимые руты
"""


@app.get("/dependency-example-one")
def dependency_example_one(
        summ: int = Depends(get_summ_one)
):
    """
        В функции dependency_example_one объявлен всего один параметр summ типа int,
        но указано, что это Dependes от функции get_summ (прошу заметить, что передается именно объект функции!)
        Сама функция get summ принимает 2 параметра и возвращает их сумму. Именно эти 2 параметра будут использоваться
        в качестве query параметров в руте /dependency-example-one
    """
    return {"result": summ}


@app.post("/dependency-example-two")
def dependency_example_two(
    summ: int = Depends(get_summ_two)
):
    """
        Если же мы хотим чтобы параметры ожидались в теле запроса, можно использовать pydantic модели.
        В нашем случае функция get_summ_two, прописанная в зависимостях, принимает модель Input
    """
    return {"result": summ}


@app.get("/dependency-example-three", dependencies=[Depends(check_less_then_ten)])
async def dependency_example_three(
        s: int
):
    """
        В этом примере зависимость объявляется уже в декораторе.
        Нам необходимо проверить входящее значение и ничего не возвращать,
        поэтому логичнее закинуть зависимость в декоратор
        Если пользователь передает значение выше 10 - ошибка.
        Имена переменных используемых в зависимости и в функции ендпоинта должны совпадать,
        иначе Fast-api не поймет что мы от него хотим. Если бы мы тут указали параметр не s, а например x,
        в сваггере увидели бы, что ендпоинт принимает 2 параметра - s из функции зависимости и x, который описали тут
    """
    return {"result": s}


if __name__ == '__main__':
    uvicorn.run('sample:app', reload=True)
