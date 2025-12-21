"""
Geolocation service for IP addresses.
Provides location data for logging and analysis.
"""

import requests
from typing import Dict, Any


class GeoLocationService:
    """Service for geolocating IP addresses"""
    
    # Cache to avoid repeated API calls
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def get_location(cls, ip: str) -> Dict[str, Any]:
        """
        Get geolocation data for an IP address.
        
        Args:
            ip: IP address to geolocate
            
        Returns:
            Dictionary with country, city, isp, lat, lon
        """
        # Check cache first
        if ip in cls._cache:
            return cls._cache[ip]
        
        # Check if private IP
        if cls._is_private_ip(ip):
            result = {
                'country': 'Local Network',
                'city': 'N/A',
                'isp': 'Private Network'
            }
            cls._cache[ip] = result
            return result
        
        # Query external API
        try:
            response = requests.get(
                f'http://ip-api.com/json/{ip}',
                timeout=2
            )
            if response.status_code == 200:
                data = response.json()
                result = {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon')
                }
                cls._cache[ip] = result
                return result
        except Exception as e:
            print(f"[!] Geolocation error for {ip}: {e}")
        
        # Fallback
        result = {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
        cls._cache[ip] = result
        return result
    
    @staticmethod
    def _is_private_ip(ip: str) -> bool:
        """Check if IP is in private range"""
        return (
            ip.startswith('127.') or
            ip.startswith('192.168.') or
            ip.startswith('10.') or
            ip.startswith('172.')
        )
