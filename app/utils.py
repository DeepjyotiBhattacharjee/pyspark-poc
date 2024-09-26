from fastapi.responses import JSONResponse

def success_200(data):
    return JSONResponse(status_code=200, content={"status": "success", "message": "Operation successful", "data": data})

def internal_server_error_500(message):
    return JSONResponse(status_code=500, content={"status": "error", "message": message})

def bad_request_400(message):
    return JSONResponse(status_code=400, content={"status": "error", "message": message})

def not_found_404(message):
    return JSONResponse(status_code=404, content={"status": "error", "message": message})
