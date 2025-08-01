# Deployment Guide

## Quick Start

### Local Development
```bash
# 1. Clone and setup
git clone <repository>
cd transcript_to_powerpoint

# 2. Set environment variables
export OPENAI_API_KEY=your-key-here

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run unified application
streamlit run app.py
```

**Access at:** http://localhost:8503

## Docker Deployment

### Option 1: Simple Docker
```bash
# Build image
docker build -t ai-transcript-suite .

# Run container (single port)
docker run -p 8503:8503 \
  -e OPENAI_API_KEY=your-key-here \
  ai-transcript-suite
```

### Option 2: Docker Compose (Recommended)
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Start service
docker-compose up -d

# With nginx proxy (optional)
docker-compose --profile proxy up -d
```

### Access Points
- **Unified App**: http://localhost:8503 (all features in one interface)
- **With Nginx**: http://localhost (if using proxy profile)

### Navigation
- **Hub Page**: Overview and app selection
- **OpenAI App**: Premium presentations with DALL-E 3 images
- **CrewAI App**: Cost-optimized text-only presentations
- **Sidebar Navigation**: Switch between apps seamlessly

## ☁️ AWS Deployment

### ECS with Application Load Balancer
1. **Build and push to ECR**:
```bash
# Create ECR repository
aws ecr create-repository --repository-name ai-transcript-suite

# Build and push
docker build -t ai-transcript-suite .
docker tag ai-transcript-suite:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-transcript-suite:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-transcript-suite:latest
```

2. **Create ECS cluster and services**:
   - Create 3 ECS services (hub, openai, crewai)
   - Configure ALB with path-based routing
   - Set environment variables in task definitions

3. **Configure ALB rules**:
   - `/` → hub service (port 8503)
   - `/openai/*` → openai service (port 8501)
   - `/crewai/*` → crewai service (port 8502)

### AWS App Runner
```bash
# Create apprunner.yaml in project root
cat > apprunner.yaml << EOF
version: 1.0
runtime: docker
build:
  commands:
    build:
      - echo "Build completed"
run:
  runtime-version: latest
  command: streamlit run app.py --server.port 8080 --server.address 0.0.0.0
  network:
    port: 8080
    env-vars:
      - name: OPENAI_API_KEY
        value: your-key-here
EOF
```

### EC2 with Docker Compose
1. **Launch EC2 instance** (t3.medium or larger)
2. **Install Docker and Docker Compose**
3. **Deploy**:
```bash
# Clone repository
git clone <repository>
cd transcript_to_powerpoint

# Set environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Start services
docker-compose up -d
```

## 🔒 Security Considerations

### Environment Variables
- Never commit API keys to git
- Use AWS Secrets Manager or similar for production
- Set up proper IAM roles for ECS tasks

### Network Security
- Configure security groups to allow only necessary ports
- Use HTTPS in production (configure SSL/TLS)
- Consider VPC setup for internal services

### Monitoring
- Set up CloudWatch logs for container monitoring
- Configure health checks for all services
- Set up alerting for service failures

## 📊 Scaling Considerations

### Horizontal Scaling
- Each app can be scaled independently
- Use ECS auto-scaling based on CPU/memory
- Consider using multiple availability zones

### Cost Optimization
- Use spot instances for non-critical workloads
- Configure auto-scaling to scale down during low usage
- Monitor OpenAI API usage and costs

## 🛠️ Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 8501, 8502, 8503 are available
2. **API key errors**: Verify OPENAI_API_KEY is set correctly
3. **Memory issues**: CrewAI app uses less memory; consider for resource-constrained environments

### Health Checks
```bash
# Check service health
curl http://localhost:8503/_stcore/health
curl http://localhost:8501/_stcore/health
curl http://localhost:8502/_stcore/health
```

### Logs
```bash
# Docker logs
docker logs ai-suite-hub
docker logs ai-suite-openai
docker logs ai-suite-crewai

# Docker Compose logs
docker-compose logs -f
```
