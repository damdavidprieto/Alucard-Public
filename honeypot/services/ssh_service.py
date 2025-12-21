"""
SSH honeypot service.
Handles SSH connections with Paramiko and simulates shell.
"""

import socket
import os
import threading
try:
    import paramiko
except ImportError:
    paramiko = None

from .base import BaseService
from core.logger import HoneypotLogger
from detection.ssh_attacks import SSHAttackDetector
from responses.ssh_shell import FakeShell
import config


class SSHService(BaseService):
    """SSH honeypot service"""
    
    def __init__(self, host: str = None, port: int = None):
        """Initialize SSH service"""
        host = host or config.SSH_HOST
        port = port or config.SSH_PORT
        super().__init__(host, port, "SSH Honeypot")
        super().__init__(host, port, "SSH Honeypot")
        if paramiko is None:
            print("[!] Paramiko not installed. SSH service disabled.")
            return
        self.host_key = self._get_or_create_host_key()
    
    def _get_or_create_host_key(self):
        """
        Get or create RSA host key for SSH server.
        
        Returns:
            RSA key object
        """
        key_file = config.SSH_HOST_KEY_FILE
        
        if os.path.exists(key_file):
            try:
                return paramiko.RSAKey.from_private_key_file(key_file)
            except:
                pass
        
        # Generate new key
        key = paramiko.RSAKey.generate(config.SSH_KEY_SIZE)
        try:
            key.write_private_key_file(key_file)
        except:
            pass  # Use in-memory key if can't write
        
        return key
    
    def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Handle SSH client connection with Paramiko.
        
        Args:
            client_socket: Client socket
            address: Client address (ip, port)
        """
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            
            server = SSHServerInterface(address)
            transport.start_server(server=server)
            
            # Wait for authentication
            channel = transport.accept(20)
            if channel is None:
                transport.close()
                return
            
            # Log successful authentication
            if server.authenticated:
                HoneypotLogger.log_connection(
                    service='SSH',
                    ip=address[0],
                    port=address[1],
                    data=f"Successful login: {server.username}",
                    extra={
                        'username': server.username,
                        'password': server.password,
                        'auth_attempts': server.auth_attempts,
                        'authenticated': True
                    }
                )
                
                # Start fake shell
                self._run_fake_shell(channel, server.username, address)
            
            transport.close()
            
        except Exception as e:
            print(f"[!] SSH handler error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _run_fake_shell(self, channel, username: str, address: tuple) -> None:
        """
        Run fake shell session.
        
        Args:
            channel: Paramiko channel
            username: Authenticated username
            address: Client address
        """
        shell = FakeShell(username, address)
        
        # Send banner
        channel.send(shell.get_banner())
        
        while True:
            try:
                # Send prompt
                channel.send(shell.get_prompt())
                
                # Read command
                command = self._read_command(channel)
                if command is None:
                    return
                
                if not command:
                    continue
                
                # Log command
                HoneypotLogger.log_connection(
                    service='SSH',
                    ip=address[0],
                    port=address[1],
                    data=command,
                    extra={
                        'username': username,
                        'command': command,
                        'current_dir': shell.current_dir,
                        'type': 'command_execution',
                        'attacks_detected': SSHAttackDetector.detect_command_attack(command)
                    }
                )
                
                # Process command
                output = shell.process_command(command)
                channel.send(output + "\r\n")
                
                # Exit commands
                if command.lower() in ['exit', 'logout', 'quit']:
                    channel.send("logout\r\n")
                    return
                    
            except Exception as e:
                print(f"[!] Shell error: {e}")
                return
    
    def _read_command(self, channel) -> str:
        """
        Read command from channel.
        
        Args:
            channel: Paramiko channel
            
        Returns:
            Command string or None if connection closed
        """
        command = ""
        while not command.endswith('\n'):
            char = channel.recv(1).decode('utf-8', errors='ignore')
            if not char:
                return None
            if char == '\x03':  # Ctrl+C
                channel.send("^C\r\n")
                return ""
            command += char
            if char in ['\r', '\n']:
                break
        
        return command.strip()


if paramiko:
    ServerInterface = paramiko.ServerInterface
else:
    ServerInterface = object

class SSHServerInterface(ServerInterface):
    """Paramiko SSH Server Interface for honeypot"""
    
    def __init__(self, client_address: tuple):
        """
        Initialize SSH server interface.
        
        Args:
            client_address: Client IP and port
        """
        self.event = threading.Event()
        self.client_address = client_address
        self.username = None
        self.password = None
        self.authenticated = False
        self.auth_attempts = 0
    
    def check_auth_password(self, username: str, password: str):
        """
        Handle password authentication.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            AUTH_SUCCESSFUL or AUTH_FAILED
        """
        self.auth_attempts += 1
        self.username = username
        self.password = password
        
        # Log authentication attempt
        HoneypotLogger.log_connection(
            service='SSH',
            ip=self.client_address[0],
            port=self.client_address[1],
            data=f"Auth attempt #{self.auth_attempts}",
            extra={
                'username': username,
                'password': password,
                'attempt_number': self.auth_attempts,
                'authenticated': False,
                'type': 'auth_attempt'
            }
        )
        
        # Accept after threshold attempts to seem realistic
        if self.auth_attempts >= config.SSH_AUTH_ATTEMPTS_THRESHOLD:
            self.authenticated = True
            return paramiko.AUTH_SUCCESSFUL
        
        return paramiko.AUTH_FAILED
    
    def check_channel_request(self, kind: str, chanid: int):
        """Allow channel requests"""
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_shell_request(self, channel):
        """Allow shell requests"""
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        """Allow PTY requests"""
        return True
