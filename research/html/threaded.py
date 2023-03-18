import threading
import http.server
import socketserver
import json

class HttpServerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.scroll_pos = 0
        self.server = socketserver.TCPServer(('localhost', 8000), HttpHandler)

    def run(self):
        print('Starting HTTP server on port 8000')
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

class HttpHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Scroll Position</title>
                    <script>
                        function sendScrollPos() {
                            var scrollPos = window.scrollY;
                            var xhr = new XMLHttpRequest();
                            xhr.open('POST', '/scroll', true);
                            xhr.setRequestHeader('Content-Type', 'application/json');
                            xhr.send(JSON.stringify({ 'scrollPos': scrollPos }));
                        }

                        window.addEventListener('scroll', sendScrollPos);
                    </script>
                </head>
                <body>
                    <h1>Scroll Position Example</h1>
                    <p>Scroll down to update the scroll position on the server.</p>
                </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/scroll':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            scroll_pos = data['scrollPos']
            server_thread.scroll_pos = scroll_pos
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Scroll position updated.')
        else:
            self.send_error(404, 'Not Found')

# Start the HTTP server thread
server_thread = HttpServerThread()
server_thread.start()

# Wait for the user to exit the program
input('Press enter to stop the server...')

# Stop the HTTP server thread
server_thread.stop()
server_thread.join()
