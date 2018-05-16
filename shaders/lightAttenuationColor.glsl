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

    // fragmentColor = vec4(sphereColour.xyz * shading * attenuation + vec3(0.2, 0.0, 0.0), sphereColour.w);
    fragmentColor = vec4(sphereColour.xyz * shading * attenuation + vec3(0.2, 0.0, 0.0), 0.2);
}