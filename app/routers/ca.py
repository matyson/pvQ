from fastapi import APIRouter, HTTPException
from ..fake_data import pv_list

router = APIRouter(
    prefix="/ca",
    tags=["Channel Access"],
    responses={404: {"description": "Not found"}},
)


@router.get("/info/{pv_name}")
async def cainfo(pv_name: str):
    res = next((pv for pv in pv_list if pv.name == pv_name), None)
    if res is None:
        raise HTTPException(status_code=404, detail="PV not found")
    return res


@router.get("/get/{pv_name}")
async def caget(pv_name: str):
    res = next((pv for pv in pv_list if pv.name == pv_name), None)
    if res is None:
        raise HTTPException(status_code=404, detail="PV not found")
    return res


@router.get("/get_many")
async def caget_many(pv: str):
    res = [v for v in pv_list if v.name in pv]
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="PVs not found")
    return res


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
