#version 450 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 color;
layout(location = 1) in vec2 aTex;

out vec2 v_TexCoord;
out vec3 colorInterp;

uniform mat4 u_mvp;

void main() {
  gl_Position = u_mvp * vec4(aPos, 1.0f);
  v_TexCoord = aTex;
  colorInterp = color;
}