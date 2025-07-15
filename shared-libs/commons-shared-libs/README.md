## 🧱 Shared Core Libraries

This directory contains reusable libraries that are shared across services, jobs, and system components. These are packaged and mounted into running containers and jobs as a common runtime foundation.

### 📦 Modules Included

* **Service Lifecycle & Registry**

  * Defines a standardized service base class with lifecycle hooks (`on_start`, `on_stop`, `on_failure`)
  * Centralized service manager to start, stop, and monitor registered services
  * Lightweight service registry for tracking active service instances and resolving dependencies dynamically

* **Observability**

  * Provides integrated support for metrics, tracing, and structured logging
  * Built on OpenTelemetry for standards-compliant instrumentation
  * Includes decorators to transparently capture spans and record metrics in async services and jobs

* **Client Connectors**

  * Shared async clients and adapters for:

    * **HTTP** (sync & async, including WebSocket support)
    * **Kafka** (AIOKafka-based producer/consumer wrappers)
    * **Elasticsearch** (async client wrapper with config-driven setup)
  * Encapsulates connection logic, tracing, and retry policies



### Current versions:

- `commons_service_management` - 0.2.4
- `commons_observability` - 0.4.1
- `commons_connector` - 0.4.3
