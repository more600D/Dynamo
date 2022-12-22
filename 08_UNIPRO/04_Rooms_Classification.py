import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter

rooms = IN[0]  # noqa
tech = IN[1]  # noqa
names = IN[2]  # noqa

tech_rooms = []


def get_rooms(room, tech):
    unwrap_room = UnwrapElement(room)  # noqa
    r_param = unwrap_room.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT)
    if r_param:
        r_param_value = r_param.AsString()
        if r_param_value is not None:
            if isinstance(tech, list):
                for t in tech:
                    if t.lower() in r_param_value.lower():
                        tech_rooms.append(room)
            else:
                if tech.lower() in r_param_value.lower():
                    tech_rooms.append(room)
    return tech_rooms


result = None
if not names:
    for r in rooms:
        result = get_rooms(r, tech)
else:
    if isinstance(names, list):
        for r in rooms:
            for n in names:
                if n in r.Name:
                    result = get_rooms(r, tech)
    else:
        for r in rooms:
            if names in r.Name:
                result = get_rooms(r, tech)

OUT = result
