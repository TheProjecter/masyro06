import Blender
from Blender import *
from Blender.Scene import Render

editmode = Window.EditMode()   				# If we are in edit mode; exit edit mode
if editmode: Window.EditMode(0)

world = World.GetCurrent()
if (world == None): 
	world = World.New("")

world.setHor([0.0, 0.0, 0.0])					# Black colour for Horizont

scn = Scene.GetCurrent()
context = scn.getRenderingContext()
context.setRenderPath("//") 
context.setImageType(Render.PNG)
context.enableGrayscale()

context.enableRayTracing(0)
context.setRenderer(Render.INTERNAL)
	
nameList = NMesh.GetNames()
complexList = {}
maxValue = 0
j = 1

for mat in Material.Get():
	compDict = {'RayMirrorLevel': 0, 'RayTranspLevel':0}

	# Removes all textures of the material
	texture = Texture.New()
	texture.setType('None')

	for i in range(0,9):
		mat.setTexture(i, texture)
	
	# Obtaining poperties for complexity
	if (mat.mode & Material.Modes.RAYMIRROR):
		compDict['RayMirrorLevel'] = mat.getMirrDepth()
		
	if (mat.mode & Material.Modes.RAYTRANSP):
		compDict['RayTranspLevel'] = mat.getTransDepth()
		
	# Calculates the material complexity
	complexList[j] = compDict['RayMirrorLevel'] + compDict['RayTranspLevel']
	if (complexList[j] > maxValue):
		maxValue = complexList[j]		
	j = j+1

j = 1	
for mat in Material.Get():
	mat.setMode()   # Remove all flags (even UV Mapping)
	mat.setAlpha(1)
	mat.emit = 0
	complexity = (complexList[j] * 1.0) / maxValue * (1.0)
	print complexity
	mat.setRGBCol (complexity, complexity, complexity) 
	mat.mode |= Material.Modes.SHADELESS
	j = j+1
