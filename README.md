# RAG-LLM: Advanced Distributed Retrieval-Augmented Generation System

## 🚀 Overview

RAG-LLM is a comprehensive, production-ready distributed system for Retrieval-Augmented Generation that combines the power of large language models with intelligent document processing, CSV data analysis, and scalable vector storage. Built with FastAPI, it provides a unified API for processing multiple data types and generating AI-powered responses.

## ✨ Key Features

### 🔄 **Multi-Modal Data Processing**
- **Document Processing**: PDF, DOCX, TXT files with intelligent chunking
- **CSV Data Analysis**: SQL query generation and execution on CSV files
- **Image Processing**: OCR and image content extraction
- **Tabular Data**: Intelligent column analysis and data type inference

### 🏗️ **Distributed Architecture**
- **Peer-to-Peer Nodes**: No single point of failure
- **Sharding & Replication**: Automatic data distribution across nodes
- **Auto-Scaling**: Dynamic node addition/removal based on load
- **Health Monitoring**: Continuous cluster health checks

### 🤖 **AI-Powered Intelligence**
- **Unified `/ask` Endpoint**: Single endpoint for all data types
- **LLM Integration**: Gemini AI for intelligent responses
- **Smart Collection Management**: AI-driven document categorization
- **Context-Aware Responses**: Combines CSV data and documents seamlessly

### 📊 **Advanced Analytics**
- **Real-time Metrics**: Performance and health monitoring
- **Query Analysis**: Intelligent search optimization
- **Confidence Scoring**: Response reliability assessment
- **Source Attribution**: Transparent answer sources

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Coordinator                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Upload    │ │   Search    │ │     Ask     │          │
│  │   Service   │ │   Service   │ │   Service   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │    Types    │ │  Services   │ │    API      │          │
│  │ (Processors)│ │(Ingestion/  │ │ (Endpoints) │          │
│  │             │ │ Inference)  │ │             │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Storage   │ │ CSV DBs     │ │   Logs      │          │
│  │ (Distributed│ │ (SQLite)    │ │ (Monitoring)│          │
│  │  Vector DB) │ │             │ │             │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Distributed Vector Cluster                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Node 1  │ │ Node 2  │ │ Node 3  │ │ Node N  │          │
│  │(Shards) │ │(Shards) │ │(Shards) │ │(Shards) │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
rag-llm/
├── core/                          # Core application layer
│   ├── api/                       # FastAPI endpoints
│   │   └── main.py               # Main API application
│   ├── models/                    # Data models
│   │   ├── base.py               # Base document models
│   │   ├── csv_index.py          # CSV indexing models
│   │   ├── document.py           # Document models
│   │   └── ...
│   ├── services/                  # Business logic
│   │   ├── ingestion/            # Document processing
│   │   │   ├── chunker.py        # Text chunking
│   │   │   ├── extractor.py      # Content extraction
│   │   │   └── pipeline.py       # Processing pipeline
│   │   └── inference/            # AI services
│   │       ├── gemini_client.py  # Gemini AI integration
│   │       ├── query_analyzer.py # Query analysis
│   │       └── reasoning_engine.py # Reasoning logic
│   ├── types/                     # Data processors
│   │   ├── document_processor.py # Document handling
│   │   ├── image_processor.py    # Image processing
│   │   └── tabular_processor.py  # CSV/tabular data
│   └── utils/                     # Utilities
│       ├── logging.py            # Logging configuration
│       ├── encryption.py         # Security utilities
│       └── validation.py         # Data validation
├── data/                          # Data layer
│   ├── storage/                   # Storage management
│   │   ├── distributed_storage_manager.py
│   │   ├── distributed_vector_store.py
│   │   ├── csv_database.py       # CSV database manager
│   │   └── auto_scaler.py        # Auto-scaling logic
│   └── data/                      # Data storage
│       ├── csv_databases/         # SQLite CSV databases
│       ├── documents/             # Document storage
│       ├── images/                # Image storage
│       ├── node_data/             # Vector node data
│       └── logs/                  # Application logs
├── config/                        # Configuration
│   ├── config.py                  # Settings management
│   ├── docker-compose.yml         # Docker configuration
│   └── env.example                # Environment template
├── scripts/                       # Utility scripts
│   ├── start_node1.py            # Vector node starters
│   ├── start_node2.py
│   ├── start_node3.py
│   └── start_vector_nodes.py
├── demos/                         # Demo applications
│   ├── demo_autoscaling.py       # Auto-scaling demo
│   └── demo_distributed_system.py # System demo
├── docs/                          # Documentation
│   ├── architecture.md           # System architecture
│   ├── autoscaling.md            # Auto-scaling guide
│   ├── CSV_INDEXING.md           # CSV processing guide
│   └── ...
└── tests/                         # Test files
    └── example_usage.py          # Usage examples
```

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone the repository
git clone https://github.com/Nhakhoa02/rag-llm.git
cd rag-llm

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp config/env.example .env
# Edit .env with your configuration
```

### 2. **Start the System**

```bash
# Start vector nodes (in separate terminals)
python scripts/start_node1.py
python scripts/start_node2.py
python scripts/start_node3.py

# Start the main API server
python -m uvicorn core.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. **Upload and Query Data**

```bash
# Upload a document
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"

