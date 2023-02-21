#version 450 core

out vec4 FragColor;

in vec2 v_TexCoord;
in vec3 colorInterp;

uniform sampler2D u_Texture;

void main() {
  //   FragColor = texture(u_Texture, v_TexCoord);
  FragColor = vec4(colorInterp, 1);
}