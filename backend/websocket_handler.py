import asyncio
import json
from typing import Set, Callable, Dict, Any
from backend.logger import FarBotLogger

class WebSocketHandler:
    """Handles WebSocket connections for real-time updates"""
    
    def __init__(self, logger: FarBotLogger):
        self.logger = logger
        self.clients: Set = set()
        self.subscriptions: Dict[str, Set] = {}
    
    def add_client(self, client_id: str):
        """Add a client connection"""
        self.clients.add(client_id)
        self.logger.debug(f"Client connected: {client_id}")
    
    def remove_client(self, client_id: str):
        """Remove a client connection"""
        self.clients.discard(client_id)
        self.logger.debug(f"Client disconnected: {client_id}")
    
    def subscribe(self, client_id: str, topic: str):
        """Subscribe client to topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(client_id)
    
    def unsubscribe(self, client_id: str, topic: str):
        """Unsubscribe client from topic"""
        if topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)
    
    async def broadcast(self, topic: str, event: str, data: Any = None):
        """Broadcast message to subscribers"""
        if topic not in self.subscriptions:
            return
        
        message = {
            'type': 'event',
            'topic': topic,
            'event': event,
            'data': data
        }
        
        self.logger.debug(f"Broadcasting to {len(self.subscriptions[topic])} clients: {event}")
    
    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client"""
        if client_id in self.clients:
            self.logger.debug(f"Sending to {client_id}: {message['event']}")
