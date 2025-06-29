#!/usr/bin/env python3
"""
Auto-Scaling Demo for Distributed RAG System

This script demonstrates the intelligent auto-scaling capabilities of the distributed
vector storage system. It shows how the system automatically adds and removes nodes
based on performance metrics and load conditions.
"""

import asyncio
import time
import requests
import json
import random
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
DEMO_DURATION = 300  # 5 minutes
METRICS_INTERVAL = 10  # seconds

class AutoScalingDemo:
    """Demo class for showcasing auto-scaling functionality."""
    
    def __init__(self):
        self.api_base = API_BASE_URL
        self.demo_start_time = time.time()
        self.metrics_history = []
        
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "="*60)
        print(f"🚀 {title}")
        print("="*60)
    
    def print_section(self, title: str):
        """Print a formatted section."""
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def print_metric(self, name: str, value: Any, unit: str = ""):
        """Print a formatted metric."""
        if isinstance(value, float):
            print(f"  {name}: {value:.2f}{unit}")
        else:
            print(f"  {name}: {value}{unit}")
    
    async def check_system_health(self) -> bool:
        """Check if the system is healthy and ready."""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ System Status: {data['status']}")
                return True
            else:
                print(f"❌ System unhealthy: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to system: {e}")
            return False
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get current cluster status."""
        try:
            response = requests.get(f"{self.api_base}/cluster/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get cluster status: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error getting cluster status: {e}")
            return {}
    
    async def get_autoscaling_status(self) -> Dict[str, Any]:
        """Get current auto-scaling status."""
        try:
            response = requests.get(f"{self.api_base}/autoscaling/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get auto-scaling status: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error getting auto-scaling status: {e}")
            return {}
    
    async def start_autoscaling(self) -> bool:
        """Start the auto-scaling system."""
        try:
            response = requests.post(f"{self.api_base}/autoscaling/start", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Auto-scaling: {data['message']}")
                return True
            else:
                print(f"❌ Failed to start auto-scaling: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error starting auto-scaling: {e}")
            return False
    
    async def stop_autoscaling(self) -> bool:
        """Stop the auto-scaling system."""
        try:
            response = requests.post(f"{self.api_base}/autoscaling/stop", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Auto-scaling: {data['message']}")
                return True
            else:
                print(f"❌ Failed to stop auto-scaling: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error stopping auto-scaling: {e}")
            return False
    
    async def update_thresholds(self, thresholds: Dict[str, Any]) -> bool:
        """Update auto-scaling thresholds."""
        try:
            response = requests.post(
                f"{self.api_base}/autoscaling/thresholds",
                json=thresholds,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Thresholds updated: {data['message']}")
                return True
            else:
                print(f"❌ Failed to update thresholds: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error updating thresholds: {e}")
            return False
    
    async def manual_scale_up(self) -> bool:
        """Manually trigger scale up."""
        try:
            response = requests.post(f"{self.api_base}/autoscaling/scale-up", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Manual scale up: {data['message']}")
                return True
            else:
                print(f"❌ Failed to scale up: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error scaling up: {e}")
            return False
    
    async def manual_scale_down(self) -> bool:
        """Manually trigger scale down."""
        try:
            response = requests.post(f"{self.api_base}/autoscaling/scale-down", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Manual scale down: {data['message']}")
                return True
            else:
                print(f"❌ Failed to scale down: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error scaling down: {e}")
            return False
    
    async def simulate_load(self, duration: int = 30):
        """Simulate load by making multiple requests."""
        print(f"\n🔥 Simulating load for {duration} seconds...")
        
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration:
            try:
                # Make various API calls to simulate load
                requests.get(f"{self.api_base}/health", timeout=2)
                requests.get(f"{self.api_base}/cluster/status", timeout=2)
                requests.get(f"{self.api_base}/indexes", timeout=2)
                
                # Simulate search requests
                search_payload = {
                    "query": f"test query {random.randint(1, 1000)}",
                    "limit": 5
                }
                requests.post(f"{self.api_base}/search", json=search_payload, timeout=2)
                
                request_count += 4
                await asyncio.sleep(0.5)  # 2 requests per second
                
            except Exception as e:
                print(f"⚠️  Load simulation error: {e}")
                await asyncio.sleep(1)
        
        print(f"✅ Load simulation complete: {request_count} requests made")
    
    def display_cluster_status(self, status: Dict[str, Any]):
        """Display formatted cluster status."""
        if not status:
            print("❌ No cluster status available")
            return
        
        print(f"📊 Cluster Status:")
        self.print_metric("Total Nodes", status.get("total_nodes", 0))
        self.print_metric("Healthy Nodes", status.get("healthy_nodes", 0))
        self.print_metric("Total Shards", status.get("total_shards", 0))
        self.print_metric("Total Collections", status.get("total_collections", 0))
        self.print_metric("Total Vectors", status.get("total_vectors", 0))
        self.print_metric("Replication Factor", status.get("replication_factor", 0))
        self.print_metric("Consistency Level", status.get("consistency_level", "unknown"))
        
        # Display node details
        nodes = status.get("nodes", [])
        if nodes:
            print(f"\n🖥️  Node Details:")
            for node in nodes:
                print(f"  Node {node['id']}: {node['status']} (Load: {node['load']:.2f}, Vectors: {node['vector_count']})")
    
    def display_autoscaling_status(self, status: Dict[str, Any]):
        """Display formatted auto-scaling status."""
        if not status:
            print("❌ No auto-scaling status available")
            return
        
        print(f"🤖 Auto-Scaling Status:")
        self.print_metric("Running", status.get("is_running", False))
        self.print_metric("Last Scale Up", time.strftime("%H:%M:%S", time.localtime(status.get("last_scale_up", 0))))
        self.print_metric("Last Scale Down", time.strftime("%H:%M:%S", time.localtime(status.get("last_scale_down", 0))))
        
        # Display thresholds
        thresholds = status.get("thresholds", {})
        if thresholds:
            print(f"\n⚙️  Scaling Thresholds:")
            self.print_metric("CPU High", thresholds.get("cpu_threshold_high", 0), "")
            self.print_metric("Memory High", thresholds.get("memory_threshold_high", 0), "")
            self.print_metric("Latency High", thresholds.get("latency_threshold_high", 0), "ms")
            self.print_metric("Min Nodes", thresholds.get("min_nodes", 0))
            self.print_metric("Max Nodes", thresholds.get("max_nodes", 0))
        
        # Display recent scaling history
        history = status.get("scaling_history", [])
        if history:
            print(f"\n📈 Recent Scaling Actions:")
            for action in history[-3:]:  # Last 3 actions
                timestamp = time.strftime("%H:%M:%S", time.localtime(action.get("timestamp", 0)))
                print(f"  {timestamp}: {action.get('action', 'unknown')} - {action.get('reason', 'no reason')}")
    
    async def run_demo(self):
        """Run the complete auto-scaling demo."""
        self.print_header("AUTO-SCALING DEMO FOR DISTRIBUTED RAG SYSTEM")
        
        # Step 1: Check system health
        self.print_section("Step 1: System Health Check")
        if not await self.check_system_health():
            print("❌ System is not healthy. Please ensure all services are running.")
            return
        
        # Step 2: Display initial cluster status
        self.print_section("Step 2: Initial Cluster Status")
        initial_status = await self.get_cluster_status()
        self.display_cluster_status(initial_status)
        
        # Step 3: Configure auto-scaling thresholds for demo
        self.print_section("Step 3: Configure Auto-Scaling Thresholds")
        demo_thresholds = {
            "cpu_threshold_high": 0.3,  # Lower for demo
            "memory_threshold_high": 0.4,  # Lower for demo
            "latency_threshold_high": 200.0,  # Lower for demo
            "min_nodes": 3,
            "max_nodes": 6,  # Limit for demo
            "scale_up_cooldown": 30,  # Shorter for demo
            "scale_down_cooldown": 60  # Shorter for demo
        }
        await self.update_thresholds(demo_thresholds)
        
        # Step 4: Start auto-scaling
        self.print_section("Step 4: Start Auto-Scaling")
        await self.start_autoscaling()
        
        # Step 5: Monitor and simulate load
        self.print_section("Step 5: Load Simulation and Monitoring")
        print("🔄 Starting monitoring loop...")
        
        monitoring_start = time.time()
        while time.time() - monitoring_start < DEMO_DURATION:
            current_time = time.time() - monitoring_start
            
            # Display current status every 30 seconds
            if int(current_time) % 30 == 0:
                print(f"\n⏰ Demo Time: {int(current_time)}s / {DEMO_DURATION}s")
                
                # Get current status
                cluster_status = await self.get_cluster_status()
                autoscaling_status = await self.get_autoscaling_status()
                
                self.display_cluster_status(cluster_status)
                self.display_autoscaling_status(autoscaling_status)
                
                # Store metrics for analysis
                self.metrics_history.append({
                    "timestamp": current_time,
                    "cluster_status": cluster_status,
                    "autoscaling_status": autoscaling_status
                })
            
            # Simulate load at different intervals
            if int(current_time) % 60 == 0:  # Every minute
                await self.simulate_load(20)  # 20 seconds of load
            
            await asyncio.sleep(METRICS_INTERVAL)
        
        # Step 6: Manual scaling demonstration
        self.print_section("Step 6: Manual Scaling Demonstration")
        print("🔄 Demonstrating manual scale up...")
        await asyncio.sleep(2)
        await self.manual_scale_up()
        
        await asyncio.sleep(5)
        print("🔄 Demonstrating manual scale down...")
        await self.manual_scale_down()
        
        # Step 7: Final status
        self.print_section("Step 7: Final System Status")
        final_cluster_status = await self.get_cluster_status()
        final_autoscaling_status = await self.get_autoscaling_status()
        
        self.display_cluster_status(final_cluster_status)
        self.display_autoscaling_status(final_autoscaling_status)
        
        # Step 8: Stop auto-scaling
        self.print_section("Step 8: Stop Auto-Scaling")
        await self.stop_autoscaling()
        
        # Step 9: Demo summary
        self.print_section("Demo Summary")
        print("🎉 Auto-scaling demo completed!")
        print(f"📊 Metrics collected: {len(self.metrics_history)} data points")
        print(f"⏱️  Total demo time: {DEMO_DURATION} seconds")
        
        # Show scaling events
        scaling_events = []
        for metric in self.metrics_history:
            history = metric.get("autoscaling_status", {}).get("scaling_history", [])
            scaling_events.extend(history)
        
        if scaling_events:
            print(f"🔄 Scaling events during demo: {len(scaling_events)}")
            for event in scaling_events[-5:]:  # Last 5 events
                timestamp = time.strftime("%H:%M:%S", time.localtime(event.get("timestamp", 0)))
                print(f"  {timestamp}: {event.get('action', 'unknown')} - {event.get('reason', 'no reason')}")
        else:
            print("ℹ️  No automatic scaling events occurred during demo")
        
        print("\n💡 Key Features Demonstrated:")
        print("  ✅ Real-time performance monitoring")
        print("  ✅ Automatic node scaling based on metrics")
        print("  ✅ Configurable scaling thresholds")
        print("  ✅ Manual scaling controls")
        print("  ✅ Scaling history and analytics")
        print("  ✅ Fault-tolerant distributed architecture")

async def main():
    """Main demo function."""
    demo = AutoScalingDemo()
    await demo.run_demo()

if __name__ == "__main__":
    print("🚀 Starting Auto-Scaling Demo...")
    print("📋 Make sure your distributed RAG system is running:")
    print("   1. Vector nodes (ports 8001, 8002, 8003)")
    print("   2. Main API server (port 8000)")
    print("   3. All services healthy")
    print("\n⏳ Starting demo in 5 seconds...")
    
    time.sleep(5)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    
    print("\n�� Demo completed!")