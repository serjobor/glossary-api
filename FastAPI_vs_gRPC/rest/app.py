from fastapi import FastAPI, HTTPException
from typing import Dict

from .models import Term, TermUpdate
from .data import data

app = FastAPI()

@app.get("/", response_model=Dict[str, Term])
async def get_all_terms():
  """
  Получить список всех терминов
  """
  return data

@app.post('/term/{keyword}', response_model=Term)
async def create_term(keyword: str, term: Term) -> Term:
  """
  Добавить новый термин с описанием
  """
  if keyword in data:
    raise HTTPException(
      status_code=400, 
      detail=f"Термин '{keyword}' уже существует"
    )
  else:
    data[keyword] = term
  return data[keyword]

@app.put('/term/{keyword}', response_model=Term)
async def update_term(keyword: str, term_update: TermUpdate) -> Term:
  """
  Обновить существующий термин
  Можно изменить только definition и source_link, но не title
  """
  if keyword not in data:
    raise HTTPException(
      status_code=404,
      detail=f"Термин '{keyword}' не найден"
    )
  
  # Сохраняем оригинальный title, обновляем только definition и source_link
  data[keyword].definition = term_update.definition
  data[keyword].source_link = term_update.source_link
  
  return data[keyword]