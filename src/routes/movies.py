from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter(prefix="/movies/", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(page: int = Query(1, ge=1, description="Page number (starting from 1)"),
                     per_page: int = Query(10, ge=1, le=20, description="Items per page"),
                     db: AsyncSession = Depends(get_db)):

    count_query = select(func.count().select_from(MovieModel))
    count_results = await db.execute(count_query)
    total_items = count_results.scalar_one()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page} not found. Total pages: {total_pages}"
        )

    offset = (page - 1) * per_page
    query = select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    results = await db.execute(query)
    movies = results.scalars().all()

    base_url = "/theater/movies/"

    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(id: int, db: AsyncSession = Depends(get_db)):
    query = select(MovieModel).where(MovieModel.id == id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
