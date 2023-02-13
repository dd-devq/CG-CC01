#pragma once

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>


#include "glad/glad.h"
#include "GLFW/glfw3.h"

class Shader
{
public:
    Shader() = default;
    ~Shader() = default;
    void SetShader(const GLchar* vertexPath, const GLchar* fragmentPath);
    void UseShader();
    inline GLuint GetProgram() const { return _program; }
    GLint GetUniformLocation(const std::string& name);
    void SetUniform1i(const std::string& name, int value);
    void SetUniform1f(const std::string& name, float value);
    void SetUniform4f(const std::string& name, float f0, float f1, float f2, float f3);
    void SetUniformMat4f(const std::string& name, const glm::mat4& matrix);
private:
    std::unordered_map<std::string, int> _shaderCache;
    GLuint _program;
};