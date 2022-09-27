from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from models import Order, User
from schemas import Order as OrderSchema, UpdateOrder
from database import Session, engine

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

session = Session(bind=engine)


@order_router.post('/create', response_model_exclude_defaults=OrderSchema, status_code=201)
async def create_order(order: OrderSchema, Authorize: AuthJWT = Depends()):
    """_summary_: This is the create order route

    Args:
        order (OrderSchema): quantity, order_status, pizza_size

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        new_order = Order(
            quantity=order.quantity,
            order_status=order.order_status,
            pizza_size=order.pizza_size,
            user_id=db_user.id
        )
        session.add(new_order)
        session.commit()

        return {"message": "Order created successfully"}

    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@order_router.get('/all', response_model_exclude_defaults=OrderSchema, status_code=200)
async def get_orders(Authorize: AuthJWT = Depends()):
    """_summary_: This is the get orders route

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        if (db_user.is_staff):
            orders = session.query(Order).all()
            return orders
        else:
            return HTTPException(status_code=401, detail="You are not authorized to view orders")
    except Exception:
        return HTTPException(status_code=400, detail="Something went wrong")


@order_router.get('/order/{id}', response_model_exclude_defaults=OrderSchema, status_code=200)
async def get_order(id: int, Authorize: AuthJWT = Depends()):
    """_summary_: This is the get order route

    Args:
        id (int): order id

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        if (db_user.is_staff) or (db_user.id == order.user_id):
            order = session.query(Order).filter_by(id=id).first()
            return order
        else:
            return HTTPException(status_code=401, detail="You are not authorized to view this order")
    except Exception:
        return HTTPException(status_code=500, detail="Sorry, something went wrong")


@order_router.get('/get', response_model_exclude_defaults=OrderSchema, status_code=200)
async def get_user_orders(Authorize: AuthJWT = Depends()):
    """_summary_: This is the get user orders route

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        orders = session.query(Order).filter_by(user_id=db_user.id).all()
        return orders
    except Exception:
        return HTTPException(status_code=500, detail="Sorry, something went wrong")


# only is_staff or the user who created the order can update the order
@order_router.put('/update/{id}', response_model_exclude_defaults=UpdateOrder, status_code=200)
async def update_order(id: int, order: UpdateOrder, Authorize: AuthJWT = Depends()):
    """_summary_: This is the update order route

    Args:
        id (int): order id
        order (UpdateOrder): quantity, or order_status or pizza_size

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        order = session.query(Order).filter_by(id=id).first()
        if (db_user.is_staff) or (db_user.id == order.user_id):
            order.order_status = order.order_status
            order.quantity = order.quantity
            order.pizza_size = order.pizza_size

            session.commit()
            return {"message": "Order updated successfully"}
        else:
            return HTTPException(status_code=401, detail="You are not authorized to update this order")
    except Exception:
        return HTTPException(status_code=500, detail="Sorry, something went wrong")


@order_router.delete('/delete/{id}', response_model_exclude_defaults=OrderSchema, status_code=200)
async def delete_order(id: int, Authorize: AuthJWT = Depends()):
    """_summary_: This is the delete order route

    Args:
        id (int): order id

    Returns:
        _type_: Json response
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter_by(username=current_user).first()
        order = session.query(Order).filter_by(id=id).first()
        if (db_user.is_staff) or (db_user.id == order.user_id):
            session.delete(order)
            session.commit()
            return {"message": "Order deleted successfully"}
        else:
            return HTTPException(status_code=401, detail="You are not authorized to delete this order")
    except Exception:
        return HTTPException(status_code=500, detail="Sorry, something went wrong")
