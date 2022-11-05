from django.http import JsonResponse


def get_response(data=None, message="", status=200):
    if data is not None and not isinstance(data, dict):
        raise TypeError("data should be a dictionary")
    if data is None:
        data = {}
    message_dict = {200: "OK", 201: "Created", 405: "Method not allowed", 406: "invalid credentials"}
    if message == "":
        message = message_dict.get(status)
    return JsonResponse({"data": data, "message": message, "status": status}, status=status)
