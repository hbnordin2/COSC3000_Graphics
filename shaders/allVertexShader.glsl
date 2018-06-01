#version 330
in vec3 positionIn;
in vec3 normalIn;
in vec2 textureCoordIn;

out VertexData
    {
        vec3 fragmentColor;
        vec2 v2f_textureCoord;
        vec3 v2f_viewSpacePosition;
        vec3 v2f_viewSpaceNormal;
    };

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;

void main(){

    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionIn, 1.0)).xyz;
    v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalIn);
    v2f_textureCoord = textureCoordIn;

    gl_Position = modelToClipTransform * vec4(positionIn, 1.0);
}