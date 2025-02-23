from fastapi import FastAPI, Request, status
from pydantic import BaseModel
import urllib
from fastapi.responses import FileResponse,RedirectResponse
import os
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from exception_handlers import request_validation_exception_handler, http_exception_handler, unhandled_exception_handler
from middleware import log_request_middleware
import pdfWrite


app = FastAPI()
app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
FilePath = ""

class CustomURLProcessor:
    def __init__(self):  
        self.path = "" 
        self.request = None

    def url_for(self, request: Request, name: str, **params: str):
        self.path = request.url_for(name, **params)
        self.request = request
        return self
    
    def include_query_params(self, **params: str):
        parsed = list(urllib.parse.urlparse(self.path))
        parsed[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(parsed)   

{
  "blank_pdf": "s3 blank pdf link",
  "json_link": "s3 json link"
}

class Item(BaseModel):
    blank_pdf: str | None = None 
    json_link: str | None = None 
    language: str  | None = None 




@app.post("/items/")
async def create_item(item: Item):
    if item.blank_pdf is None:
        raise HTTPException(
            status_code=404,
            detail="blank_pdf not found",
            headers={"X-Error": "There goes my error"},
        )
    if item.json_link is None:
        raise HTTPException(
            status_code=404,
            detail="json_link not found",
            headers={"X-Error": "There goes my error"},
        )
    if item.language is None:
        raise HTTPException(
            status_code=404,
            detail="language not found",
            headers={"X-Error": "There goes my error"},
        )
    
    blank_pdf = """"""+item.blank_pdf+""""""
    json_link = """"""+item.json_link+""""""
    print(blank_pdf,json_link)
    isFile = os.path.isfile("pdfWrite.py")
    print(isFile)
    FilePath = pdfWrite.main(item.blank_pdf,item.json_link)
    redirect_url = app.url_path_for("get_pdf",filename_pdf=FilePath)
    response = RedirectResponse(url=redirect_url)
    return response
    #os.system("pdfWrite.py "+item.blank_pdf+" "+item.json_link)    
    #return FileResponse(FilePath)

 
@app.post("/pdf/{filename_pdf}/")
def get_pdf(filename_pdf: str):   
    headers = {'Content-Disposition': 'inline; filename_pdf=' +filename_pdf}
    #return {"status": "Success", "filename_pdf": filename_pdf}
    return FileResponse(path=filename_pdf, headers=headers, media_type='application/pdf')   
    
