
# NTS Proxy

HTTP proxy for handling OAuth2 authentication on the Dutch National Terminology Server (Nationale Terminologieserver).

Based on: https://github.com/Nictiz/snippets/tree/main

## Prerequisites

- Docker and Docker Compose V2
- NTS credentials (username and password) - [Request access](https://nictiz.atlassian.net/servicedesk/customer/portal/4)
- Java JDK 21+ (for certificate installation)

## Quick Start

### 1. Set Environment Variables

Set your NTS credentials as environment variables. These persist only for the current session:

**PowerShell:**
```powershell
$env:NTS_USER = "your-username"
$env:NTS_PASS = "your-password"
```

**Command Prompt:**
```cmd
set NTS_USER=your-username
set NTS_PASS=your-password
```

> **Tip**: For persistent credentials, add these to your system environment variables via Windows Settings.

### 2. Start the Proxy

Navigate to the proxy directory and start the container:

```powershell
cd util\NTS-proxy
docker compose up -d --build
```

The proxy runs on `localhost:8080` and intercepts requests to `terminologieserver.nl`.

Verify it's running:
```powershell
docker ps
docker logs nts-proxy-nts-proxy-1
```

### 3. Install mitmproxy Certificate

**⚠️ Required for HTTPS interception**

Run as Administrator:
```cmd
cd util\NTS-proxy
install-cert.bat
```

This script:
1. Extracts the mitmproxy CA certificate from the container
2. Locates your Java installation (via `JAVA_HOME`)
3. Imports the certificate into Java's truststore (`cacerts`)
4. Removes any existing certificate first to avoid conflicts

Default truststore password: `changeit`

## Usage

### Local Development: IG Publisher

Use the provided batch script from the project root:

```cmd
_genonce_nts.bat
```

This runs the IG Publisher with:
- `-proxy localhost:8080` - Routes requests through the proxy
- `-tx http://terminologieserver.nl/fhir` - Terminology server endpoint

The IG Publisher's HTTP client properly uses the `-proxy` parameter and routes all terminology validation through the authenticated proxy.

### CI/CD: GitHub Actions

The workflow automatically:
1. Starts the NTS proxy container
2. Installs the mitmproxy certificate into the GitHub runner's Java truststore
3. Sets Java system properties to force ALL HTTP/HTTPS traffic through the proxy:
   ```bash
   JAVA_TOOL_OPTIONS="-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8080 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=8080"
   ```
4. Runs the Java validator with `-tx https://terminologieserver.nl/fhir`

See `.github/workflows/r4_firely_terminal.yaml` for implementation details.

### Manual Usage: Standalone Java Validator

For direct validator usage:

**Windows (Command Prompt):**
```cmd
set JAVA_TOOL_OPTIONS=-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8080 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=8080
java -jar validator_cli.jar -tx https://terminologieserver.nl/fhir -ig input -txLog tx.log
```

**PowerShell:**
```powershell
$env:JAVA_TOOL_OPTIONS = "-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8080 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=8080"
java -jar validator_cli.jar -tx https://terminologieserver.nl/fhir -ig input -txLog tx.log
```

**Linux/macOS:**
```bash
export JAVA_TOOL_OPTIONS="-Dhttp.proxyHost=localhost -Dhttp.proxyPort=8080 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=8080"
java -jar validator_cli.jar -tx https://terminologieserver.nl/fhir -ig input -txLog tx.log
```

## How It Works

The proxy uses [mitmproxy](https://mitmproxy.org/) to intercept and modify HTTP/HTTPS traffic:

1. **Request interception**: mitmproxy intercepts HTTPS requests to `terminologieserver.nl`
2. **Token retrieval**: Authenticates with NTS using OAuth2 password grant flow
3. **Header injection**: Adds `Authorization: Bearer <token>` to each request
4. **URL rewriting**: Converts HTTPS URLs in responses to HTTP to ensure continued proxy usage
5. **Response forwarding**: Returns authenticated response to client

### Why Two Approaches?

- **IG Publisher** (`-proxy` parameter): Built-in proxy support works correctly
- **Java Validator** (system properties): Requires system-level proxy configuration because it caches URLs from CapabilityStatement responses and bypasses the `-proxy` parameter for subsequent requests

## Architecture

```
FHIR Validator/IG Publisher
         ↓
   localhost:8080 (mitmproxy)
         ↓
   OAuth2 Token Injection
         ↓
terminologieserver.nl (HTTPS + Bearer token)
```

## ⚠️ Clearing the Terminology Cache

When switching from the default terminology server (`tx.fhir.org`) to the NTS proxy, you should clear the local terminology cache. The IG Publisher caches terminology responses in `input-cache/txcache/`, and stale entries from a different server will cause validation errors or incorrect results.

### Option 1: Use the `-resetTx` argument

Pass `-resetTx` when running the IG Publisher to reset the cache automatically:

```cmd
_genonce_nts.bat -resetTx
```

This works because `_genonce_nts.bat` passes extra arguments (`%*`) to the IG Publisher. You only need to do this **once** after switching; subsequent runs can omit it.

### Option 2: Manually delete the cache folder

Delete the `input-cache/txcache/` directory before running the build:

**PowerShell:**
```powershell
Remove-Item -Recurse -Force input-cache\txcache
.\_genonce_nts.bat
```

**Command Prompt:**
```cmd
rmdir /s /q input-cache\txcache
_genonce_nts.bat
```

### When is this needed?

- Switching **from** `tx.fhir.org` **to** `terminologieserver.nl` (or vice versa)
- After changing NTS credentials (tokens may be cached in responses)
- When terminology validation produces unexpected errors after a server change

> **Tip**: If you're unsure, it's always safe to run with `-resetTx` once. The cache will be rebuilt on the next run.

## Troubleshooting

### ❌ Certificate/SSL Errors

**Error**: `PKIX path building failed: unable to find valid certification path`

**Solution**:
1. Ensure `install-cert.bat` ran as Administrator
2. Verify certificate installation:
   ```cmd
   keytool -list -keystore "%JAVA_HOME%\lib\security\cacerts" -storepass changeit | findstr mitmproxy
   ```
3. Restart your terminal after installation
4. Check the proxy container is running: `docker ps`

### ❌ 401 Unauthorized / "No credentials provided"

**Error**: Validation fails with authentication errors in `tx.log`

**Possible causes**:
- Environment variables not set: `Get-ChildItem Env: | Where-Object Name -like "*NTS*"`
- Proxy not running: `docker ps`
- Invalid credentials: Verify username/password at [NTS Service Desk](https://nictiz.atlassian.net/servicedesk/customer/portal/4)
- Java not using proxy: Check `JAVA_TOOL_OPTIONS` for standalone validator

**Solution**:
```powershell
# Check environment variables
Get-ChildItem Env: | Where-Object Name -like "*NTS*"

# Restart proxy with fresh credentials
docker compose down
$env:NTS_USER = "your-username"
$env:NTS_PASS = "your-password"
docker compose up -d

# Check logs for token retrieval
docker logs nts-proxy-nts-proxy-1
```

### ❌ Proxy Container Not Starting

**Error**: Container fails to start or exits immediately

**Solution**:
1. Check Docker is running: `docker ps`
2. Verify environment variables are set before `docker compose up`
3. Check container logs: `docker logs nts-proxy-nts-proxy-1`
4. Rebuild the image: `docker compose up -d --build --force-recreate`

### ℹ️ Viewing Proxy Traffic

Monitor all requests and responses:
```powershell
docker logs -f nts-proxy-nts-proxy-1
```

Look for:
- `Got an NTS access token` - Successful authentication
- `Added NTS auth token to GET/POST` - Requests being proxied
- `Rewrote URLs in JSON response` - Response modification working

### ℹ️ Testing the Proxy

Quick test without running full validation:

```powershell
# Set proxy environment
$env:HTTP_PROXY = "http://localhost:8080"
$env:HTTPS_PROXY = "http://localhost:8080"

# Test with curl (if installed)
curl -k http://terminologieserver.nl/fhir/metadata
```

You should see a successful CapabilityStatement response.

## Stopping the Proxy

```powershell
cd util\NTS-proxy
docker compose down
```

Removes the container but preserves the Docker image for faster restarts.

## Files

- `Dockerfile` - Container image definition (Debian + mitmproxy)
- `docker-compose.yml` - Container orchestration
- `NTS-proxy.py` - mitmproxy addon for authentication and URL rewriting
- `install-cert.bat` - Windows script for certificate installation
- `README.md` - This file

## Security Notes

- Credentials are passed via environment variables (not stored in files)
- OAuth2 tokens are cached in memory only (not persisted)
- The mitmproxy certificate is self-signed and only trusted by your local Java installation
- For production use, consider using GitHub Secrets for CI/CD credentials

## Further Reading

- [NTS Documentation](https://informatiestandaarden.nictiz.nl/wiki/Terminologie:Terminologieserver)
- [mitmproxy Documentation](https://docs.mitmproxy.org/)
- [FHIR Terminology Service](https://www.hl7.org/fhir/terminology-service.html)