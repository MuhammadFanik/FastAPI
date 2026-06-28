from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Dict, Literal

app = FastAPI()

# Model 1 - Requirements
class Requirements(BaseModel):
    degree: Annotated[str, Field(description="Degree required for this job")]
    skill: Annotated[List[str], Field(description="Skills required for this job")]