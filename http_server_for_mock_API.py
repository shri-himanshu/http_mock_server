import http.server
import json
from urllib.parse import urlparse, parse_qs
import time
import datetime
import pytz

class MyRequestHandler(http.server.BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/api/v1/gettime':
            # Implement GET /api/v1/servers logic here
            response_data = {
                            "objectId": "def-123-ghi-456",
                            "country": "Asia/India",
                            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                          }
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        elif parsed_url.path.startswith('/api/v1/gettime/'):
            # Implement GET /api/v1/servers/{resource-id} logic here
            resource_id = parsed_url.path.split('/')[4:]
            try:
                time_zone = pytz.timezone('/'.join(resource_id))
                time_by_zone = datetime.datetime.now(time_zone)
                response_data = {
                    "objectId": "def-123-ghi-456",
                    "country": '/'.join(resource_id),
                    "time": time_by_zone.strftime("%Y-%m-%d %H:%M:%S"),
                }
                self._set_response()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except pytz.exceptions.UnknownTimeZoneError:
                # Handle the case of an unknown time zone
                error_msg = {
                    "Error": "Unknown time zone",
                    "code": 400  # Use 400 for Bad Request
                }
                self._set_response(400)  # Set the response status code to 400
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))
            except Exception as err:
                # Handle other exceptions
                error_msg = {
                    "Error": "An error occurred",
                    "code": 500
                }
                self._set_response(500)  # Set the response status code to 500
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/api/v1/getname/update':
            # Implement POST /api/v1/getname/update logic here
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                # Check if the request body matches the expected structure
                if "username" in data and isinstance(data["username"], dict):
                    firstname = data["username"].get("firstname")
                    surname = data["username"].get("surname")
                    time = data["username"].get("time")
                    if firstname and surname and time:
                        response_data = {
                            "message": "POST /api/v1/getname/update",
                            "data": {
                                "firstname": firstname,
                                "surname": surname,
                                "time": time
                            }
                        }
                        self._set_response()
                        self.wfile.write(json.dumps(response_data).encode('utf-8'))
                    else:
                        error_response = {
                            "error": "Invalid request body format"
                        }
                        self._set_response(status_code=400)  # Bad Request
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                else:
                    error_response = {
                        "error": "Invalid request body format"
                    }
                    self._set_response(status_code=400)  # Bad Request
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
            except json.JSONDecodeError:
                error_response = {
                    "error": "Invalid JSON format in request body"
                }
                self._set_response(status_code=400)  # Bad Request
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        elif parsed_url.path.startswith('/api/v1/servers/'):
            # Implement POST /api/v1/servers/{resource-id} logic here
            resource_id = parsed_url.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            response_data = {"message": f"POST /api/v1/servers/{resource_id}", "data": data}
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    print('Starting server...')
    httpd.serve_forever()
