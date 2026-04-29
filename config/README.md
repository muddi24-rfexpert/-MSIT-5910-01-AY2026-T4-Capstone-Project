# config/README.md

# Configuration Files

This directory contains all configuration files for different environments and modules.

## Configuration Files

### Environment Configurations
- `config.dev.yaml` - Development environment configuration
- `config.test.yaml` - Testing environment configuration
- `config.prod.yaml` - Production environment configuration

### Module-Specific Configurations
- `drone_config.yaml` - Drone hardware and flight parameters
- `ai_models_config.yaml` - ML model training and inference parameters
- `connectivity_config.yaml` - 5G and satellite connectivity settings
- `edge_config.yaml` - Edge computing and processing parameters

### System Parameters
- `database_config.yaml` - Database connection settings
- `logging_config.yaml` - Logging configuration
- `api_config.yaml` - API server configuration

## Configuration Management

### Loading Configuration

```python
import yaml

with open('config/config.dev.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

### Environment Variables

Sensitive information (API keys, credentials) should be stored as environment variables:

```bash
export SATELLITE_API_KEY="your-api-key"
export DATABASE_PASSWORD="your-password"
```

## Configuration Best Practices

1. **Never commit sensitive data** - Use environment variables for secrets
2. **Version control** - Keep config templates in version control, not secrets
3. **Documentation** - Document all configuration options
4. **Environment-specific** - Maintain separate configs for dev, test, and production
