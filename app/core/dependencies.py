from typing import Annotated, Union

from fastapi import Depends, Request

from core.flow_loader import FlowLoader
from core.mongo_flow_loader import MongoFlowLoader


def get_flow_loader(request: Request) -> Union[FlowLoader, MongoFlowLoader]:
    return request.app.state.flow_loader  # type: ignore[no-any-return]


FlowLoaderDep = Annotated[Union[FlowLoader, MongoFlowLoader], Depends(get_flow_loader)]
