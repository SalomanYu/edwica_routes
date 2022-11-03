from fastapi import FastAPI, Query
import uvicorn

from services.database import get_all_resumes, get_resumes_by_name
from services.config import settings
from services.tools import find_most_popular_distict_way, transform_distinctWay_to_BestWay, BestwWay, Step


app = FastAPI()

@app.get('/hello')
def hello_world():
    a = get_all_resumes(table_name=settings.local_table_name)
    return {"message": f"{[i for i in a][0]}"}


@app.get('/most-popular/', response_model=list[BestwWay])
def get_most_popular_ways(profession: str = '', count: int = 3) -> list[BestwWay]:
    """ОПисание тут"""
    if not profession: return {"message": "Вы забыли указать профессию или количество путей"}
    
    resumes = get_resumes_by_name(profession, table_name='New')
    distinct_ways = find_most_popular_distict_way(resumes, count)
    return transform_distinctWay_to_BestWay(distinct_ways)


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
)