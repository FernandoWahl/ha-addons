# Changelog

All notable changes to this project will be documented in this file.

## [1.1.2] - 2025-01-13

### 🧹 Code Cleanup
- Removed hardcoded IP addresses from diagnostic scripts
- Made test scripts more generic and reusable
- Enhanced Redis connection diagnostics with flexible host testing
- Improved configuration validation and error messages

### 🔧 Improvements
- Better Redis host validation in configuration loading
- Enhanced logging for configuration debugging
- More comprehensive test coverage for different Redis configurations
- Generic examples in diagnostic tools

### 🧪 Testing
- Updated all test scripts to version 1.1.2
- Improved test_redis_connection.py with generic host examples
- Enhanced test_ha_config.py with flexible configuration testing

## [1.1.1] - 2025-01-13

### 🔧 Fixed
- Fixed configuration loading from Home Assistant options
- Redis configuration changes now properly reflected in logs
- Implemented `/data/options.json` reading for HA integration

### 🆕 Added
- New `GET /config` endpoint to view current configuration
- Detailed Redis configuration logging on startup
- Fallback to environment variables for development mode

### 🧪 Testing
- New `test_config_loading.py` script for configuration testing
- Enhanced existing test scripts with version updates

## [1.1.0] - 2025-01-12

### 🆕 Added
- Redis caching with gzip compression
- Key-based image retrieval system
- `POST /combine` now returns JSON with unique key
- `GET /image/<key>` endpoint for image retrieval
- `redis_required` configuration for startup control
- Cache management endpoints (`/cache/stats`, `/cache/clear`)

### 🔧 Features
- Configurable TTL for cache (default: 600s)
- Automatic image compression in cache
- Performance logging with hit/miss ratios
- Graceful fallback when Redis unavailable

## [1.0.0] - 2025-07-12

### Added
- Initial release of Image Combiner Home Assistant Addon
- API endpoint to combine up to 4 images into a single composite image
- Configurable image quality, cell dimensions, and timeout
- Support for multiple image formats (JPEG, PNG, GIF, BMP)
- Automatic image resizing while maintaining aspect ratio
- Intelligent layout system (1, 2, 3, or 4 images)
- Health check endpoint
- Multi-architecture support (amd64, aarch64, armv7, armhf, i386)
- Portuguese and English translations
- Comprehensive error handling and validation
- Integration examples for Home Assistant automations
