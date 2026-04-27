from typing import Annotated

from fastapi import Depends, Request

from core.flows.flow_loader_protocol import FlowLoaderProtocol


def get_flow_loader(request: Request) -> FlowLoaderProtocol:
    return request.app.state.flow_loader  # type: ignore[no-any-return]


FlowLoaderDep = Annotated[FlowLoaderProtocol, Depends(get_flow_loader)]
