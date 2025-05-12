import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document

# Define maximum allowable offset for alignment
max_distance = 0.0001

# Function to align an off-axis element
def align_off_axis_element(element, curve):
    direction = (curve.GetEndPoint(1) - curve.GetEndPoint(0)).Normalize()
    distance2hor = direction.DotProduct(XYZ.BasisY)
    distance2vert = direction.DotProduct(XYZ.BasisX)
    angle = 0
    
    # Check alignment with horizontal (Y-axis)
    if abs(distance2hor) < max_distance:
        vector = direction if direction.X >= 0 else direction.Negate()
        angle = math.asin(-vector.Y)
    
    # Check alignment with vertical (X-axis)
    if abs(distance2vert) < max_distance:
        vector = direction if direction.Y >= 0 else direction.Negate()
        angle = math.asin(vector.X)
    
    # Return angle if adjustment is needed
    if angle != 0:
        return angle
    return None

# Collect all room separation lines BEFORE starting the transaction
lines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RoomSeparationLines).WhereElementIsNotElementType().ToElements()

# Create a list to store elements and their rotation data
elements_to_align = []

# First pass: Collect all elements that need alignment
for line in lines:
    location = line.Location
    if isinstance(location, LocationCurve):
        curve = location.Curve
        angle = align_off_axis_element(line, curve)
        if angle is not None:
            # Store element ID and rotation data
            rotation_axis = Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(0) + XYZ.BasisZ)
            elements_to_align.append((line.Id, rotation_axis, angle))

# Start a transaction to modify the document
t = Transaction(doc, "Align Off-Axis Room Separation Lines")
t.Start()

# Second pass: Apply the rotations
aligned_lines_count = 0
for element_id, rotation_axis, angle in elements_to_align:
    ElementTransformUtils.RotateElement(doc, element_id, rotation_axis, angle)
    aligned_lines_count += 1

# Commit the transaction
t.Commit()

# Print the result
print("{} room separation lines were aligned.".format(aligned_lines_count))