import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter

rooms = IN[0]  # noqa
tech = IN[1]  # noqa

tech_rooms = []

for r in rooms:
    room = UnwrapElement(r)  # noqa
    r_param = room.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT)
    if r_param:
        r_param_value = r_param.AsString()
        if r_param_value is not None:
            for t in tech:
                if t in r_param_value:
                    tech_rooms.append(r)

OUT = tech_rooms
