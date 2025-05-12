import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document  # Works in the Revit Python Shell

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
    
    # Rotate the element if an angle adjustment is needed
    if angle != 0:
        # Define the rotation axis
        rotation_axis = Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(0) + XYZ.BasisZ)
        ElementTransformUtils.RotateElement(doc, element.Id, rotation_axis, angle)
        return True
    return False

# Start a transaction to modify the document
t = Transaction(doc, "Align Off-Axis Grids and Walls")
t.Start()

# Counters for the number of aligned elements
aligned_grids_count = 0
aligned_walls_count = 0

# Align off-axis grids
grids = FilteredElementCollector(doc).OfClass(Grid)
for grid in grids:
    if align_off_axis_element(grid, grid.Curve):
        aligned_grids_count += 1
"""
# Align off-axis walls
walls = FilteredElementCollector(doc).OfClass(Wall)
for wall in walls:
    # Get the wall location line (curve)
    location = wall.Location
    if isinstance(location, LocationCurve):
        curve = location.Curve
        if align_off_axis_element(wall, curve):
            aligned_walls_count += 1
"""
# Commit the transaction
t.Commit()

# Print the result using .format() method for compatibility
print("{} grids were aligned.".format(aligned_grids_count))
#print("{} walls were aligned.".format(aligned_walls_count))