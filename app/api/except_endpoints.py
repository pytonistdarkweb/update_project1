from fastapi import HTTPException, status


class UnauthorizedError(HTTPException):
    def raise_unauthorized_error(detail: str = "Incorrect username or password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
        

class TaskNotFoundError(HTTPException):
    @staticmethod
    def raise_task_not_found_error(task_id: int):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )


class UnauthorizedUserError(HTTPException):
    @staticmethod
    def raise_unauthorized_user_error():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action."
        )