import http.server
import socketserver
import json
import os
import threading
import logging
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger("Alucard.Management")

class ManagementHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == "/api/status":
            self.send_json({"status": "active", "module": "ManagementAPI"})
            
        elif path == "/logs/list":
            self.handle_list_logs()
            
        elif path == "/logs/view":
            self.handle_view_log(query)
            
        else:
            self.send_error(404, "Not Found")
            
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=4).encode())
        
    def handle_list_logs(self):
        """Lists available log dates and files"""
        bg_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
        structure = {}
        
        if os.path.exists(bg_dir):
            for date_folder in os.listdir(bg_dir):
                folder_path = os.path.join(bg_dir, date_folder)
                if os.path.isdir(folder_path):
                    files = os.listdir(folder_path)
                    structure[date_folder] = files
                    
        self.send_json(structure)
        
    def handle_view_log(self, query):
        """Returns content of a specific log file"""
        date = query.get("date", [None])[0]
        filename = query.get("file", [None])[0]
        
        if not date or not filename:
            self.send_error(400, "Missing 'date' or 'file' params")
            return
            
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', date, filename)
        
        # Security: Prevent traversal
        real_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
        real_path = os.path.abspath(file_path)
        
        if not real_path.startswith(real_root):
            self.send_error(403, "Access Denied")
            return
            
        if not os.path.exists(real_path):
            self.send_error(404, "Log file not found")
            return
            
        try:
            with open(real_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            self.send_json({"date": date, "file": filename, "content": content})
        except Exception as e:
            self.send_error(500, str(e))

class ManagementServer:
    def __init__(self, port=5000):
        self.port = port
        self.httpd = None
        self.thread = None
        self.running = False
        
    def start(self):
        self.running = True
        self.httpd = socketserver.TCPServer(("127.0.0.1", self.port), ManagementHandler)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"🔧 [MANAGEMENT] API listening on http://127.0.0.1:{self.port}")
        
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        self.running = False