# Upload a CSV file
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_data.csv"

# Ask questions (unified endpoint)
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the sales figures for Q3?",
    "include_sources": true
  }'
```

## 🔧 API Endpoints

### **Core Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload documents, CSV files, or images |
| `/ask` | POST | **Unified endpoint** - Ask questions about all data types |
| `/search` | POST | Search documents by semantic similarity |
| `/ask_csv` | POST | CSV-specific questions with SQL execution |

### **Cluster Management**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cluster/status` | GET | Get cluster health and node status |
| `/autoscaling/status` | GET | Auto-scaling status and history |
| `/autoscaling/start` | POST | Start auto-scaling monitoring |
| `/autoscaling/scale-up` | POST | Manually trigger scale-up |
| `/autoscaling/scale-down` | POST | Manually trigger scale-down |

### **Monitoring & Debug**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/indexes` | GET | List all collections/indexes |
| `/debug/collections` | GET | Detailed collection information |
| `/csv_databases` | GET | List available CSV databases |

## 🎯 Key Capabilities

### **Unified `/ask` Endpoint**
The system's crown jewel - a single endpoint that:
- **Processes CSV data** with SQL queries and actual data values
- **Searches documents** for relevant information
- **Combines all sources** using AI to generate comprehensive answers
- **Provides confidence scores** and source attribution
- **Handles conflicts** intelligently between different data sources

### **Intelligent CSV Processing**
- **Automatic SQL generation** based on natural language questions
- **Real data execution** against CSV databases
- **Column analysis** and data type inference
- **Multi-CSV support** with relevance scoring

### **Distributed Vector Storage**
- **Sharding**: Data automatically distributed across nodes
- **Replication**: Each shard replicated for fault tolerance
- **Auto-scaling**: Dynamic node management
- **Health monitoring**: Continuous cluster health checks

### **AI-Powered Features**
- **Gemini AI integration** for intelligent responses
- **Smart collection management** using AI
- **Query analysis** and optimization
- **Context-aware reasoning** across multiple data types

## 🔍 Example Usage

### **CSV Data Analysis**
```python
# Upload a sales CSV file
response = requests.post("http://localhost:8000/upload", 
    files={"file": open("sales_data.csv", "rb")})

# Ask questions about the data
question = {
    "question": "What was the total revenue in Q3 2024?",
    "include_sources": True
}
response = requests.post("http://localhost:8000/ask", json=question)
```

### **Document Search**
```python
# Upload a technical document
response = requests.post("http://localhost:8000/upload", 
    files={"file": open("technical_guide.pdf", "rb")})

# Ask questions about the content
question = {
    "question": "How does the system handle authentication?",
    "include_sources": True
}
response = requests.post("http://localhost:8000/ask", json=question)
```

### **Combined Analysis**
```python
# The system automatically combines CSV data and documents
question = {
    "question": "Based on the sales data and technical documentation, what are the key factors affecting Q3 performance?",
    "include_sources": True
}
response = requests.post("http://localhost:8000/ask", json=question)
```

## 🛠️ Configuration

### **Environment Variables**
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Vector Store
VECTOR_SIZE=384
REPLICATION_FACTOR=2
SHARD_COUNT=8

# Auto-scaling
MIN_NODES=3
MAX_NODES=10
```

### **Auto-scaling Thresholds**
```python
# Update thresholds via API
curl -X POST "http://localhost:8000/autoscaling/thresholds" \
  -H "Content-Type: application/json" \
  -d '{
    "cpu_threshold_high": 0.75,
    "memory_threshold_high": 0.80,
    "min_nodes": 3,
    "max_nodes": 10
  }'
```

## 📊 Monitoring

### **Cluster Status**
```bash
curl http://localhost:8000/cluster/status
```

### **Auto-scaling Status**
```bash
curl http://localhost:8000/autoscaling/status
```

### **Health Check**
```bash
curl http://localhost:8000/health
```

## 🧪 Testing

### **Run Demos**
```bash
# Auto-scaling demo
python demos/demo_autoscaling.py

# Distributed system demo
python demos/demo_distributed_system.py
```

### **Test Endpoints**
```bash
# Test upload functionality
curl http://localhost:8000/debug/upload_test

# Test AI collection analysis
curl http://localhost:8000/debug/ai_collection_analysis

# Check CSV databases
curl http://localhost:8000/debug/csv_databases
```

## 🔧 Development

### **Project Structure Benefits**
- **Separation of Concerns**: Core logic separated from data storage
- **Modularity**: Easy to extend and maintain
- **Scalability**: Clear boundaries for scaling components
- **Testing**: Isolated components for better testing

### **Adding New Features**
1. **Core Layer**: Add new services in `core/services/`
2. **Data Layer**: Extend storage in `data/storage/`
3. **API Layer**: Add endpoints in `core/api/main.py`
4. **Types**: Add processors in `core/types/`

## 📈 Performance

- **Scalable**: Horizontal scaling with auto-scaling
- **Fault-tolerant**: Replication and health monitoring
- **Fast**: Distributed vector search
- **Intelligent**: AI-powered processing and responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the `docs/` folder for detailed guides
- **Examples**: See `tests/example_usage.py` for usage examples

---

**Built with ❤️ using FastAPI, Gemini AI, and distributed systems principles**
