
# NTS proxy

A HTTP proxy specifically for handling authentication on the Nationale Terminologieserver. Copied from https://github.com/Nictiz/snippets/tree/main

## Prerequisites

- Docker and Docker Compose installed
- NTS credentials (username and password)
- Java JDK installed

## Setup

### 1. Set Environment Variables

Set your NTS credentials as environment variables:

**PowerShell:**
```powershell
$env:NTS_USER="your-username"
$env:NTS_PASS="your-password"
```

**Command Prompt:**
```cmd
set NTS_USER=your-username
set NTS_PASS=your-password
```

### 2. Start the Proxy

From the project root directory:
```powershell
cd util\NTS-proxy
docker-compose up -d --build
```

The proxy will run on `localhost:8080`.

### 3. Install mitmproxy Certificate

Since the IG Publisher uses HTTPS connections, you need to install the mitmproxy certificate into Java's truststore:

**Run as Administrator:**
```cmd
cd util\NTS-proxy
install-cert.bat
```

This will:
- Extract the certificate from the Docker container
- Find your Java installation
- Import the certificate into Java's truststore (default password: `changeit`)

## Usage

### Building the Implementation Guide

Use the `_genonce_nts.bat` script from the project root:
```cmd
_genonce_nts.bat
```

This script automatically:
- Configures Java to use the NTS proxy via system properties
- Connects to https://terminologieserver.nl/fhir through the proxy with authentication

### Manual Usage with HL7 Validator

If you want to use the validator directly:
```cmd
set JAVA_TOOL_OPTIONS=-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8080 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=8080
java -jar validator_cli.jar -tx https://terminologieserver.nl/fhir
```

## How It Works

1. **System-wide proxy**: Java is configured to route ALL HTTP/HTTPS traffic through localhost:8080
2. **mitmproxy intercepts**: The proxy intercepts HTTPS requests to `terminologieserver.nl`
3. **Authentication**: Adds OAuth2 Bearer token using your NTS credentials
4. **URL rewriting**: Converts HTTPS URLs in responses back to HTTP to ensure continued proxy usage
5. **Returns response**: Sends authenticated response back to the FHIR validator

The key is using Java system properties (`-Dhttp.proxyHost`, `-Dhttps.proxyHost`) to ensure ALL requests go through the proxy, not just those the validator explicitly sends through its `-proxy` parameter.

## Troubleshooting

### Certificate Issues

If you see SSL/certificate errors:
- Ensure you've run `install-cert.bat` as Administrator
- Verify the certificate was installed: Check for "mitmproxy" alias in Java's cacerts

### Proxy Not Working

Check if the proxy container is running:
```powershell
docker ps
```

View proxy logs:
```powershell
docker logs nts-proxy-nts-proxy-1
```

### Environment Variables Not Set

Ensure NTS_USER and NTS_PASS are set before starting docker-compose:
```powershell
Get-ChildItem Env: | Where-Object Name -like "*NTS*"
```

## Stopping the Proxy

```powershell
cd util\NTS-proxy
docker-compose down
```