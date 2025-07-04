"""
Simple Auto-Scaling System for Distributed RAG
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .distributed_storage_manager import DistributedStorageManager
from .distributed_vector_store import VectorNode

logger = logging.getLogger(__name__)

class ScalingAction(Enum):
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    MAINTAIN = "maintain"

@dataclass
class ScalingThresholds:
    """Configurable thresholds for scaling decisions."""
    cpu_threshold_high: float = 0.75
    memory_threshold_high: float = 0.80
    storage_threshold_high: float = 0.85
    latency_threshold_high: float = 1000.0
    error_rate_threshold_high: float = 0.05
    cpu_threshold_low: float = 0.30
    memory_threshold_low: float = 0.40
    storage_threshold_low: float = 0.50
    latency_threshold_low: float = 100.0
    error_rate_threshold_low: float = 0.01
    min_nodes: int = 3
    max_nodes: int = 10
    scale_up_cooldown: int = 300
    scale_down_cooldown: int = 600
    health_check_interval: int = 30

class AutoScaler:
    """Simple auto-scaler for distributed vector storage."""
    
    def __init__(self, storage_manager: DistributedStorageManager, thresholds: Optional[ScalingThresholds] = None):
        self.storage_manager = storage_manager
        self.thresholds = thresholds or ScalingThresholds()
        self.last_scale_up = 0
        self.last_scale_down = 0
        self.scaling_history: List[Dict] = []
        self.is_running = False
        
    async def start_monitoring(self):
        """Start the auto-scaling monitoring loop."""
        self.is_running = True
        logger.info("Starting auto-scaler monitoring")
        
        while self.is_running:
            try:
                await self._monitoring_cycle()
                await asyncio.sleep(self.thresholds.health_check_interval)
            except Exception as e:
                logger.error(f"Auto-scaler monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def stop_monitoring(self):
        """Stop the auto-scaling monitoring loop."""
        self.is_running = False
        logger.info("Stopped auto-scaler monitoring")
    
    async def _monitoring_cycle(self):
        """Single monitoring cycle."""
        try:
            # Get cluster status
            cluster_status = await self.storage_manager.get_cluster_status()
            node_count = cluster_status.get("total_nodes", 0)
            healthy_nodes = cluster_status.get("healthy_nodes", 0)
            
            # Simple scaling logic
            current_time = time.time()
            
            # Scale up if healthy nodes are low
            if (healthy_nodes < self.thresholds.min_nodes and 
                node_count < self.thresholds.max_nodes and
                current_time - self.last_scale_up > self.thresholds.scale_up_cooldown):
                await self._scale_up("Low healthy nodes", node_count)
            
            # Scale down if we have excess nodes
            elif (node_count > self.thresholds.min_nodes and
                  current_time - self.last_scale_down > self.thresholds.scale_down_cooldown):
                await self._scale_down("Excess capacity", node_count)
                
        except Exception as e:
            logger.error(f"Monitoring cycle error: {e}")
    
    async def _scale_up(self, reason: str, current_nodes: int):
        """Add a new node to the cluster."""
        try:
            new_node_id = f"node{current_nodes + 1}"
            new_port = 8000 + current_nodes + 1
            
            import subprocess
            import sys
            import os

            # Xác định script khởi động node mới (ví dụ: start_node4.py hoặc start_vector_node.py)
            script_path = os.path.join(os.path.dirname(__file__), "../../scripts/start_vector_node.py")
            script_path = os.path.abspath(script_path)

            # Khởi động process node mới (chạy ngầm)
            subprocess.Popen([
                sys.executable, script_path,
                "--node-id", new_node_id,
                "--host", "localhost",
                "--port", str(new_port)
            ])

            # Sau đó mới thêm metadata node vào cluster
            new_node = VectorNode(id=new_node_id, host="localhost", port=new_port)
            success = await self.storage_manager.add_node(new_node)
            
            if success:
                self.last_scale_up = time.time()
                logger.info(f"Successfully scaled UP: Added node {new_node_id}")
                
                self.scaling_history.append({
                    "timestamp": time.time(),
                    "action": "scale_up",
                    "reason": reason,
                    "node_id": new_node_id
                })
            else:
                logger.error(f"Failed to scale UP: Could not add node {new_node_id}")
                
        except Exception as e:
            logger.error(f"Error during scale UP: {e}")
    
    async def _scale_down(self, reason: str, current_nodes: int):
        """Remove a node from the cluster and migrate its data."""
        try:
            cluster_status = await self.storage_manager.get_cluster_status()
            nodes = cluster_status.get("nodes", [])

            # Không xóa node1, chỉ xóa khi còn nhiều hơn min_nodes
            removable_nodes = [n for n in nodes if n["id"] != "node1"]
            if len(removable_nodes) == 0 or current_nodes <= self.thresholds.min_nodes:
                logger.info("No removable node or already at min_nodes")
                return

            # Chọn node ít vectors nhất để xóa
            node_to_remove = min(removable_nodes, key=lambda n: n["vector_count"])
            node_id = node_to_remove["id"]
            logger.info(f"Preparing to remove node {node_id}")

            # Di chuyển dữ liệu nếu có hàm migrate_shards_from_node
            if hasattr(self.storage_manager, "migrate_shards_from_node"):
                await self.storage_manager.migrate_shards_from_node(node_id)
            else:
                logger.warning("No migrate_shards_from_node method implemented, skipping migration!")

            # Xóa node khỏi cluster
            success = await self.storage_manager.remove_node(node_id)

            if success:
                # Gọi sharding lại sau khi xóa node
                await self.storage_manager.rebalance_shards()
                self.last_scale_down = time.time()
                logger.info(f"Successfully scaled DOWN: Removed node {node_id}")

                self.scaling_history.append({
                    "timestamp": time.time(),
                    "action": "scale_down",
                    "reason": reason,
                    "node_id": node_id
                })
            else:
                logger.error(f"Failed to scale DOWN: Could not remove node {node_id}")

        except Exception as e:
            logger.error(f"Error during scale DOWN: {e}")
    
    def get_scaling_status(self) -> Dict:
        """Get current scaling status and history."""
        return {
            "is_running": self.is_running,
            "last_scale_up": self.last_scale_up,
            "last_scale_down": self.last_scale_down,
            "scaling_history": self.scaling_history[-10:],
            "current_metrics": None,
            "thresholds": {
                "cpu_threshold_high": self.thresholds.cpu_threshold_high,
                "memory_threshold_high": self.thresholds.memory_threshold_high,
                "storage_threshold_high": self.thresholds.storage_threshold_high,
                "latency_threshold_high": self.thresholds.latency_threshold_high,
                "error_rate_threshold_high": self.thresholds.error_rate_threshold_high,
                "cpu_threshold_low": self.thresholds.cpu_threshold_low,
                "memory_threshold_low": self.thresholds.memory_threshold_low,
                "storage_threshold_low": self.thresholds.storage_threshold_low,
                "latency_threshold_low": self.thresholds.latency_threshold_low,
                "error_rate_threshold_low": self.thresholds.error_rate_threshold_low,
                "min_nodes": self.thresholds.min_nodes,
                "max_nodes": self.thresholds.max_nodes
            }
        }
    
    def update_thresholds(self, new_thresholds: ScalingThresholds):
        """Update scaling thresholds dynamically."""
        self.thresholds = new_thresholds
        logger.info("Updated auto-scaling thresholds")

def create_auto_scaler(storage_manager: DistributedStorageManager, 
                      custom_thresholds: Optional[ScalingThresholds] = None) -> AutoScaler:
    """Create an auto-scaler with the specified configuration."""
    return AutoScaler(storage_manager, custom_thresholds) 