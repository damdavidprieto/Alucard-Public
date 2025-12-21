"""
Fake SSH shell implementation.
Simulates a Linux bash shell with fake filesystem.
"""

import datetime
from typing import Dict, List


class FakeShell:
    """Simulated bash shell for SSH honeypot"""
    
    # Fake filesystem structure
    FILESYSTEM = {
        '/': ['bin', 'etc', 'home', 'root', 'tmp', 'usr', 'var'],
        '/root': ['.bashrc', '.profile', 'passwords.txt', 'database.sql'],
        '/etc': ['passwd', 'shadow', 'hosts', 'ssh'],
        '/home': ['user'],
    }
    
    # Fake file contents
    FILE_CONTENTS = {
        'passwords.txt': 'admin:P@ssw0rd123\nroot:toor\nuser:welcome123',
        '.bashrc': '# ~/.bashrc\nalias ll="ls -la"\nexport PATH=/usr/local/bin:$PATH',
        'database.sql': 'CREATE TABLE users (id INT, username VARCHAR(50), password VARCHAR(50));',
        '/etc/passwd': 'root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000::/home/user:/bin/bash',
    }
    
    def __init__(self, username: str, client_address: tuple):
        """
        Initialize fake shell.
        
        Args:
            username: Logged in username
            client_address: Client IP and port tuple
        """
        self.username = username
        self.client_address = client_address
        self.current_dir = '/root' if username == 'root' else f'/home/{username}'
    
    def get_banner(self) -> str:
        """Get welcome banner"""
        banner = f"Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-42-generic x86_64)\r\n\r\n"
        banner += f"Last login: {datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')} from {self.client_address[0]}\r\n"
        return banner
    
    def get_prompt(self) -> str:
        """Get shell prompt"""
        if self.username == 'root':
            return f"{self.username}@honeypot:{self.current_dir}# "
        return f"{self.username}@honeypot:{self.current_dir}$ "
    
    def process_command(self, command: str) -> str:
        """
        Process a shell command and return output.
        
        Args:
            command: Command to process
            
        Returns:
            Command output
        """
        parts = command.split()
        if not parts:
            return ""
        
        cmd = parts[0].lower()
        
        # Route to appropriate handler
        handlers = {
            'whoami': self._cmd_whoami,
            'pwd': self._cmd_pwd,
            'ls': self._cmd_ls,
            'cat': self._cmd_cat,
            'id': self._cmd_id,
            'uname': self._cmd_uname,
            'hostname': self._cmd_hostname,
            'help': self._cmd_help,
            '--help': self._cmd_help,
        }
        
        handler = handlers.get(cmd)
        if handler:
            return handler(parts)
        
        return f"bash: {cmd}: command not found"
    
    def _cmd_whoami(self, parts: List[str]) -> str:
        """whoami command"""
        return self.username
    
    def _cmd_pwd(self, parts: List[str]) -> str:
        """pwd command"""
        return self.current_dir
    
    def _cmd_ls(self, parts: List[str]) -> str:
        """ls command"""
        dir_to_list = parts[1] if len(parts) > 1 else self.current_dir
        
        if dir_to_list in self.FILESYSTEM:
            return '  '.join(self.FILESYSTEM[dir_to_list])
        
        return f"ls: cannot access '{dir_to_list}': No such file or directory"
    
    def _cmd_cat(self, parts: List[str]) -> str:
        """cat command"""
        if len(parts) < 2:
            return "cat: missing file operand"
        
        filename = parts[1]
        
        # Check if file exists in our fake files
        for key, content in self.FILE_CONTENTS.items():
            if key in filename or filename in key:
                return content
        
        return f"cat: {filename}: No such file or directory"
    
    def _cmd_id(self, parts: List[str]) -> str:
        """id command"""
        if self.username == 'root':
            return "uid=0(root) gid=0(root) groups=0(root)"
        return f"uid=1000({self.username}) gid=1000({self.username}) groups=1000({self.username})"
    
    def _cmd_uname(self, parts: List[str]) -> str:
        """uname command"""
        if '-a' in parts:
            return "Linux honeypot 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux"
        return "Linux"
    
    def _cmd_hostname(self, parts: List[str]) -> str:
        """hostname command"""
        return "honeypot"
    
    def _cmd_help(self, parts: List[str]) -> str:
        """help command"""
        return "Available commands: ls, pwd, whoami, cat, id, uname, hostname, exit"
