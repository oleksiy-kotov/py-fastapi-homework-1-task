import datetime
from typing import List, Optional

from pydantic import BaseModel


class MovieSchema(BaseModel):
    id: int
    name: str
    date: datetime.datetime
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int


class MovieDetailResponseSchema(MovieSchema):
    pass