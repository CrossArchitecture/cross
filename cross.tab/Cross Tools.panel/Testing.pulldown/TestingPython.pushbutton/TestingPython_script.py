# -*- coding: utf-8 -*-
__title__   = "Center Room Tags"


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ELEMENTS
all_room_tags = FilteredElementCollector(doc, doc.ActiveView.Id)\
    .OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()

# CONTROLS
step = 2 # INTERNAL UNITS IN FEET


OFFSET_DISTANCE_FEET = 1.64042  # Offset distance in feet

def move_room_and_tag(tag, room, new_pt):
    """Function to move both Room and Tag Locations, if they are not part of the group.
    :param tag:     Room Tag
    :param room:    Room
    :param new_pt:  XYZ Point."""
    if room.GroupId == ElementId(-1):  # ElementId(-1) means None
        room.Location.Point = new_pt

    if tag.GroupId == ElementId(-1):
        tag.Location.Point = new_pt


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

def get_corner_choice():
    """Prompts the user to choose one of the four corners for the offset."""
    dialog = TaskDialog("Choose Corner")
    dialog.MainInstruction = "Select the corner to move the tags with an offset:"
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink1, "Upper Left")
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink2, "Upper Right")
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink3, "Lower Left")
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink4, "Lower Right")
    result = dialog.Show()

    if result == TaskDialogResult.CommandLink1:
        return 1
    elif result == TaskDialogResult.CommandLink2:
        return 2
    elif result == TaskDialogResult.CommandLink3:
        return 3
    elif result == TaskDialogResult.CommandLink4:
        return 4
    else:
        return None

with Transaction(doc, __title__) as t:
    t.Start()

    corner_choice = get_corner_choice()

    if corner_choice is not None:
        for tag in all_room_tags:
            room = tag.Room
            room_bb = room.get_BoundingBox(doc.ActiveView)
            offset_distance = OFFSET_DISTANCE_FEET
            offset_x = -offset_distance if corner_choice in [1, 3] else offset_distance
            offset_y = offset_distance if corner_choice in [1, 2] else -offset_distance

            if corner_choice in [1, 2]:
                room_corner = XYZ(room_bb.Min.X, room_bb.Max.Y, room_bb.Min.Z)
            else:
                room_corner = XYZ(room_bb.Max.X, room_bb.Min.Y, room_bb.Min.Z)

            room_corner_with_offset = XYZ(room_corner.X + offset_x, room_corner.Y + offset_y, room_corner.Z)
            move_room_and_tag(tag, room, room_corner_with_offset)

    t.Commit()