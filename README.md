# flask_sample

## API Endpoints
## Health
"/" --> Health check [GET]<br>
"/health" --> Health Check [GET]
## Sensor Events
"/event" --> Device events [POST]
- Submits a JSON event 
```json
{
  "timestamp": "2018-02-24T08:45:21.893Z", 
  "direction": "1", 
  "dpu_id": "423"
}
```
## Room Events
"/room" --> [GET / POST]
- ###POST input 
```json
{
    "name": "SpaceA",
    "description": "Space A",
    "capacity": 10,
    "company": "Density",
    "floor": 1,
    "sensors": [
        {"dpu_id": 423,
        "name": "Doorway Z"
        },
        {"dpu_id": 283,
        "name": "Doorway Y"
        }
    ]
}
```
- ### GET format
```json
{
    "name": "SpaceA",
    "description": "Space A",
    "floor": 1,
    "company": "Density"
}
```
Response
```json
{
    "description": "None",
    "uid": "spacea1density",
    "max_capacity": "10",
    "date_created": "2021-06-23 17:34:32.362094",
    "name": "SpaceA",
    "floor": "1",
    "company": "Density",
    "date_modified": "2021-06-23 17:34:32.362109",
    "sensors": "[Device: 283:Doorway Y, Device: 423:Doorway Z]",
    "occupancy": 0
}
```

## Testing
Set path directory to project level
```commandline
pytest -vv
```

## Setup
```commandline
pip install -r requirements.txt
```
Setup database (SQLLite)
```commandline
FLASK createdb
```

Drop database (SQLLite)
```commandline
FLASK dropdb
```

Run server
```commandline
FLASK run
```