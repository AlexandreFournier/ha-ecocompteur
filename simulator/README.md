# Ecocompteur API Simulator

A dockerized HTTP server that simulates the Ecocompteur API for testing and development purposes.

## Features

- Simulates all Ecocompteur API endpoints
- Dynamic real-time data generation
- Realistic power consumption values
- Easy Docker deployment
- Web interface for endpoint testing

## API Endpoints

| Endpoint | Description | Format |
|----------|-------------|--------|
| `/data.json` | General configuration and consumption data | JSON |
| `/inst.json` | Real-time instantaneous data (updates dynamically) | JSON |
| `/log1.csv` | Hourly statistics | CSV |
| `/log2.csv` | Daily statistics | CSV |

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts **two simulators** by default:
- **Simulator 1**: `http://172.28.0.10` or `http://localhost:8081`
- **Simulator 2**: `http://172.28.0.11` or `http://localhost:8082`

### Using Docker

Build the image:
```bash
docker build -t ecocompteur-simulator .
```

Run the container:
```bash
docker run -d -p 8080:80 --name ecocompteur-simulator ecocompteur-simulator
```

### Running Locally (without Docker)

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python app.py
```

The simulator will be available at `http://localhost:80`

## Testing with Home Assistant

To use this simulator with the Home Assistant Ecocompteur integration:

1. Start the simulators: `docker-compose up -d`
2. Configure in `configuration.yaml`:

```yaml
sensor:
  # First Ecocompteur simulator
  - platform: ecocompteur
    name: "Ecocompteur 1"
    host: "172.28.0.10"
    # or use: host: "localhost:8081"

  # Second Ecocompteur simulator
  - platform: ecocompteur
    name: "Ecocompteur 2"
    host: "172.28.0.11"
    # or use: host: "localhost:8082"
```

## Adding More Simulators

To add a third (or more) simulator, edit `docker-compose.yml` and add another service:

```yaml
  ecocompteur-simulator-3:
    build: .
    container_name: ecocompteur-simulator-3
    networks:
      ecocompteur_net:
        ipv4_address: 172.28.0.12
    ports:
      - "8083:80"
    restart: unless-stopped
```

Available IP range: `172.28.0.2` to `172.28.255.254`

## Data Characteristics

- **Real-time data** (`/inst.json`): Values change on each request to simulate live readings
- **Power consumption**: Randomly varies between 150-300W to simulate realistic usage
- **Timestamps**: Uses current system time
- **Configuration data** (`/data.json`): Static configuration matching typical Ecocompteur setup

## Network Configuration

The simulators run on a custom Docker network:
- **Network name**: `simulator_ecocompteur_net`
- **Subnet**: `172.28.0.0/16`
- **Gateway**: `172.28.0.1`

### Accessing from Other Containers

To access the simulators from another container (like a devcontainer), connect it to the network:

```bash
# From host machine
docker network connect simulator_ecocompteur_net <container-name-or-id>
```

Or add to your container's configuration:
```json
"runArgs": ["--network=simulator_ecocompteur_net"]
```

## Development

To modify the simulated data:

1. Edit `app.py`
2. Rebuild: `docker-compose build`
3. Restart: `docker-compose up -d`

## Stopping the Simulator

```bash
docker-compose down
```

Or if using Docker directly:
```bash
docker stop ecocompteur-simulator
docker rm ecocompteur-simulator
```

## Health Check

The simulator includes a health check that verifies the `/data.json` endpoint is responding. You can check the container status with:

```bash
docker-compose ps
```

## License

Same as the main ha-ecocompteur project.
