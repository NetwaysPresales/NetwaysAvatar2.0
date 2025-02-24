from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from utils.tools import fetch_user_from_db
from data_models.settings_model import current_settings
from logger import logger

router = APIRouter()

@router.put("/api/load-user-data")
async def load_user(request: Request):
    """
    Fetches user data from the database based on `user_id` and updates `current_settings` directly.
    """
    try:
        request_data = await request.json()
        user_id = request_data.get("user_id")

        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")

        # Fetch user data from the database
        user_data = fetch_user_from_db(user_id)

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Directly modify `current_settings`
        current_settings.user.user_id = user_id
        current_settings.user.user_name = user_data.get("name")
        current_settings.user.user_job = user_data.get("job")
        current_settings.user.selected_conversation = None  # Reset conversation selection
        current_settings.user.past_conversations = user_data.get("past_conversations", [])

        logger.info(f"Loaded user data for user_id {user_id}: {user_data}")

        return JSONResponse(content={"message": "User data loaded successfully", "user": user_data})

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        logger.error(f"Error loading user data: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})
