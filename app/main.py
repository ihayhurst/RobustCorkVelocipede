from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
import io
from db import getData
import pandas as pd


app = FastAPI(title="RAAV querys for Cerella")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/lov2/data/csv", response_class=StreamingResponse)
async def read_LOV2_data():
    sql = """
    SELECT SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    FROM RPT_CERELLA_DATA
    GROUP BY SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    """
    data = getData(sql)
    df = pd.json_normalize(data)
    df = pd.pivot_table(
        df,
        values="AVG",
        index=["SUBSTANCE_IDENTIFIER", "UISMILES"],
        columns=["END_POINT_NAME"],
    )
    df = df.reset_index()
    json_response = (
        df.stack()
        .groupby(level=0)
        .agg(lambda x: x.reset_index(level=0, drop=True).to_dict())
        .tolist()
    )
    
    df = df.reset_index(drop=True)
    stream = io.StringIO()
    df.to_csv(stream,encoding="utf-8-sig", index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        
    return response

@app.get("/api/psd")
def project_Substance_Details():
        sql = """
        select
        distinct project_code, project_name, rd_subs_pc
        from pres_project
        where 1=1
        and (RD_STATUS_PC ='FUNDED'
        and RD_PROJECT_STAGE_PC in ('OPTIM','LEADEXP','PMG','H2L','LSEL')
        OR project_code in
                (select project_code from CONF_CERELLA_PROJECT where INCLUDE ='Y')
                )
        and project_code not in
        (select project_code from CONF_CERELLA_PROJECT where INCLUDE ='N')
        order by 1,3
        """
        data = getData(sql)
        return data