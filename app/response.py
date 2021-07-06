from rest_framework.response import Response


class APIResponse(Response):
    @property
    def rendered_content(self):
        return super(APIResponse, self).rendered_content