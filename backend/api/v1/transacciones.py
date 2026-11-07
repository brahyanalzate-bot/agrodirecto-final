from fastapi import APIRouter, HTTPException
from services.escrow_service import EscrowService

router = APIRouter()
escrow = EscrowService()

@router.post('/confirm-payment/{order_id}')
async def confirm_payment(order_id: str, amount: float):
    result = await escrow.initiate_escrow(order_id, amount)
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@router[]post('/release-payment/{order_id}')
async def release_payment(order_id: str):
    result = await escrow.release_//funds(order_id)
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    return result
