from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
import io
from db import getData
from models import (
    DataModel,
    Details,
    AvailableProperties,
    AdditionalMetadata,
    Endpoint,
    Transformation,
)
import units
import pandas as pd
from typing import List


app = FastAPI(title="RAAV querys for Cerella")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get(
    "/status",
    description="Test that the service can be contacted",
    operation_id="testQueryService"
)
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
    response_model=DataModel,
)
def get_datasourceData(sourceId: str):
    sql = """
        select
        distinct END_POINT_NAME,
        METHOD_GROUP,
        UNIT,
        TRANSFORMATION
        from CONF_CERELLA_ENDPOINT
        """
    data = getData(sql)
    df = pd.json_normalize(data)
    #optionally endpoints manually if required
    # df.drop(df[df['END_POINT_NAME'] =="SynAcidpKa (Dec 2021)"].index, inplace=True)
    # df.drop(df[df['END_POINT_NAME'] =="SynLogP (D-Cide Dec 2021)"].index, inplace=True)
    
    # Add NUMBER as default columnType
    df = df.assign(COL_TYPE="NUMBER")
    # transform units
    df["UNIT"] = df.apply(lambda row: getUnitConv(row.UNIT), axis=1)
    df.rename(
        columns={
            "END_POINT_NAME": "columnName",
            "METHOD_GROUP": "assayId",
            "UNIT": "units",
            "COL_TYPE": "columnType",
        },
        inplace=True,
    )
    data = df.to_dict(orient="records")

    response = [
        AvailableProperties(
            details=Details(assayId="", units="OTHER", format="smiles"),
            fieldName="SUBSTANCE_IDENTIFIER",
            columnType="TEXT",
            columnName="SUBSTANCE_IDENTIFIER",
        ),
        AvailableProperties(
            details=Details(assayId="", units="OTHER", format="smiles"),
            fieldName="UISMILES",
            columnType="STRUCTURE",
            columnName="UISMILES",
        ),
    ]

    for row in data:
        details = row.pop("assayId", None), row.pop("units", None)
        column_data = AvailableProperties(
            details=Details(assayId=details[0], units=details[1]),
            fieldName=row["columnName"],
            columnName=row["columnName"],
            columnType=row["columnType"],
        ).dict()
        response.append(column_data)

    # append the Structure descriptor columns
    cerella_endpoints = []
    for row in data:
        if row["TRANSFORMATION"] == "log":
            cerella_endpoint = Endpoint(
                endpointName=row["columnName"],
                transformation=Transformation(
                    constant=0, factor=1, functionType="LOG10"
                ),
            )
            cerella_endpoints.append(cerella_endpoint)

    # Create AdditionalMetadata object
    additional_metadata = AdditionalMetadata(cerellaEndpoints=cerella_endpoints)

    # Create DataModel object
    completeResponse = DataModel(
        database="None",
        name="Syngenta_lov2",
        connection="DATA_FILE@95fec5ef-d53b-4326-989a-dcca037dba33",
        idColumn="SUBSTANCE_IDENTIFIER",
        template="",
        cartridgeColumn=None,
        chemistryColumn="UISMILES",
        sourceId="e95ec0d-4de8-45e0-95ee-990d152c1864",
        additionalMetadata=additional_metadata,
        availableProperties=response,
    )

    return completeResponse


def getUnitConv(unit_string):
    unit_string = units.parse_unit(unit_string)
    unit_string = unit_string.name
    return unit_string


@app.get(
    "/datasources/{sourceId}/data/csv",
    response_class=StreamingResponse,
    description="Retrieve data from the database specified by the source. Return a csv file",
    operation_id="getDataQueryServiceCSV",
)
async def read_data():
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


@app.get(
    "/datasources/{sourceId}/data",
    description="Retrieve data from the database specified by the source.",
    operation_id="getDataQueryService"
)
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


@app.get("/datasources/psd")
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
