from rest_framework .views import Response


def get_response(data=None, message="", status=200):
    if data is None:
        data = {}
    message_dict = {200: "OK", 201: "Created", 202: "Accepted", 405: "Method not allowed", 406: "invalid credentials"}
    if message == "":
        message = message_dict.get(status)
    return Response({"data": data, "message": message, "status": status}, status=status)
