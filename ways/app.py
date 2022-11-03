from fastapi import FastAPI
import uvicorn

from services.database import get_resumes_by_name, find_all_resume_title_where_has_this_profession
from services.tools import find_most_popular_distict_way, transform_distinctWay_to_BestWay, Way
from services.config import settings


app = FastAPI()

@app.get('/')
def hello_world():
    """Метод главной страницы, который выводит подсказку о том, где искать документацию по АПИ"""
    return {"message": f"Добавьте к адресной строке /docs для подробной информации о методах"}


@app.get('/most-popular', response_model=list[Way])
def get_most_popular_ways(profession: str = '', count: int = 3) -> list[Way]:
    """Метод выводит топ путей (количество путей задается переменной count) по заданной профессии
    Искать введеную профессию будут только среди целевых профессий\n
    Если путей по заданной профессии нет, то будет выведен пустой список\n
    Параметры:\n
    1. profession: целевая профессия, чьи пути нужно найти\n
    2. count (по умолчанию 3): количество путей"""

    resumes = get_resumes_by_name(profession, table_name='New')
    distinct_ways = find_most_popular_distict_way(resumes, count) # Оставляем только уникальные пути
    return transform_distinctWay_to_BestWay(distinct_ways)


@app.get('/top-related-professions', response_model=list[str])
def get_top_related_professions(profession: str = '', count: int = 5) -> list[str]:
    """Метод выводит топ целевых профессий, в резюме которых среди занимаемых должностей есть искомая профессия
    Параметры:\n
    1. profession: название должности, по которым нужно найти целевую профессию\n
    2. count (по умолчанию 3): количество профессий"""

    professions = find_all_resume_title_where_has_this_profession(profession)
    return professions[:count]


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
)