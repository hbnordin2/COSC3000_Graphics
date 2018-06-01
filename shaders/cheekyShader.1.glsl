#version 330
in VertexData
{
    vec2 v2f_textureCoord;
    vec3 v2f_viewSpacePosition;
    vec3 v2f_viewSpaceNormal;
};

out vec4 fragmentColor;

uniform vec3 viewSpaceLightPosition;

uniform sampler2D texture1;

void main(){

    vec3 tmpColor = texture( texture1, v2f_textureCoord ).rgb;

    if (tmpColor.x + tmpColor.y + tmpColor.z < 1.2) {
        tmpColor = vec3(0, 0, 0);
    }

    fragmentColor = vec4(tmpColor.xyz, 0.05);
}