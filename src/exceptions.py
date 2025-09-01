from datetime import date

from fastapi import HTTPException


class HotelAppException(Exception):
    detail = 'Custom app exception'

    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(HotelAppException):
    detail = 'Object not found'


class RoomNotFoundException(HotelAppException):
    detail = 'Room not found'


class HotelNotFoundException(HotelAppException):
    detail = 'Hotel not found'


class ObjectAlreadyExistsException(HotelAppException):
    detail = 'Object already exists'


class AllRoomsAreBookedException(HotelAppException):
    detail = 'All rooms are booked'


class IncorrectTokenException(HotelAppException):
    detail = 'Incorrect token'


class EmailNotRegisteredException(HotelAppException):
    detail = 'Email not registered'


class IncorrectPasswordException(HotelAppException):
    detail = 'Incorrect password'


class UserAlreadyExistsException(HotelAppException):
    detail = 'User already exists'


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail='date_to must be after date_from')


class HotelAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(HotelAppHTTPException):
    status_code = 404
    detail = 'Hotel not found'


class RoomNotFoundHTTPException(HotelAppHTTPException):
    status_code = 404
    detail = 'Room not found'


class AllRoomsAreBookedHTTPException(HotelAppHTTPException):
    status_code = 409
    detail = 'All rooms are booked'


class IncorrectTokenHTTPException(HotelAppHTTPException):
    detail = 'Incorrect token'


class EmailNotRegisteredHTTPException(HotelAppHTTPException):
    status_code = 401
    detail = 'Email not registered'


class UserEmailAlreadyExistsHTTPException(HotelAppHTTPException):
    status_code = 409
    detail = 'User already exists'


class IncorrectPasswordHTTPException(HotelAppHTTPException):
    status_code = 401
    detail = 'Incorrect password'


class NoAccessTokenHTTPException(HotelAppHTTPException):
    status_code = 401
    detail = 'No access token'
