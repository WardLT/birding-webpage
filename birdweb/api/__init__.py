"""Functions related to FastAPI"""
from pydantic import BaseModel, Field
from datetime import timedelta
from time import monotonic

from fastapi import FastAPI

from birdweb.data import load_data

app = FastAPI()

_start_time = monotonic()


class SummaryStats(BaseModel):
    """General information about my activities"""

    # Overall statistics
    total_images: int = Field(description='Total number of images')
    total_species: int = Field(description='Number of species I have imaged')


@app.get("/")
def home():
    """Information about the server"""

    return {
        'uptime': timedelta(seconds=monotonic() - _start_time),
        'image_count': len(load_data())
    }


@app.get("/statistics")
def statistics() -> SummaryStats:
    """Get general information about my photo collection"""

    data = load_data()
    return SummaryStats(
        total_images=len(data),
        total_species=len(set(x.species for x in data))
    )
