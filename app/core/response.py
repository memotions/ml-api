from fastapi.responses import JSONResponse


def json_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={"status": "error", "message": message},
    )
