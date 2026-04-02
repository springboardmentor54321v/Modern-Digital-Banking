from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.alert import Alert
from app.models.user import User
from app.api.deps import get_current_user 
from app.schemas.alert import AlertResponse, MarkReadRequest, AlertCountResponse

router = APIRouter()

# 1. GET ALL ALERTS (Paginated)
@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    """Fetch all alerts for the user, sorted by latest first."""
    alerts = db.query(Alert).filter(Alert.user_id == current_user.id)\
        .order_by(Alert.created_at.desc())\
        .limit(limit).offset(offset).all()
    return alerts

# 2. GET UNREAD ALERTS
@router.get("/unread", response_model=List[AlertResponse])
def get_unread_alerts(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Filter for notifications where is_read is False."""
    unread = db.query(Alert).filter(
        Alert.user_id == current_user.id, 
        Alert.is_read == False
    ).order_by(Alert.created_at.desc()).all()
    return unread

# 3. POST MARK AS READ (The 404 Fix)
@router.post("/mark-read", status_code=status.HTTP_200_OK)
def mark_alert_as_read(
    request: MarkReadRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific alert state. 
    JSON Input: {"alert_id": 123}
    """
    # Debugging: This helps you see the attempt in your terminal
    print(f"DEBUG: Attempting to mark alert {request.alert_id} for user {current_user.id}")

    alert = db.query(Alert).filter(
        Alert.id == request.alert_id, 
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        # If this triggers, either the ID is wrong or you are logged in as the wrong user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Alert {request.alert_id} not found for current user."
        )
    
    alert.is_read = True
    db.commit()
    return {"message": f"Alert {request.alert_id} marked as read successfully."}

# 4. GET UNREAD COUNT
@router.get("/count", response_model=AlertCountResponse)
def get_alert_count(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Used for dashboard notification badges."""
    count = db.query(Alert).filter(
        Alert.user_id == current_user.id, 
        Alert.is_read == False
    ).count()
    return {"unread_count": count}

# 5. POST MARK ALL AS READ
@router.post("/mark-all-read", status_code=status.HTTP_200_OK)
def mark_all_read(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Bulk action to clear all notifications."""
    db.query(Alert).filter(
        Alert.user_id == current_user.id, 
        Alert.is_read == False
    ).update({Alert.is_read: True}, synchronize_session=False)
    
    db.commit()
    return {"message": "All alerts marked as read."}