from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from crawler.database import Listing, setup_database

app = FastAPI()
Session = setup_database()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Real Estate API. Visit /docs for API documentation."}

@app.get("/listings/")
def get_listings(region: str = None, trucheck: bool = None):
    with Session() as session:
        query = session.query(Listing)
        if region:
            query = query.filter(Listing.region.ilike(f"%{region}%"))
        if trucheck is not None:
            query = query.filter(Listing.trucheck == trucheck)
        results = query.all()
        if not results:
            raise HTTPException(status_code=404, detail="No listings found")
        return results

@app.get("/listings/region_counts/")
def count_listings_by_region():
    with Session() as session:
        results = session.query(Listing.region, func.count(Listing.id)).group_by(Listing.region).all()
        return {"region_counts": dict(results)}

@app.get("/listings/trucheck_counts/")
def count_trucheck_by_region():
    with Session() as session:
        results = session.query(Listing.region, func.count(Listing.id)).filter(Listing.trucheck == True).group_by(Listing.region).all()
        return {"trucheck_counts": dict(results)}
