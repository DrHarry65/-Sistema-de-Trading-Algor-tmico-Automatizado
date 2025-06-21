# trading_logic.py
# Copyright (C) 2025 Alejandro Rodriguez
# This file is part of ProyectoNombre.
#
# ProyectoNombre is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ProyectoNombre is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from typing import List, Dict, Optional

class BinanceAPI:
    BASE_URL = "https://api.binance.com"
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    def _generate_signature(self, data: str) -> str:
        return hmac.new(
            self.secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def get_historical_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[List[Dict]]:
        endpoint = "/api/v3/klines"
        params = {
            'symbol': symbol.upper(),
            'interval': timeframe,
            'limit': limit
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            formatted_data = []
            for item in data:
                formatted_data.append({
                    'time': item[0] / 1000,  # Convertir a segundos
                    'open': float(item[1]),
                    'high': float(item[2]),
                    'low': float(item[3]),
                    'close': float(item[4]),
                    'volume': float(item[5]),
                    'close_time': item[6] / 1000,
                    'quote_volume': float(item[7]),
                    'count': item[8],
                })
            
            return formatted_data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
    
    def place_order(self, symbol: str, side: str, quantity: float, price: Optional[float] = None) -> Optional[Dict]:
        endpoint = "/api/v3/order"
        timestamp = int(time.time() * 1000)
        
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': 'LIMIT' if price else 'MARKET',
            'quantity': quantity,
            'timestamp': timestamp,
            'recvWindow': 5000
        }
        
        if price:
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        try:
            params['signature'] = self._generate_signature(urlencode(params))
            headers = {'X-MBX-APIKEY': self.api_key}
            
            response = requests.post(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                data=params
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error placing order: {e}")
            return None
    
    def get_account_info(self) -> Optional[Dict]:
        endpoint = "/api/v3/account"
        timestamp = int(time.time() * 1000)
        params = {'timestamp': timestamp}
        
        try:
            params['signature'] = self._generate_signature(urlencode(params))
            headers = {'X-MBX-APIKEY': self.api_key}
            
            response = requests.get(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None