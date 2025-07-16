import os
from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class MongoConfig:
    uri: str
    database: str
    username: str = ""
    password: str = ""
    host: str = "localhost"
    port: int = 27017
    auth_db: str = "admin"
    use_tls: bool = False
    replica_set: str = ""

    @staticmethod
    def from_env() -> "MongoConfig":
        uri = os.getenv("MONGO_URI", "")
        if uri:
            return MongoConfig(
                uri=uri,
                database=os.getenv("MONGO_DATABASE", "default_db"),
            )

        username = os.getenv("MONGO_USERNAME", "")
        password = os.getenv("MONGO_PASSWORD", "")
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", 27017))
        auth_db = os.getenv("MONGO_AUTH_DB", "admin")
        use_tls = os.getenv("MONGO_USE_TLS", "false").lower() == "true"
        replica_set = os.getenv("MONGO_REPLICA_SET", "")

        auth_part = ""
        if username and password:
            auth_part = f"{quote_plus(username)}:{quote_plus(password)}@"

        uri_parts = f"mongodb://{auth_part}{host}:{port}"
        options = []

        if use_tls:
            options.append("tls=true")
        if replica_set:
            options.append(f"replicaSet={replica_set}")
        if options:
            uri_parts += f"/?{'&'.join(options)}"
        else:
            uri_parts += f"/{auth_db}"

        return MongoConfig(
            uri=uri_parts,
            database=os.getenv("MONGO_DATABASE", "default_db"),
            username=username,
            password=password,
            host=host,
            port=port,
            auth_db=auth_db,
            use_tls=use_tls,
            replica_set=replica_set,
        )
