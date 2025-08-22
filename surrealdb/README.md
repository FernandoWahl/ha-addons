# SurrealDB Add-on for Home Assistant

![SurrealDB Logo](https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/black%20logo.svg)

## About

SurrealDB is a scalable, distributed, collaborative, document-graph database, designed for the realtime web. This add-on provides a SurrealDB instance that can be used by other Home Assistant add-ons, particularly the Open Notebook add-on.

## Features

- 🗄️ **Multi-model database** - Document, Graph, and Key-Value in one
- 🚀 **Real-time subscriptions** - Live queries and real-time updates
- 🔒 **Built-in security** - Authentication and authorization
- 📊 **ACID transactions** - Full ACID compliance
- 🌐 **WebSocket & HTTP APIs** - Multiple connection methods
- 💾 **Flexible storage** - Memory, File, or TiKV backends

## Installation

1. Navigate to Supervisor → Add-on Store
2. Add this repository: `https://github.com/FernandoWahl/ha-addons`
3. Find "SurrealDB" in the add-on list
4. Click "Install"
5. Configure the add-on (see Configuration section)
6. Start the add-on

## Configuration

### Basic Configuration

```yaml
username: "root"
password: "your_secure_password"
database: "open_notebook"
bind_address: "0.0.0.0:8000"
log_level: "info"
auth_enabled: true
storage_type: "memory"
data_path: "/data/surrealdb"
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `username` | string | `root` | Database username |
| `password` | password | `root` | Database password |
| `database` | string | `open_notebook` | Default database name |
| `bind_address` | string | `0.0.0.0:8000` | Address and port to bind |
| `log_level` | list | `info` | Logging level (trace, debug, info, warn, error) |
| `auth_enabled` | bool | `true` | Enable authentication |
| `storage_type` | list | `memory` | Storage backend (memory, file, tikv) |
| `data_path` | string | `/data/surrealdb` | Path for file storage |

### Storage Types

#### Memory Storage (Default)
- **Pros**: Fastest performance, no disk I/O
- **Cons**: Data lost on restart
- **Use case**: Development, testing, temporary data

#### File Storage
- **Pros**: Persistent data, good performance
- **Cons**: Single node only
- **Use case**: Production single-instance deployments

#### TiKV Storage
- **Pros**: Distributed, highly available
- **Cons**: Requires TiKV cluster
- **Use case**: Large-scale production deployments

## Usage

### Connecting from Other Add-ons

Other Home Assistant add-ons can connect to SurrealDB using:

**WebSocket Connection:**
```
ws://addon_surrealdb:8000/rpc
```

**HTTP API:**
```
http://addon_surrealdb:8000
```

### Health Check

The add-on provides a health endpoint:
```
http://addon_surrealdb:8000/health
```

### Example Connection (Python)

```python
from surrealdb import Surreal

async def connect_to_surrealdb():
    db = Surreal("ws://addon_surrealdb:8000/rpc")
    await db.connect()
    await db.signin({
        "user": "root",
        "pass": "your_password"
    })
    await db.use("open_notebook", "main")
    return db
```

## Integration with Open Notebook

This SurrealDB add-on is designed to work seamlessly with the Open Notebook add-on:

1. **Install SurrealDB** add-on first
2. **Configure** username/password
3. **Start** SurrealDB add-on
4. **Configure Open Notebook** to use external SurrealDB:
   ```yaml
   surrealdb_host: "addon_surrealdb"
   surrealdb_port: 8000
   surrealdb_user: "root"
   surrealdb_password: "your_password"
   ```

## Ports

- **8000/tcp**: SurrealDB WebSocket and HTTP API

## Data Persistence

When using file storage (`storage_type: "file"`), data is persisted in the `/data/surrealdb` directory, which is mapped to Home Assistant's data directory.

## Security

- Change the default password in production
- Use strong passwords for the database user
- Consider network security if exposing ports
- Authentication is enabled by default

## Troubleshooting

### Connection Issues
- Ensure the add-on is running and healthy
- Check the logs for any error messages
- Verify network connectivity between add-ons

### Performance Issues
- Consider switching from memory to file storage for large datasets
- Monitor resource usage in Home Assistant
- Adjust log level to reduce I/O if needed

### Data Loss
- Use file storage for data persistence
- Regular backups are recommended
- Memory storage loses data on restart

## Support

For issues and feature requests, please use the [GitHub repository](https://github.com/FernandoWahl/ha-addons).

## License

This add-on is licensed under the MIT License. SurrealDB itself is licensed under the Business Source License.
