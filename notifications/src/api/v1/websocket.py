from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/like")
async def handle_likes():
    """
    Нужно продумать как получить идентификатор владельца комментария,
    которому поставили лайк
    """
    return None
