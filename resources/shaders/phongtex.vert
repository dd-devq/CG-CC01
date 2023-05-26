#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec3 normal;
layout(location = 2) in vec2 texcoord;
uniform mat4 projection, modelview;
out vec3 normal_interp;
out vec3 vertPos;
out vec3 colorInterp;
out vec2 texcoordInterp;

void main(){
  colorInterp = color;
  vec4 vertPos4 = modelview * vec4(position, 1.0);
  vertPos = vec3(vertPos4) / vertPos4.w;

  mat4 normal_matrix = transpose(inverse(modelview));
  normal_interp = vec3(normal_matrix * vec4(normal, 0.0));

  texcoordInterp = texcoord;
  gl_Position = projection * vertPos4;
}

// #version 330 core

// // input attribute variable, given per vertex
// layout(location = 0) in vec3 vertex;
// layout(location = 1) in vec3 normal;
// layout(location = 2) in vec3 color;
// layout(location = 3) in vec2 texcoord;

// uniform mat4 projection, modelview;
// out vec3 normal_interp;
// out vec3 color_interp;
// out vec3 vert_pos;
// out vec2 texcoord_interp;

// void main(){
//   color_interp = color;
//   vec4 vert_pos4 = modelview * vec4(vertex, 1.0);
//   vert_pos = vec3(vert_pos4) / vert_pos4.w;

//   mat4 normal_matrix = transpose(inverse(modelview));
//   normal_interp = vec3(normal_matrix * vec4(normal, 0.0));

//   texcoord_interp = texcoord;
//   gl_Position = projection * vert_pos4;
// }