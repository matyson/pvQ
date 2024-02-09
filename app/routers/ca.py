from fastapi import APIRouter, HTTPException, Request, Query
from ..models import PVModel, Status
from typing import Annotated
from ..fake_data import pv_list
from caproto import ReadNotifyResponse


router = APIRouter(
    prefix="/ca",
    tags=["Channel Access"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root():
    return {"Hello": "from CA"}


@router.get("/info/{pv_name}")
async def cainfo(pv_name: str, request: Request):
    return {"info": "TO DO"}


@router.get("/get/{pv_name}")
async def caget(pv_name: str, request: Request):
    ca = request.state.ca
    pvs = await ca.get_pvs(pv_name)

    try:
        res = await pvs[0].read()
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout")

    # my data is a python builtin or numpy array, so I need to convert it to a list to be able to serialize it
    if isinstance(res.data, (list, tuple)):
        return PVModel(
            name=pv_name,
            data=res.data,
            status=Status(
                name=res.status.name,
                code=res.status.code,
                code_with_severity=res.status.code_with_severity,
                severity=res.status.severity,
                success=res.status.success,
                description=res.status.description,
            ),
            data_type=res.data_type,
            data_count=res.data_count,
        )
    return PVModel(
        name=pv_name,
        data=res.data.tolist(),
        status=Status(
            name=res.status.name,
            code=res.status.code,
            code_with_severity=res.status.code_with_severity,
            severity=res.status.severity,
            success=res.status.success,
            description=res.status.description,
        ),
        data_type=res.data_type,
        data_count=res.data_count,
    )


@router.get("/get_many")
async def caget_many(pv: Annotated[list[str], Query()], request: Request):
    ca = request.state.ca
    pvs = await ca.get_pvs(*pv)

    values = []
    for pv in pvs:
        try:
            res = await pv.read()
        except TimeoutError:
            raise HTTPException(status_code=408, detail="Timeout")
        values.append({"name": pv.name, "value": res.data[0]})
    return values


@router.put("/put/{pv_name}")
async def caput(pv_name: str, value: float):
    res = next((pv for pv in pv_list if pv.name == pv_name), None)
    if res is None:
        raise HTTPException(status_code=404, detail="PV not found")
    res.value = value
    return res


@router.put("/put_many")
async def caput_many(pv: str, value: float):
    res = [v for v in pv_list if v.name in pv]
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="PVs not found")
    for r in res:
        r.value = value
    return res
