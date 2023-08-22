import rpw
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import Transaction, FamilySymbol

with rpw.db.Transaction("Delete family types from project"):
    # Find families of selected object and delete it
    for id in uidoc.Selection.GetElementIds():
        el = doc.GetElement(id)
        familytype_id = el.GetTypeId()
        doc.Delete(familytype_id)



