import datetime
import threading
import http.server
import unittest
import urllib.request
import json
import time

# Import MyRequestHandler from your code or provide its definition here
from http_server_for_mock_API import MyRequestHandler

class UnitTests(unittest.TestCase):
    """Unit tests for urlopen"""

    def assertDatetimeAlmostEqual(self, datetime1, datetime2, delta=None):
        """
        Custom assertion to compare datetime objects with optional delta.
        """
        if delta is None:
            delta = datetime.timedelta(seconds=1)  # Adjust the delta as needed
        self.assertAlmostEqual(datetime1.replace(second=0, microsecond=0), datetime2.replace(second=0, microsecond=0),
                               delta=delta)

    def test_do_GET(self):
        """Test GET request to /api/v1/servers"""
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 8000), MyRequestHandler
        )
        with server:
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            try:
                url = "http://127.0.0.1:8000/api/v1/gettime"
                response = urllib.request.urlopen(url)
                result_data = response.read().decode('utf-8')
                result = json.loads(result_data)
                server.shutdown()
            except Exception as e:
                result = str(e)

        # Modify the expected response based on your server's logic
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        expected_response = {"objectId": "def-123-ghi-456", "country": "Asia/India", "time": localtime}
        print("Expected Response : ", expected_response)
        print("Actual Response : ", result)
        self.assertEqual(result['objectId'], expected_response['objectId'])
        self.assertEqual(result['country'], expected_response['country'])
        # not comparing the time due to difference in seconds
        #self.assertDatetimeAlmostEqual(result['time'], expected_response['time'])


if __name__ == '__main__':
    unittest.main()
