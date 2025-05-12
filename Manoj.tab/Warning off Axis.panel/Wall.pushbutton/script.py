__author__='Manoj Mittal'
import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
 
# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document  # Works in the Revit Python Shell
 
# Get uidoc
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI.Selection import Selection, ObjectType
uidoc = __revit__.ActiveUIDocument
 
 
# Define maximum allowable offset for alignment
max_distance = 0.0001
 
# Function to align an off-axis element
def align_off_axis_element(element, curve):
    direction = (curve.GetEndPoint(1) - curve.GetEndPoint(0)).Normalize()
    distance2hor = direction.DotProduct(XYZ.BasisY)
    distance2vert = direction.DotProduct(XYZ.BasisX)
    angle = 0
    try:
        # Check alignment with horizontal (Y-axis)
        if abs(distance2hor) < max_distance:
            vector = direction if direction.X >= 0 else direction.Negate()
            angle = math.asin(-vector.Y)
       
        # Check alignment with vertical (X-axis)
        if abs(distance2vert) < max_distance:
            vector = direction if direction.Y >= 0 else direction.Negate()
            angle = math.asin(vector.X)
       
        # Rotate the element if an angle adjustment is needed
        if angle != 0:
            # Define the rotation axis
            rotation_axis = Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(0) + XYZ.BasisZ)
            ElementTransformUtils.RotateElement(doc, element.Id, rotation_axis, angle)
            return True
        return False
    except Exception as e:
        print("Error:", e)
   
 
# Start a transaction to modify the document
t = Transaction(doc, "Align Off-Axis Walls")
t.Start()
 
# Counters for the number of aligned elements
aligned_walls_count = 0
 
# getting current selection as list of ElementIds
sel = uidoc.Selection.GetElementIds()
 
# checking if something is selected; if yes, just get the first element
if len(sel) > 0:
    element = doc.GetElement(sel[0])
 
# if nothing is selected:
else:
    # prompting selection will return not an element, but its reference.
    # PickObject() takes an argument - what you want to select: whole element,
    # part of it, linked element etc. We only need an element.
    element_reference = uidoc.Selection.PickObject(ObjectType.Element, "Select an element.")
    # obtaining the element from reference, so we can access its parameters
    element = doc.GetElement(element_reference)
 
# Get the wall location line (curve)
location = element.Location
if isinstance(location, LocationCurve):
    curve = location.Curve
    if align_off_axis_element(element, curve):
        aligned_walls_count += 1
   
 
# Commit the transaction
t.Commit()
 
# Print the result
print(aligned_walls_count, " walls were aligned.")