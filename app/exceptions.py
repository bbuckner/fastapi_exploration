from fastapi import HTTPException, status


def post_does_not_exist(id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} does not exist.",
    )


def not_authorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not authorized to perform requested action.",
    )
