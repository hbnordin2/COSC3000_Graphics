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