from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import time
import imgui
from math import *
import random

import magic
import lab_utils as lu
from ObjModel import ObjModel
import glob
import os

from Sphere import Sphere

g_lightYaw = 25.0
g_lightYawSpeed = 0.0#145.0
g_lightPitch = -75.0
g_lightPitchSpeed = 0.0#30.0
g_lightDistance = 250.0
g_lightColourAndIntensity = lu.vec3(0.9, 0.9, 0.6)
g_ambientLightColourAndIntensity = lu.vec3(0.1)

g_camera = lu.OrbitCamera([0,0,0], 10.0, -25.0, -35.0)
g_yFovDeg = 45.0

g_currentModelName = "shaderBall1.obj"
g_model = None
g_vertexShaderSource = ObjModel.defaultVertexShader
g_fragmentShaderSource = ObjModel.defaultFragmentShader
g_currentFragmentShaderName = 'fragmentShader.glsl'

g_currentEnvMapName = 'NissiBeach2'

g_environmentCubeMap = None

# Set the texture unit to use for the cube map to the next free one
# (free as in not used by the ObjModel)
TU_EnvMap = ObjModel.TU_Max



def buildShader(vertexShaderSource, fragmentShaderSource):
    shader = lu.buildShader(vertexShaderSource, fragmentShaderSource, ObjModel.getDefaultAttributeBindings())
    if shader:
        glUseProgram(shader)
        ObjModel.setDefaultUniformBindings(shader)
        glUseProgram(0)
    return shader

 

g_reloadTimeout = 1.0
def update(dt, keys, mouseDelta):
    global g_camera
    global g_reloadTimeout
    global g_lightYaw
    global g_lightYawSpeed
    global g_lightPitch
    global g_lightPitchSpeed

    g_lightYaw += g_lightYawSpeed * dt
    g_lightPitch += g_lightPitchSpeed * dt

    g_reloadTimeout -= dt
    if g_reloadTimeout <= 0.0:
        reLoadShader()
        g_reloadTimeout = 1.0

    g_camera.update(dt, keys, mouseDelta)

def getPosition(x, rotationSpeed, time):
    radius = sqrt(x * x + 0 * 0)
    theta = atan2(0, x)
    theta += time * rotationSpeed
    x = radius * cos(theta)
    y = radius * sin(theta)

    return lu.vec3(x, y, 0)


# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(xOffset, width, height, time, textures, vao):
    global g_camera
    global g_yFovDeg
    global g_model

    lightPosition = lu.vec3(0,0,0)

    sunPosition = lu.vec3(0, 0, 0)
    mercuryPosition = getPosition(80, 0.01, time)
    saturnPosition = getPosition(300, 0.05, time)
    experimentPosition = getPosition(150, 0.02, time)
    moonPosition = getPosition(25, 0.1, time)

    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(xOffset, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.0, 0.0, 0.0, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    worldToViewTransform = g_camera.getWorldToViewMatrix([0,1,0])
    viewToClipTransform = lu.make_perspective(g_yFovDeg, width/height, 0.1, 1500.0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    Sphere.drawSphereWithTexture(experimentPosition, 20.0, "planet1.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/planetFragmentShader.glsl")
    Sphere.drawSphereWithTexture(mercuryPosition, 10.0, "planet2.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/planetFragmentShader.glsl")
    Sphere.drawSphereWithTexture(saturnPosition, 10.0, "fire.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/planetFragmentShader.glsl")

    randomNo = random.random()

    Sphere.drawSphereWithTexture(sunPosition, 15.0, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/sunFragmentShader.glsl")
    Sphere.drawSphereWithTexture(sunPosition, 16.0 + 1 * randomNo, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/cheekyShader.glsl")
    Sphere.drawSphereWithTexture(sunPosition, 17.0 + 2 * randomNo, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/cheekyShader.glsl")
    Sphere.drawSphereWithTexture(sunPosition, 18.0 + 3 * randomNo, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/cheekyShader.glsl")
    Sphere.drawSphereWithTexture(sunPosition, 20.0 + 5 * randomNo, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/cheekyShader.1.glsl")
    Sphere.drawSphereWithTexture(sunPosition, 24.0 + 9 * randomNo, "sun.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/cheekyShader.2.glsl")

    Sphere.drawSphereWithTexture(sunPosition, 700, "stars3.png", viewToClipTransform, worldToViewTransform, textures, vao, lu.transformPoint(worldToViewTransform, lightPosition), "shaders/allVertexShader.glsl", "shaders/sunFragmentShader.1.glsl")


    glDisable(GL_BLEND)

def itemListCombo(currentItem, items, name):
    ind = items.index(currentItem)
    _,ind = imgui.combo(name, ind, items)
    return items[ind]


g_currentMaterial = 0
def drawUi(width, height):
    global g_yFovDeg
    global g_currentMaterial
    global g_lightYaw
    global g_lightYawSpeed
    global g_lightPitch
    global g_lightPitchSpeed
    global g_lightDistance
    global g_lightColourAndIntensity
    global g_ambientLightColourAndIntensity
    global g_environmentCubeMap
    global g_currentEnvMapName
    global g_currentModelName
    global g_currentFragmentShaderName
    global g_model

    g_camera.drawUi()
    
    g_model.updateMaterials()



def reLoadShader():
    global g_vertexShaderSource
    global g_fragmentShaderSource
    global g_shader
    
    vertexShader = ""
    with open('vertexShader.glsl') as f:
        vertexShader = f.read()
    fragmentShader = ""
    with open(g_currentFragmentShaderName) as f:
        fragmentShader = f.read()

    if g_vertexShaderSource != vertexShader or fragmentShader != g_fragmentShaderSource:
        newShader = buildShader(vertexShader, fragmentShader)
        if newShader:
            if g_shader:
                glDeleteProgram(g_shader)
            g_shader = newShader
            print("Reloaded shader, ok!")
        else:
            pass
        g_vertexShaderSource = vertexShader
        g_fragmentShaderSource = fragmentShader


def loadModel(modelName):
    global g_model
    g_model = ObjModel("data/" + modelName)

    g_camera.target = g_model.centre
    g_camera.distance = lu.length(g_model.centre - g_model.aabbMin) * 3.1
    g_lightDistance = lu.length(g_model.centre - g_model.aabbMin) * 1.3


def initResources():
    global g_camera
    global g_lightDistance
    global g_shader
    global g_environmentCubeMap

    loadModel(g_currentModelName)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)
    glEnable(GL_FRAMEBUFFER_SRGB)

    # Build with default first since that really should work, so then we have some fallback
    g_shader = buildShader(g_vertexShaderSource, g_fragmentShaderSource)

    reLoadShader()    


# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 4, part 1", 960, 640, renderFrame, initResources, drawUi, update)
