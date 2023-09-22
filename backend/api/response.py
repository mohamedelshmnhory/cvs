from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, status, data=None, message=None, status_code=None):
        content = {"status": status, "message": message, "data": data}
        super().__init__(data=content, status=status_code)
