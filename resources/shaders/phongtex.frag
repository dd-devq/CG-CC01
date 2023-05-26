#version 330 core

precision mediump float;
in vec3 normal_interp;  // Surface normal
in vec3 vertPos;       // Vertex position
in vec3 colorInterp;
in vec2 texcoordInterp;

uniform mat3 K_materials;
uniform mat3 I_light;

uniform int mode;   // Rendering mode
uniform float shininess; // Shininess
uniform vec3 light_pos; // Light position
out vec4 fragColor;

uniform sampler2D texture;

void main() {
  vec3 N = normalize(normal_interp);
  vec3 L = normalize(light_pos - vertPos);
  vec3 R = reflect(-L, N);      // Reflected light vector
  vec3 V = normalize(-vertPos); // Vector to viewer

  float specAngle = max(dot(R, V), 0.0);
  float specular = pow(specAngle, shininess);
  vec3 g = vec3(max(dot(L, N), 0.0), specular, 1.0);
  vec3 rgb = 0.5*matrixCompMult(K_materials, I_light) * g + 0.5*colorInterp;

  // fragColor = vec4(rgb, 1.0);
  fragColor = texture2D(texture, texcoordInterp);
}

// #version 330 core

// precision mediump float;
// in vec3 normal_interp;  // Surface normal
// in vec3 vert_pos;       // Vertex position
// in vec3 color_interp;
// in vec2 texcoord_interp;

// uniform mat3 K_materials;
// uniform mat3 I_light;

// uniform float phong_factor; // Shininess
// uniform float shininess; // Shininess
// uniform vec3 light_pos; // Light position
// out vec4 fragColor;


// uniform sampler2D texture;

// void main() {
//   vec3 N = normalize(normal_interp);
//   vec3 L = normalize(light_pos - vert_pos);
//   vec3 R = reflect(-L, N);      // Reflected light vector
//   vec3 V = normalize(-vert_pos); // Vector to viewer

//   vec3 lv = light_pos - vert_pos;
//   float lvd = 1.0/(dot(lv, lv));
//   float specAngle = max(dot(R, V), 0.0);
//   float specular = pow(specAngle, shininess);
//   vec3 g = vec3(lvd*max(dot(L, N), 0.0), specular, 1.0);
//   vec3 rgb = matrixCompMult(K_materials, I_light) * g; // +  colorInterp;

//   fragColor = vec4(rgb, 1.0);
//   vec4 color_interp4 = vec4(color_interp, 1.0);
//   float color_factor = 0.2;
//   float texture_factor = 1.0 - (color_factor + phong_factor);
//   fragColor = color_factor*color_interp4 + phong_factor*fragColor + texture_factor*texture2D(texture, texcoord_interp);
// }