from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sqlite3

from services.config import settings
from services.schedules import ProfessionStep, ResumeGroup
from services.tools import group_steps_to_resume



def connect(db_name: str = settings.local_database_path):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    return db, cursor


def get_all_resumes(table_name: str, db_name: str=settings.local_database_path) -> tuple[ProfessionStep]:
    db, cursor = connect(db_name)
    cursor.execute(f"SELECT * FROM {table_name}")
    # (*item[1:], item[-1]) - Это значит, что мы берем сначала все значения стобцов, кроме первого
    # После этого мы в конец добавляем отдельно первый элемент. Такое решение используется потому,
    # что у ProfessionStep.db_id принимает дефолтное значение и поэтому мы поставиили его в конец
    data = (ProfessionStep(*(*item[1:], item[0])) for item in cursor.fetchall()) 
    db.close()
    return data


def get_resumes_by_name(profession:str, table_name: str, db_name: str = settings.local_database_path) -> list[ResumeGroup]:
    db, cursor = connect(db_name)
    cursor.execute(f"SELECT * FROM {table_name} WHERE title='{profession}';")
    data = (ProfessionStep(*(*item[1:], item[0])) for item in cursor.fetchall()) 
    db.close()
    return group_steps_to_resume(data)

def find_experiencePost(profession: str) -> tuple[ProfessionStep]:
    db, cursor = connect()
    query = f"SELECT resumeId FROM {settings.local_table_name} WHERE experiencePost='{profession}'"
    cursor.execute(query)
    resumeIds = [id[0] for id in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM {settings.local_table_name} WHERE resumeId IN {resumeIds}")
    data = (ProfessionStep(*(*item[1:], item[0])) for item in cursor.fetchall()) 
    db.close()
    exit(len(data))
    return data