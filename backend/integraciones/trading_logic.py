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

import pandas as pd
import numpy as np
import ta
from typing import Dict, Optional
from datetime import datetime
from .brokers import BinanceAPI
from estrategias.models import Estrategia
from senales.models import Senal
# Agregar esta importación que falta
from operaciones.models import Operacion


class TradingEngine:
    def __init__(self):
        self.broker = BinanceAPI()
    
    def calculate_rsi(self, data, period=14):
        """Calcular RSI usando la librería 'ta'"""
        return ta.momentum.RSIIndicator(close=data, window=period).rsi()
    
    def calculate_sma(self, data, period=20):
        """Calcular SMA (Media Móvil Simple)"""
        return ta.trend.SMAIndicator(close=data, window=period).sma_indicator()
    
    def calculate_ema(self, data, period=20):
        """Calcular EMA (Media Móvil Exponencial)"""
        return ta.trend.EMAIndicator(close=data, window=period).ema_indicator()
    
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """Calcular MACD"""
        macd_indicator = ta.trend.MACD(close=data, window_fast=fast, window_slow=slow, window_sign=signal)
        macd_line = macd_indicator.macd()
        macd_signal = macd_indicator.macd_signal()
        macd_histogram = macd_indicator.macd_diff()
        
        return macd_line, macd_signal, macd_histogram
    
    def calculate_bollinger_bands(self, data, period=20, std=2):
        """Calcular Bandas de Bollinger"""
        bb_indicator = ta.volatility.BollingerBands(close=data, window=period, window_dev=std)
        bb_high = bb_indicator.bollinger_hband()
        bb_mid = bb_indicator.bollinger_mavg()
        bb_low = bb_indicator.bollinger_lband()
        
        return bb_high, bb_mid, bb_low
    
    def calculate_stochastic(self, high, low, close, k_period=14, d_period=3):
        """Calcular Oscilador Estocástico"""
        stoch_indicator = ta.momentum.StochasticOscillator(
            high=high, low=low, close=close, 
            window=k_period, smooth_window=d_period
        )
        stoch_k = stoch_indicator.stoch()
        stoch_d = stoch_indicator.stoch_signal()
        
        return stoch_k, stoch_d
    
    def procesar_estrategia(self, estrategia: Estrategia) -> Optional[Senal]:
        """Procesar una estrategia y generar señales"""
        try:
            # Obtener datos del mercado
            data = self.broker.get_historical_data(
                symbol='BTCUSDT',  # Ejemplo con BTC/USDT
                timeframe=estrategia.timeframe,
                limit=100
            )
            
            if not data:
                return None
            
            df = pd.DataFrame(data)
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            
            # Calcular indicadores según configuración
            indicadores_valores = {}
            
            if 'rsi' in estrategia.indicadores:
                periodo = estrategia.indicadores['rsi']['periodo']
                df['rsi'] = self.calculate_rsi(df['close'], period=periodo)
                indicadores_valores['rsi'] = float(df['rsi'].iloc[-1])
            
            if 'sma' in estrategia.indicadores:
                periodo = estrategia.indicadores['sma']['periodo']
                df['sma'] = self.calculate_sma(df['close'], period=periodo)
                indicadores_valores['sma'] = float(df['sma'].iloc[-1])
            
            if 'ema' in estrategia.indicadores:
                periodo = estrategia.indicadores['ema']['periodo']
                df['ema'] = self.calculate_ema(df['close'], period=periodo)
                indicadores_valores['ema'] = float(df['ema'].iloc[-1])
            
            if 'macd' in estrategia.indicadores:
                macd_line, macd_signal, macd_histogram = self.calculate_macd(df['close'])
                df['macd'] = macd_line
                df['macd_signal'] = macd_signal
                df['macd_histogram'] = macd_histogram
                indicadores_valores['macd'] = float(df['macd'].iloc[-1])
                indicadores_valores['macd_signal'] = float(df['macd_signal'].iloc[-1])
            
            if 'bollinger' in estrategia.indicadores:
                bb_high, bb_mid, bb_low = self.calculate_bollinger_bands(df['close'])
                df['bb_high'] = bb_high
                df['bb_mid'] = bb_mid
                df['bb_low'] = bb_low
                indicadores_valores['bb_high'] = float(df['bb_high'].iloc[-1])
                indicadores_valores['bb_mid'] = float(df['bb_mid'].iloc[-1])
                indicadores_valores['bb_low'] = float(df['bb_low'].iloc[-1])
            
            # Lógica de generación de señales
            ultimo = df.iloc[-1]
            tipo_senal = self._evaluar_condiciones_senal(ultimo, estrategia)
            
            if tipo_senal:
                return Senal.objects.create(
                    estrategia=estrategia,
                    simbolo='BTCUSDT',
                    tipo=tipo_senal,
                    precio=ultimo['close'],
                    indicadores_valores=indicadores_valores
                )
            
            return None
            
        except Exception as e:
            print(f"Error procesando estrategia {estrategia.id}: {e}")
            return None
    
    def _evaluar_condiciones_senal(self, ultimo_dato: pd.Series, estrategia: Estrategia) -> Optional[str]:
        """Evaluar las condiciones para generar una señal"""
        # Verificar condiciones de RSI
        if 'rsi' in estrategia.indicadores:
            rsi_config = estrategia.indicadores['rsi']
            rsi_actual = ultimo_dato.get('rsi')
            
            if pd.notna(rsi_actual):
                if rsi_actual < rsi_config.get('compra', 30):
                    return 'BUY'
                elif rsi_actual > rsi_config.get('venta', 70):
                    return 'SELL'
        
        # Verificar condiciones de MACD
        if 'macd' in estrategia.indicadores:
            macd_actual = ultimo_dato.get('macd')
            macd_signal = ultimo_dato.get('macd_signal')
            
            if pd.notna(macd_actual) and pd.notna(macd_signal):
                if macd_actual > macd_signal:
                    return 'BUY'
                elif macd_actual < macd_signal:
                    return 'SELL'
        
        # Agregar más condiciones según tus estrategias...
        
        return None
    
    def ejecutar_senal(self, senal: Senal) -> bool:
        """Ejecutar una señal de trading"""
        if senal.procesada:
            return False
        
        try:
            order = self.broker.place_order(
                symbol=senal.simbolo,
                side=senal.tipo.lower(),  # 'buy' o 'sell'
                quantity=self.calcular_cantidad(senal),
                price=str(senal.precio)
            )
            
            if order and order.get('status') == 'FILLED':
                # Registrar la operación
                Operacion.objects.create(
                    estrategia=senal.estrategia,
                    simbolo=senal.simbolo,
                    tipo=senal.tipo,
                    precio_entrada=senal.precio,
                    cantidad=float(order['executedQty']),
                    estado='OPEN',
                    stop_loss=self.calcular_stop_loss(senal),
                    take_profit=self.calcular_take_profit(senal)
                )
                senal.procesada = True
                senal.save()
                return True
                
        except Exception as e:
            print(f"Error ejecutando señal {senal.id}: {e}")
        
        return False
    
    def calcular_cantidad(self, senal: Senal) -> float:
        """Calcular la cantidad a operar basada en gestión de riesgo"""
        # Aquí puedes implementar lógica más sofisticada
        # Por ejemplo, basada en el porcentaje del capital, volatilidad, etc.
        return 0.001  # Ejemplo: 0.001 BTC
    
    def calcular_stop_loss(self, senal: Senal) -> float:
        """Calcular el precio de stop loss"""
        precio = float(senal.precio)
        # Ejemplo: 2% debajo/arriba del precio de entrada
        if senal.tipo == 'BUY':
            return precio * 0.98
        return precio * 1.02
    
    def calcular_take_profit(self, senal: Senal) -> float:
        """Calcular el precio de take profit"""
        precio = float(senal.precio)
        # Ejemplo: 4% arriba/abajo del precio de entrada
        if senal.tipo == 'BUY':
            return precio * 1.04
        return precio * 0.96
    
    def actualizar_operaciones_abiertas(self):
        """Actualizar el estado de las operaciones abiertas"""
        try:
            operaciones_abiertas = Operacion.objects.filter(estado='OPEN')
            
            for operacion in operaciones_abiertas:
                # Obtener precio actual
                precio_actual = self.broker.get_current_price(operacion.simbolo)
                
                if not precio_actual:
                    continue
                
                # Verificar stop loss y take profit
                if operacion.tipo == 'BUY':
                    if precio_actual <= operacion.stop_loss:
                        self._cerrar_operacion(operacion, precio_actual, 'STOP_LOSS')
                    elif precio_actual >= operacion.take_profit:
                        self._cerrar_operacion(operacion, precio_actual, 'TAKE_PROFIT')
                else:  # SELL
                    if precio_actual >= operacion.stop_loss:
                        self._cerrar_operacion(operacion, precio_actual, 'STOP_LOSS')
                    elif precio_actual <= operacion.take_profit:
                        self._cerrar_operacion(operacion, precio_actual, 'TAKE_PROFIT')
                        
        except Exception as e:
            print(f"Error actualizando operaciones: {e}")
    
    def _cerrar_operacion(self, operacion, precio_cierre: float, motivo: str):
        """Cerrar una operación"""
        try:
            # Ejecutar orden de cierre en el broker
            order = self.broker.place_order(
                symbol=operacion.simbolo,
                side='sell' if operacion.tipo == 'BUY' else 'buy',
                quantity=operacion.cantidad,
                price=str(precio_cierre)
            )
            
            if order and order.get('status') == 'FILLED':
                operacion.precio_salida = precio_cierre
                operacion.estado = 'CLOSED'
                operacion.motivo_cierre = motivo
                operacion.ganancia_perdida = self._calcular_pnl(operacion, precio_cierre)
                operacion.save()
                
        except Exception as e:
            print(f"Error cerrando operación {operacion.id}: {e}")
    
    def _calcular_pnl(self, operacion, precio_cierre: float) -> float:
        """Calcular ganancia/pérdida de una operación"""
        precio_entrada = float(operacion.precio_entrada)
        cantidad = float(operacion.cantidad)
        
        if operacion.tipo == 'BUY':
            return (precio_cierre - precio_entrada) * cantidad
        else:  # SELL
            return (precio_entrada - precio_cierre) * cantidad