from typing import List

from common.types import (
    JSONRPC_ID,
    ContentTypeNotSupportedError,
    JSONRPCResponse,
    UnsupportedOperationError,
)


def are_modalities_compatible(
    server_output_modes: List[str], client_output_modes: List[str]
) -> bool:
    """Modalities are compatible if they are both non-empty
    and there is at least one common element."""
    if client_output_modes is None or len(client_output_modes) == 0:
        return True

    if server_output_modes is None or len(server_output_modes) == 0:
        return True

    return any(x in server_output_modes for x in client_output_modes)


def new_incompatible_types_error(request_id: JSONRPC_ID) -> JSONRPCResponse:
    """Create a new JSON-RPC response with an incompatible types error."""
    return JSONRPCResponse(id=request_id, error=ContentTypeNotSupportedError())


def new_not_implemented_error(request_id: JSONRPC_ID) -> JSONRPCResponse:
    """Create a new JSON-RPC response with an unsupported operation error."""
    return JSONRPCResponse(id=request_id, error=UnsupportedOperationError())
