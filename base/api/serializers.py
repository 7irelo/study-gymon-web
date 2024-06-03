import json
from base.models import Room

def roomSerialize(pk):
    data = {
        "field1": Room.objects.get(id=pk)
    }
    return json.dumps(data)