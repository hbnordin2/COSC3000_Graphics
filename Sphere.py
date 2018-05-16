from lab_utils import *
from math import *

class Sphere:
    # Recursively subdivide a triangle with its vertices on the surface of the unit sphere such that the new vertices also are on part of the unit sphere.
    @staticmethod
    def subDivide(dest, v0, v1, v2, level):
        #If the level index/counter is non-zero...
        if level:
            # ...we subdivide the input triangle into four equal sub-triangles
            # The mid points are the half way between to vertices, which is really (v0 + v2) / 2, but 
            # instead we normalize the vertex to 'push' it out to the surface of the unit sphere.
            v3 = normalize(v0 + v1);
            v4 = normalize(v1 + v2);
            v5 = normalize(v2 + v0);

            # ...and then recursively call this function for each of those (with the level decreased by one)
            subDivide(dest, v0, v3, v5, level - 1);
            subDivide(dest, v3, v4, v5, level - 1);
            subDivide(dest, v3, v1, v4, level - 1);
            subDivide(dest, v5, v4, v2, level - 1);
        else:
            # If we have reached the terminating level, just output the vertex position
            dest.append(v0)
            dest.append(v1)
            dest.append(v2)

    @staticmethod
    def createSphere(numSubDivisionLevels):
        sphereVerts = []

        # The root level sphere is formed from 8 triangles in a diamond shape (two pyramids)
        subDivide(sphereVerts, vec3(0, 1, 0), vec3(0, 0, 1), vec3(1, 0, 0), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, 1, 0), vec3(1, 0, 0), vec3(0, 0, -1), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, 1, 0), vec3(0, 0, -1), vec3(-1, 0, 0), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, 1, 0), vec3(-1, 0, 0), vec3(0, 0, 1), numSubDivisionLevels)

        subDivide(sphereVerts, vec3(0, -1, 0), vec3(1, 0, 0), vec3(0, 0, 1), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, -1, 0), vec3(0, 0, 1), vec3(-1, 0, 0), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, -1, 0), vec3(-1, 0, 0), vec3(0, 0, -1), numSubDivisionLevels)
        subDivide(sphereVerts, vec3(0, -1, 0), vec3(0, 0, -1), vec3(1, 0, 0), numSubDivisionLevels)

        return sphereVerts;

    @staticmethod
    def makeBetterSphere(divisions):
        x = 0
        y = 0
        z = 0
        r = 20
        
        dTheta=180.0/divisions
        
        dLon=360.0/divisions
        
        degToRad=3.14/180

        vertices = []

        lat = 0
        while(lat <= 180):

            lon = 0
            while(lon <= 360):
                x = r*cos(lat * degToRad) * sin(lon * degToRad)
                y = r*sin(lat * degToRad) * sin(lon * degToRad)
                z = r*cos(lon * degToRad)

                vertices.append([x, y, z])

                x = r*cos((lat + dTheta) * degToRad) * sin(lon * degToRad)
                y = r*sin((lat + dTheta) * degToRad) * sin(lon * degToRad)
                z = r*cos( lon * degToRad )

                vertices.append([x,y,z])

                lon += dLon

            lat += dTheta

        return vertices

    @staticmethod 
    def getUV(vertices):
        uv = []
        for i in vertices:
            Z = i[2]
            X = i[0]
            Y = i[1]
            U = (-Z/abs(X) + 1)/2
            V = (-Y/abs(X) + 1)/2
            uv.append([U,V])
        return uv

    # TODO: EXPAND LU FUNCTIONS OUT SO YOU CAN SEE AND CONTROL THEM (WE DON'T NEED ANY OF THEM IN REALITY)
    # https://learnopengl.com/code_viewer_gh.php?code=src/2.lighting/4.2.lighting_maps_specular_map/lighting_maps_specular.cpp
    @staticmethod
    def drawSphereWithShader(position, radius, sphereColour, viewToClipTransform, worldToViewTransform, viewSpaceLightPosition, shader):
        # same as
        # g_sphereVertexArrayObject = glGenVertexArrays(1);
        g_sphereVertexArrayObject = createVertexArrayObject()
        sphereVerts = Sphere.createSphere(3)
        # uv = Sphere.getUV(sphereVerts)
        # sphereVerts = Sphere.makeBetterSphere(20)

        g_numSphereVerts = len(sphereVerts)
        g_sphereVertexArrayObject = createVertexArrayObject()

        # Load up buffer

        # Vertex locations
        createAndAddVertexArrayData(g_sphereVertexArrayObject, sphereVerts, 0)
        # Normals
        createAndAddVertexArrayData(g_sphereVertexArrayObject, sphereVerts, 1)
        # TexCoords
        # createAndAddVertexArrayData(g_sphereVertexArrayObject, uv, 2)



        # Bind buffer to vertex array
        glBindVertexArray(g_sphereVertexArrayObject)

        g_sphereShader = shader

        glUseProgram(g_sphereShader)
        setUniform(g_sphereShader, "sphereColour", sphereColour)

        modelToWorldTransform = make_translation(position[0], position[1], position[2]) * make_scale(radius, radius, radius);
        # modelToWorldTransform = make_translation(position[0], position[1], position[2])
        modelToClipTransform = viewToClipTransform * worldToViewTransform * modelToWorldTransform
        modelToViewTransform = worldToViewTransform * modelToWorldTransform
        modelToViewNormalTransform = inverse(transpose(Mat3(modelToViewTransform)))
        setUniform(g_sphereShader, "modelToClipTransform", modelToClipTransform)
        setUniform(g_sphereShader, "modelToViewTransform", modelToViewTransform)
        setUniform(g_sphereShader, "modelToViewNormalTransform", modelToViewNormalTransform)
        setUniform(g_sphereShader, "viewSpaceLightPosition", viewSpaceLightPosition)

        # Draw everything in the vertex buffers
        glDrawArrays(GL_TRIANGLES, 0, g_numSphereVerts)

    @staticmethod
    def makeShader():        
        vertexShader = """
            #version 330
            in vec3 positionIn;
            in vec3 normalIn;

            uniform mat4 modelToClipTransform;
            uniform mat4 modelToViewTransform;
            uniform mat3 modelToViewNormalTransform;

            // 'out' variables declared in a vertex shader can be accessed in the subsequent stages.
            // For a fragment shader the variable is interpolated (the type of interpolation can be modified, try placing 'flat' in front here and in the fragment shader!).
            out VertexData
            {
                vec3 v2f_viewSpacePosition;
                vec3 v2f_viewSpaceNormal;
            };

            void main() 
            {
                v2f_viewSpacePosition = (modelToViewTransform * vec4(positionIn, 1.0)).xyz;
                v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalIn);

                // gl_Position is a buit-in 'out'-variable that gets passed on to the clipping and rasterization stages (hardware fixed function).
                // it must be written by the vertex shader in order to produce any drawn geometry. 
                // We transform the position using one matrix multiply from model to clip space. Note the added 1 at the end of the position to make the 3D
                // coordinate homogeneous.
                gl_Position = modelToClipTransform * vec4(positionIn, 1.0);
            }
"""

        fragmentShader = """
            #version 330
            // Input from the vertex shader, will contain the interpolated (i.e., area weighted average) vaule out put for each of the three vertex shaders that 
            // produced the vertex data for the triangle this fragmet is part of.
            in VertexData
            {
                vec3 v2f_viewSpacePosition;
                vec3 v2f_viewSpaceNormal;
            };

            // Other uniforms used by the shader
            uniform vec4 sphereColour;

            uniform vec3 viewSpaceLightPosition;
            uniform vec3 lightColourAndIntensity;
            uniform vec3 ambientLightColourAndIntensity;


            out vec4 fragmentColor;

            void main() 
            {
                float shading = max(0.0, dot(normalize(viewSpaceLightPosition-v2f_viewSpacePosition), v2f_viewSpaceNormal));

                float distance = length(viewSpaceLightPosition-v2f_viewSpacePosition);
                float attenuation = 1/(1.0 + 0.00000005 * distance + 0.00002 * distance * distance);

                fragmentColor = vec4(sphereColour.xyz * shading * attenuation + vec3(0.2, 0.0, 0.0), sphereColour.w);
            }
"""
        g_sphereShader = buildShader([vertexShader], [fragmentShader], {"positionIn" : 0, "normalIn" : 1})

        return g_sphereShader



    @staticmethod
    def drawSphere(position, radius, sphereColour, viewToClipTransform, worldToViewTransform):
        g_sphereVertexArrayObject = None
        g_sphereShader = None
        g_numSphereVerts = 0

        modelToWorldTransform = make_translation(position[0], position[1], position[2]) * make_scale(radius, radius, radius);

        sphereVerts = createSphere(3)
        g_numSphereVerts = len(sphereVerts)
        g_sphereVertexArrayObject = createVertexArrayObject()
        createAndAddVertexArrayData(g_sphereVertexArrayObject, sphereVerts, 0)
        # redundantly add as normals...
        createAndAddVertexArrayData(g_sphereVertexArrayObject, sphereVerts, 1)



        vertexShader = """
            #version 330
            in vec3 positionIn;
            in vec3 normalIn;

            uniform mat4 modelToClipTransform;
            uniform mat4 modelToViewTransform;
            uniform mat3 modelToViewNormalTransform;

            // 'out' variables declared in a vertex shader can be accessed in the subsequent stages.
            // For a fragment shader the variable is interpolated (the type of interpolation can be modified, try placing 'flat' in front here and in the fragment shader!).
            out VertexData
            {
                vec3 v2f_viewSpacePosition;
                vec3 v2f_viewSpaceNormal;
            };

            void main() 
            {
                v2f_viewSpacePosition = (modelToViewTransform * vec4(positionIn, 1.0)).xyz;
                v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalIn);

                // gl_Position is a buit-in 'out'-variable that gets passed on to the clipping and rasterization stages (hardware fixed function).
                // it must be written by the vertex shader in order to produce any drawn geometry. 
                // We transform the position using one matrix multiply from model to clip space. Note the added 1 at the end of the position to make the 3D
                // coordinate homogeneous.
                gl_Position = modelToClipTransform * vec4(positionIn, 1.0);
            }
"""

        fragmentShader = """
            #version 330
            // Input from the vertex shader, will contain the interpolated (i.e., area weighted average) vaule out put for each of the three vertex shaders that 
            // produced the vertex data for the triangle this fragmet is part of.
            in VertexData
            {
                vec3 v2f_viewSpacePosition;
                vec3 v2f_viewSpaceNormal;
            };

            // Other uniforms used by the shader
            uniform vec4 sphereColour;

            uniform vec3 viewSpaceLightPosition;
            uniform vec3 lightColourAndIntensity;
            uniform vec3 ambientLightColourAndIntensity;


            out vec4 fragmentColor;

            void main() 
            {
                float shading = max(0.0, dot(normalize(-v2f_viewSpacePosition), v2f_viewSpaceNormal));
                fragmentColor = vec4(sphereColour.xyz * shading, sphereColour.w);

            }
"""
        g_sphereShader = buildShader([vertexShader], [fragmentShader], {"positionIn" : 0, "normalIn" : 1})


        glUseProgram(g_sphereShader)
        setUniform(g_sphereShader, "sphereColour", sphereColour)

        modelToClipTransform = viewToClipTransform * worldToViewTransform * modelToWorldTransform
        modelToViewTransform = worldToViewTransform * modelToWorldTransform
        modelToViewNormalTransform = inverse(transpose(Mat3(modelToViewTransform)))
        setUniform(g_sphereShader, "modelToClipTransform", modelToClipTransform);
        setUniform(g_sphereShader, "modelToViewTransform", modelToViewTransform);
        setUniform(g_sphereShader, "modelToViewNormalTransform", modelToViewNormalTransform);


        glBindVertexArray(g_sphereVertexArrayObject)
        glDrawArrays(GL_TRIANGLES, 0, g_numSphereVerts)