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
    
    float shading = max(0.0, dot(normalize(viewSpaceLightPosition-v2f_viewSpacePosition), v2f_viewSpaceNormal));
    float distance = length(viewSpaceLightPosition-v2f_viewSpacePosition);
    float attenuation = 1/(1 + 0.000000025 * distance + 0.00003 * distance * distance);

    vec3 tmpColor = texture( texture1, v2f_textureCoord ).rgb;

    fragmentColor = vec4(tmpColor.xyz * shading * attenuation + 0.05 * tmpColor.xyz, 1.0);
}