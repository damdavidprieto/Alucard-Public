"""
Logging system for the honeypot.
Provides JSON-formatted logging with geolocation.
"""

import logging
import json
import datetime
import os
from typing import Dict, Any, Optional

from .geolocation import GeoLocationService


# Get instance metadata (for GCP deployment tracking)
def get_instance_metadata():
    """Get instance metadata if running on GCP"""
    try:
        import requests
        metadata_server = "http://metadata.google.internal/computeMetadata/v1/"
        metadata_flavor = {'Metadata-Flavor': 'Google'}
        
        zone = requests.get(metadata_server + 'instance/zone', 
                           headers=metadata_flavor, timeout=1).text.split('/')[-1]
        instance_name = requests.get(metadata_server + 'instance/name',
                                     headers=metadata_flavor, timeout=1).text
        external_ip = requests.get(metadata_server + 'instance/network-interfaces/0/access-configs/0/external-ip',
                                   headers=metadata_flavor, timeout=1).text
        
        return {
            'instance_name': instance_name,
            'zone': zone,
            'external_ip': external_ip,
            'environment': 'GCP'
        }
    except:
        return {
            'instance_name': 'local',
            'zone': 'local',
            'external_ip': 'localhost',
            'environment': 'LOCAL'
        }


INSTANCE_METADATA = get_instance_metadata()


# Configure logging with daily rotation
# We will manage handlers dynamically in HoneypotLogger

class HoneypotLogger:
    """Enhanced logger with JSON formatting, geolocation, and automatic rotation"""
    
    _current_date = None
    _logger = logging.getLogger('honeypot')
    _logger.setLevel(logging.INFO)
    
    @staticmethod
    def _get_log_filename(date_str):
        """Generate log filename for a specific date"""
        log_dir = os.environ.get('LOG_DIR', '/logs')
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f'honeypot_{date_str}.log')

    @classmethod
    def _check_rotation(cls):
        """Check if date has changed and rotate log file if needed"""
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if cls._current_date != now_date:
            # Rotate
            new_log_file = cls._get_log_filename(now_date)
            
            # Remove old handlers
            for handler in cls._logger.handlers[:]:
                cls._logger.removeHandler(handler)
                handler.close()
            
            # Add new handler
            file_handler = logging.FileHandler(new_log_file)
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)
            
            cls._current_date = now_date
            print(f"[*] Log rotated to: {new_log_file}")

    # --- SAMAEL INTEGRATION ---
    _samael_client = None

    @classmethod
    def _get_samael_client(cls):
        """Lazy load SamaelClient"""
        if cls._samael_client is None:
            try:
                # Add path dynamically for now
                import sys
                from pathlib import Path
                shared_path = str(Path(os.getcwd()) / ".." / "Shared" / "rare-sdk")
                if shared_path not in sys.path:
                    sys.path.append(shared_path)
                    
                from rare_sdk.client import SamaelClient
                
                # Config from env
                secret = os.environ.get("RARE_SHARED_SECRET", "dev-secret-key-123")
                url = os.environ.get("SAMAEL_URL", "http://localhost:8889")
                
                cls._samael_client = SamaelClient(url, secret, client_id="Alucard")
                print("✅ [ALUCARD] Connected to Samael SDK")
            except ImportError:
                print("⚠️ [ALUCARD] rare-sdk not found, telemetry disabled")
            except Exception as e:
                print(f"⚠️ [ALUCARD] Error initializing Samael SDK: {e}")
        return cls._samael_client

    @classmethod
    def _send_telemetry(cls, event_type: str, data: Dict[str, Any]):
        """Send telemetry to Samael in background"""
        client = cls._get_samael_client()
        if client:
            try:
                # We should run this async or in thread to not block, 
                # but for now we do it inline with exception handling
                payload = {
                    "source": "alucard",
                    "event_type": event_type,
                    "data": data,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                client.send_telemetry(payload)
            except Exception as e:
                # Fail silently to not impact honeypot
                pass

    @staticmethod
    def log_connection(
        service: str,
        ip: str,
        port: int,
        data: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a connection event with full details.
        
        Args:
            service: Service name (HTTP, SSH, etc.)
            ip: Source IP address
            port: Source port
            data: Optional data payload
            extra: Optional extra metadata
        """
        # Check for rotation before logging
        HoneypotLogger._check_rotation()

        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'instance': INSTANCE_METADATA,  # Add instance metadata
            'service': service,
            'source_ip': ip,
            'source_port': port,
            'geolocation': GeoLocationService.get_location(ip),
            'data': data,
            'extra': extra or {}
        }
        
        # Write to log file via our managed logger
        HoneypotLogger._logger.info(json.dumps(log_entry))
        
        # Console output
        country = log_entry['geolocation'].get('country', 'Unknown')
        env = INSTANCE_METADATA['environment']
        instance = INSTANCE_METADATA['instance_name']
        print(f"[{env}:{instance}] [{service}] Connection from {ip}:{port} ({country})")

        # Telemetry: Log all connections? Maybe too noisy.
        # Let's log if it looks suspicious or just basic stats.
        # For now only log if it's an attack via log_attack calling this?
        # Actually log_attack calls log_connection, so we'll handle it inside log_attack mostly,
        # but maybe we want to send "connection_attempt" too.
        # Let's keep it lightweight for now and only send explicit attacks.
    
    @staticmethod
    def log_attack(
        service: str,
        ip: str,
        port: int,
        attack_type: str,
        details: Dict[str, Any]
    ) -> None:
        """
        Log a detected attack.
        
        Args:
            service: Service name
            ip: Source IP
            port: Source port
            attack_type: Type of attack detected
            details: Attack details
        """
        extra = {
            'attack_type': attack_type,
            'attack_details': details
        }
        
        HoneypotLogger.log_connection(
            service=service,
            ip=ip,
            port=port,
            data=f"Attack detected: {attack_type}",
            extra=extra
        )

        # Send to Samael
        HoneypotLogger._send_telemetry("attack_detected", {
            "service": service,
            "ip": ip,
            "port": port,
            "type": attack_type,
            "details": details,
            "geolocation": GeoLocationService.get_location(ip)
        })
