#pragma once

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

#include "glad/glad.h"
#include "GLFW/glfw3.h"

class Shader
{
public:
    Shader() = default;
    ~Shader() = default;
    void SetShader(const GLchar* vertexPath, const GLchar* fragmentPath);
    void UseShader();
private:
    GLuint _program;
};