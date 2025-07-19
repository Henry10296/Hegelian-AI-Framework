# Type stubs for optional dependencies
from typing import Any, Optional

# Neo4j stubs
if not hasattr(globals(), 'NEO4J_AVAILABLE'):
    NEO4J_AVAILABLE = False

if not NEO4J_AVAILABLE:
    class AsyncGraphDatabase:
        @staticmethod
        def driver(uri: str, auth: tuple) -> Any:
            return None
    
    class ServiceUnavailable(Exception):
        pass
    
    class TransientError(Exception):
        pass