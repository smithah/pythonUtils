import uvicorn
import pathlib

cwd = pathlib.Path(__file__).parent.resolve()
log_config = f"{cwd}/log.ini"



if __name__ == "__main__":
    
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="debug",workers=10, limit_concurrency=10, limit_max_requests=1000)