from services.schedules import ProfessionStep, ResumeGroup, DistinctWay, BestwWay, Step
from services.config import settings


def group_steps_to_resume(data: tuple[ProfessionStep]) -> list[ResumeGroup]:
    resume_dict = {} # Вида ID-ссылка на резюме:list[ProfessionsStep]
    for step in data:
        if step.resumeId not in resume_dict:
            resume_dict[step.resumeId] = [step]
        else:
            resume_dict[step.resumeId].append(step)
    result = [ResumeGroup(ID=id, ITEMS=group) for id, group in resume_dict.items()] # Генератор нельзя использовать, т.к собираемся обращаться по индексу
    return result


def find_most_popular_distict_way(resumes: list[ResumeGroup], count: int = 0) -> list[DistinctWay]:
    distinct_ways: dict[DistinctWay, int] = {} # Словарь типа Айди пути: количество повторений
    for resume in resumes:
        step = resume.ITEMS[0]
        current_way = DistinctWay(
            similarId=step.similarPathId, 
            resumeId=resume.ID,
            skills=step.skills,
            deadline=step.generalExcepience,
            steps=(Step(profession=step.experiencePost, deadline=step.experienceDuration) for step in resume.ITEMS)
            # steps=tuple([(step.experiencePost, step.experienceDuration) for step in resume.ITEMS])
            )
        if current_way in distinct_ways:distinct_ways[current_way] += 1
        else:distinct_ways[current_way] = 1
    
    most_popular_way = sorted(distinct_ways, key=distinct_ways.get, reverse=True)
    if not count: return [key for key in most_popular_way]
    return [key for key in most_popular_way[:count]]


def transform_distinctWay_to_BestWay(ways: list[DistinctWay]) -> list[BestwWay]:
    result = [
        {
            "deadline": way.deadline,
            "skills": way.skills.split(' | '),
            "steps": [{"profession": step.profession, "deadline": step.deadline} for step in way.steps]
        }
    for way in ways]
    return result




def top_following_professions(profession: str, resumes: list[ResumeGroup], count: int= 5):
    
    distinct_ways = find_most_popular_distict_way(group_steps_to_resume(resumes))
    popular_folowing_professions: dict[str, int] = {}
    for way in distinct_ways:
        if len(way.steps) > 1: print(way.steps)
        try:
            follow_profession = next((way.steps[i-1] for i,k in enumerate(way.steps) if k[0] == profession))
            if follow_profession == profession: continue
        except IndexError:
            continue

