# Tool and Base Generator V0.1

from warnings import catch_warnings
from vcCommand import *
import vcMatrix, vcVector 
import random
import math

app = getApplication()
cmd = getCommand()  
cmd.Name = "ToolAndBase"

def OnStart():
    global program

    program = getProgram() 
    if not program:
        app.messageBox("No program selected, aborting.","Warning",VC_MESSAGE_TYPE_WARNING,VC_MESSAGE_BUTTONS_OK)
        return

    controller = program.Executor.Controller
    createProperties()
    executeInActionPanel()

def getProgram():
    teachcontext = app.TeachContext

    if teachcontext.ActiveRobot:
        executors = teachcontext.ActiveRobot.findBehavioursByType(VC_ROBOTEXECUTOR)

    if executors:
        return executors[0].Program

    return None

def createProperties():
    global all_props
    global genButton

    createProperty(VC_REAL, 'Sphere Radius', None, None)
    createProperty(VC_REAL, 'Point Spacing X', None, None)
    createProperty(VC_REAL, 'Point Spacing Y', None, None)
    createProperty(VC_REAL, 'Point Spacing Z', None, None)
    createProperty(VC_REAL, 'Z Cutoff', None, None)
    createProperty(VC_REAL, 'Void Radius', None, None)

    createProperty(VC_REAL, 'Rx', None, None)
    createProperty(VC_REAL, 'Ry', None, None)
    createProperty(VC_REAL, 'Rz', None, None)

    createProperty(VC_REAL, 'Speed', None, None)
    createRestrainedProperty(VC_STRING, 'Move Type', 'Linear', ['Linear', 'Joint'])

    genButton = createProperty(VC_BUTTON, 'Generate', None, callGenerator)

    all_props = [x for x in cmd.Properties]

def createProperty(type, name, defaultValue, callback):
    prop = cmd.getProperty(name)
    if prop == None:
        prop = cmd.createProperty(type, name)

    if defaultValue:
        prop.Value = defaultValue

    if callback:
        prop.OnChanged = callback

    return prop

def createPropertyOld(type, name, defaultValue, callback):
    prop = cmd.getProperty(name)
    if prop:
        return prop

    prop = cmd.createProperty(type, name)

    if defaultValue:
        prop.Value = defaultValue

    if callback:
        prop.OnChanged = callback

    return prop

def createRestrainedProperty(type, name, defaultValue, constraints):
    prop = cmd.getProperty(name)
    if prop:
        return prop

    prop = cmd.createProperty(type, name, VC_PROPERTY_STEP)
    prop.StepValues = constraints

    if defaultValue:
        prop.Value = defaultValue

    return prop

def callGenerator(arg = None):
    global all_props

    print 'Generating...'

    routine = app.TeachContext.ActiveRoutine
    routine.clear()

    moveType = cmd.getProperty('Move Type').Value


    addMesCall = False

    sphere_radius = cmd.getProperty('Sphere Radius').Value

    x_spacing = cmd.getProperty('Point Spacing X').Value
    y_spacing = cmd.getProperty('Point Spacing Y').Value
    z_spacing = cmd.getProperty('Point Spacing Z').Value

    rx = cmd.getProperty('Rx').Value
    ry = cmd.getProperty('Ry').Value
    rz = cmd.getProperty('Rz').Value

    z_cutoff = cmd.getProperty('Z Cutoff').Value

    void_radius = cmd.getProperty('Void Radius').Value

    index = 0

    points = GeneratePointGrid(sphere_radius, x_spacing, y_spacing, z_spacing, z_cutoff, void_radius)
    
    print("printing points...")
    for point in points:
        index += 1
        addPosition(routine, moveType, str(index), point[0], point[1], point[2], addMesCall, rx, ry, rz)

    all_props = None
    app.render()
    print 'Done.'

def addPosition(routine, moveType, name, x, y, z, addMesCall, rx, ry, rz):
    speed = cmd.getProperty('Speed').Value

    m = vcMatrix.new()
    m.translateAbs(x, y, z)
    m.setWPR(rx, ry, rz)

    stat = None
    if moveType == 'Linear':
        stat = routine.addStatement(VC_STATEMENT_LINMOTION)
    else:
        stat = routine.addStatement(VC_STATEMENT_PTPMOTION)

    stat.readIn()
    stat.Positions[0].Name = name
    stat.Positions[0].PositionInReference = m
    stat.AccuracyMethod = VC_MOTIONTARGET_AM_DISTANCE
    stat.AccuracyValue = 0.0

    if moveType == 'Linear':
        stat.MaxSpeed = speed
    else:
        clampedSpeed = max(min(speed, 100.0), 0.0)
        stat.JointSpeed = clampedSpeed / 100.0

    if addMesCall:
        stat = routine.addStatement(VC_STATEMENT_COMMENT)
        stat.Comment = 'USR_CMD GRID_MEASURE()'

def GeneratePointGrid(sphere_radius, x_spacing, y_spacing, z_spacing, z_cutoff, void_radius):
    points = []
    
    x, y, z = sphere_radius, sphere_radius, - sphere_radius
    
    while x <= sphere_radius:
        while y <= sphere_radius:
            while z <= sphere_radius:
                distance = math.sqrt(x**2 + y**2 + z**2)
                if distance <= sphere_radius and z >= z_cutoff and distance >= void_radius:
                    points.append((x, y, z))
                z += z_spacing
            y += y_spacing
            z = -sphere_radius
        x += x_spacing
        y = -sphere_radius
    
    return points
