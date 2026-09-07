from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/api")
def health():
    return {"status": "success", "message": "api is working"}


@router.get("/protected")
def protected_health():
    return {"status": "success", "message": "api is working"}


# @router.get("/db")
# def db_health(code: str):
#     if code != "now-you-see-me":
#         raise HTTPException(status_code=403, detail="Invalid code")
#     try:
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         return {"status": "success", "message": getpass.getuser()}

#     except Exception:
#         raise HTTPException(status_code=503, detail="db down")
