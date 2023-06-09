from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
import io
from db import getData
import units
import pandas as pd


app = FastAPI(title="RAAV querys for Cerella")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/status", description="Test that the service can be contacted")
def get_DB_status():
    sql = "SELECT node_name, node_state FROM nodes ORDER BY 1;"
    return getData(sql)


@app.get(
    "/datasources",
    description="Retrieve a list of data sources supported by the service",
    operation_id="sourcesQueryService",
)
def get_datasources():
    data = {
        "sourceId": "8e95ec0d-4de8-45e0-95ee-990d152c1864",
        "sourceName": "LOV2",
        "properties": {"description": "Louise Owen query2"},
    }
    return data


@app.get(
    "/datasources/{sourceId}",
    operation_id="getSourceProperties",
    summary="Datasource definition",
    description="Returns a Cerella datasource description for a sourceId",
)
def get_datasourceData(sourceId: str):
    sql = """
        select
        distinct END_POINT_NAME,
        METHOD_GROUP,
        UNIT,
        MEASUREMENT,
        UNIT_TYPE,
        TRANSFORMATION
        from CONF_CERELLA_ENDPOINT
        """
    data = getData(sql)
    df = pd.json_normalize(data)
    # Add NUMBER as default columnType
    df = df.assign(COL_TYPE="NUMBER")
    # transform units
    df["UNIT"] = df.apply(lambda row: getUnitConv(row.UNIT), axis=1)
    data = df.to_dict(orient="records")
    return data
    


def getUnitConv(unit_string):
        # unit_string = f"{unit_string}-WIBBLE"
        unit_string = units.parse_unit(unit_string)
        unit_string = unit_string.name
        return unit_string



@app.get("/datasources/lov2/data/csv", response_class=StreamingResponse)
async def read_LOV2_data():
    sql = """
    SELECT SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    FROM RPT_CERELLA_DATA
    GROUP BY SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    """
    data = getData(sql)
    df = pivot_data(data)
    stream = io.StringIO()
    df.to_csv(stream, encoding="utf-8-sig", index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

@app.get("/datasources/lov2/data")
def prepare_json():
    sql = """
    SELECT SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    FROM RPT_CERELLA_DATA
    GROUP BY SUBSTANCE_IDENTIFIER, UISMILES, END_POINT_NAME, AVG
    """
    data = getData(sql)
    df = pivot_data(data)
    json_response = (
        df.stack()
        .groupby(level=0)
        .agg(lambda x: x.reset_index(level=0, drop=True).to_dict())
        .tolist()
    )
    return json_response


def pivot_data(data):
    df = pd.json_normalize(data)
    df = pd.pivot_table(
        df,
        values="AVG",
        index=["SUBSTANCE_IDENTIFIER", "UISMILES"],
        columns=["END_POINT_NAME"],
    )
    df = df.reset_index()
    return df
    
    
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
