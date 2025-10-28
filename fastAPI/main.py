from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

GLOSSARY_TERMS = [
  {
    "id": 1,
    "term": "Термин 1",
    "definition": "Описание 1",
    "coordinate": {
    "x": 50,
    "y": 50
    }
  },
  {
    "id": 2,
    "term": "Термин 2",
    "definition": "Описание 2",
    "coordinate": {
    "x": 100,
    "y": 50
    }
  },
  {
    "id": 3,
    "term": "Термин 3",
    "definition": "Описание 3",
    "coordinate": {
    "x": 150,
    "y": 50
    }
  },
]

@app.get('/')
def testFunc():
  return 'Hello World'

@app.get('/terms', summary='Получение списка всех терминов.', tags=['ТЕРМИНЫ'])
def getAllTerms():
  return GLOSSARY_TERMS

@app.get('/terms/search-by-id/{term_id}', summary='Получение термина по id', tags=['ТЕРМИНЫ'])
def getTermById(term_id: int):
  for term in GLOSSARY_TERMS:
    if term['id'] == term_id:
      return term
  raise HTTPException(status_code=404, detail='Термин с id='+ term_id + ' не найден')

@app.get('/terms/search-by-name/{term_name}', summary='Получение информации о конкретном термине по ключевому слову', tags=['ТЕРМИНЫ'])
def getTermByName(term_name: str):
  for term in GLOSSARY_TERMS:
    if term['term'] == term_name:
      return term
  raise HTTPException(status_code=404, detail='Термин с ключевым словом - '+ term_name + ' не найден')


class NewTerm(BaseModel):
  term: str = Field(max_length=100)
  definition: str | None = Field(max_length=1000)
  # coordinate: Coordinate

class Coordinate(BaseModel):
  x: int = Field(ge=0)
  y: int = Field(ge=0)

@app.post('/terms', summary='Добавление нового термина с описанием', tags=['ТЕРМИНЫ'])
def createNewTerm(new_term: NewTerm):
  GLOSSARY_TERMS.append({
    "id": len(GLOSSARY_TERMS) + 1,
    "term": new_term.term,
    "definition": new_term.definition,
    "coordinate": {
      "x": GLOSSARY_TERMS[len(GLOSSARY_TERMS) - 1]['coordinate']['x'] + 50,
      "y": 50
    }
  })
  return {'success': True, 'message': 'Новый термин был успешно добавлен!', 'addedTermElem': GLOSSARY_TERMS[-1]}

@app.patch('/terms/{term_id}', summary='Обновление существующего термина по id', tags=['ТЕРМИНЫ'])
def updateTermById(term_id: int, new_term: NewTerm):
  global GLOSSARY_TERMS

  for term in GLOSSARY_TERMS:
    if term['id'] == term_id:
      term['term'] = new_term.term
      term['definition'] = new_term.definition
      return {'success': True, 'message': 'Термин был успешно обновлен!', 'updatedTermElem': term}

  raise HTTPException(status_code=404, detail='Обновить термин с id='+ term_id + ' не удалось')

@app.delete('/terms/{term_id}', summary='Удаление термина из глоссария по id', tags=['ТЕРМИНЫ'])
def deleteTermById(term_id: int):
  global GLOSSARY_TERMS
  isTerm: bool = False

  for term in GLOSSARY_TERMS:
    if term['id'] == term_id:
      isTerm = True
      deletedTermElem = term

  if isTerm:
    GLOSSARY_TERMS = list(filter(lambda term: term["id"] != term_id, GLOSSARY_TERMS))
    return {'success': True, 'message': 'Термин был успешно удален!', 'deletedTermElem': deletedTermElem}
  
  raise HTTPException(status_code=404, detail='Удалить термин с id='+ term_id + ' не удалось')


if __name__ == "__main__":
  uvicorn.run("main:app", reload=True)
