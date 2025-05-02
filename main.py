from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Import your existing methods here:
from googleScrap import expand_gmb_link_and_get_kgmid_url, extract_google_details

@app.get("/scrape")
def scrape_business_info(link: str = Query(..., description="Short GMB Link")):
    try:
        kgmid_url = expand_gmb_link_and_get_kgmid_url(link)
        if not kgmid_url:
            return JSONResponse(status_code=400, content={"error": "Invalid GMB link or kgmid not found."})
        result = extract_google_details(kgmid_url)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Optional: For local testing
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
