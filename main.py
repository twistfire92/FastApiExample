import uvicorn


if __name__ == '__main__':
    uvicorn.run('application:get_app', reload=True)

