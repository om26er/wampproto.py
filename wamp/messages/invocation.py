from __future__ import annotations

from wamp.messages import error, util
from wamp.messages.message import Message


class Invocation(Message):
    INVOCATION_TEXT = "INVOCATION"
    MESSAGE_TYPE = 68

    def __init__(
        self,
        request_id: int,
        registration_id: int,
        args: list | None = None,
        kwargs: dict | None = None,
        details: dict | None = None,
    ):
        super().__init__()
        self.request_id = request_id
        self.registration_id = registration_id
        self.args = args
        self.kwargs = kwargs
        self.details = details if details is not None else {}

    @staticmethod
    def parse(msg: list) -> Invocation:
        if not isinstance(msg, list):
            raise error.InvalidTypeError(list, type(msg), "message", Invocation.INVOCATION_TEXT)

        if len(msg) < 4 or len(msg) > 6:
            raise error.InvalidMessageLengthError("between 4 & 6", len(msg), Invocation.INVOCATION_TEXT)

        if msg[0] != Invocation.MESSAGE_TYPE:
            raise error.InvalidMessageTypeError(Invocation.MESSAGE_TYPE, msg[0], Invocation.INVOCATION_TEXT)

        request_id = util.validate_session_id_or_raise(msg[1], Invocation.INVOCATION_TEXT, "request ID")
        registration_id = util.validate_session_id_or_raise(msg[2], Invocation.INVOCATION_TEXT, "registration ID")
        options = util.validate_details_or_raise(msg[3], Invocation.INVOCATION_TEXT, "options")

        args = None
        if len(msg) > 4:
            args = msg[4]
            if not isinstance(args, list):
                raise error.InvalidTypeError(list, type(msg[4]), "args", Invocation.INVOCATION_TEXT)

        kwargs = None
        if len(msg) > 5:
            kwargs = msg[5]
            if not isinstance(kwargs, dict):
                raise error.InvalidTypeError(dict, type(msg[5]), "kwargs", Invocation.INVOCATION_TEXT)

        return Invocation(request_id, registration_id, args, kwargs, options)

    def marshal(self) -> list:
        message = [Invocation.MESSAGE_TYPE, self.request_id, self.registration_id, self.details]
        if self.args is not None:
            message.append(self.args)

        if self.kwargs is not None:
            message.append(self.kwargs)

        return message
