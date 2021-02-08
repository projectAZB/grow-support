from marshmallow import Schema, fields, post_load

from backend.user.contracts import UserRequest


class UserRequestSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def make_user_request(self, data, **kwargs):
        return UserRequest(**data)
