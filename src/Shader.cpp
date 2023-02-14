#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

#include "glm/glm.hpp"
#include <glm/gtc/type_ptr.hpp>

#include "Shader.h"


void Shader::SetShader(const GLchar* vertexPath, const GLchar* fragmentPath)
{
    // Shaders reading
    std::string vertexCode;
    std::string fragmentCode;
    std::ifstream vShaderFile;
    std::ifstream fShaderFile;

    vShaderFile.exceptions(std::ifstream::badbit);
    fShaderFile.exceptions(std::ifstream::badbit);

    try
    {
        vShaderFile.open(vertexPath);
        fShaderFile.open(fragmentPath);
        std::stringstream vShaderStream, fShaderStream;

        vShaderStream << vShaderFile.rdbuf();
        fShaderStream << fShaderFile.rdbuf();
        vShaderFile.close();
        fShaderFile.close();

        vertexCode = vShaderStream.str();
        fragmentCode = fShaderStream.str();
    }

    catch (std::ifstream::failure e)
    {
        std::cout << "ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ" << std::endl;
    }

    const GLchar* vShaderCode = vertexCode.c_str();
    const GLchar * fShaderCode = fragmentCode.c_str();

    // Shaders compilation
    GLuint vertex, fragment;
    GLint success;
    GLchar infoLog[512];

    // Vertex Shader
    vertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex, 1, &vShaderCode, NULL);
    glCompileShader(vertex);
    glGetShaderiv(vertex, GL_COMPILE_STATUS, &success);

    if (!success)
    {
        glGetShaderInfoLog(vertex, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    // Fragment Shader
    fragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment, 1, &fShaderCode, NULL);
    glCompileShader(fragment);
    glGetShaderiv(fragment, GL_COMPILE_STATUS, &success);

    if (!success)
    {
        glGetShaderInfoLog(fragment, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    // Shader Program
    _program = glCreateProgram();
    glAttachShader(_program, vertex);
    glAttachShader(_program, fragment);
    glLinkProgram(_program);
    glGetProgramiv(_program, GL_LINK_STATUS, &success);

    if (!success)
    {
        glGetProgramInfoLog(_program, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
    }

    glDeleteShader(vertex);
    glDeleteShader(fragment);
}

void Shader::SetUniform1i(const std::string& name, int value)
{
    glUniform1i(GetUniformLocation(name), value);
}

void Shader::SetUniform1f(const std::string& name, float value)
{
    glUniform1f(GetUniformLocation(name), value);
}

void Shader::SetUniform4f(const std::string& name, float f0, float f1, float f2, float f3)
{
    glUniform4f(GetUniformLocation(name), f0, f1, f2, f3);
}

void Shader::SetUniformMat4f(const std::string& name, const glm::mat4& matrix)
{
    glUniformMatrix4fv(GetUniformLocation(name), 1, GL_FALSE, glm::value_ptr(matrix));
}

GLint Shader::GetUniformLocation(const std::string& name) {
    if(_shaderCache.find(name) != _shaderCache.end()) {
        return _shaderCache[name];
    }
    int location = glGetUniformLocation(_program, name.c_str());
    if(location == -1) {
        std::cout << "No active uniform variable with name " << name << " found" << std::endl;
    }
    _shaderCache[name] = location;
    return location;
}

void Shader::UseShader()
{
    glUseProgram(_program);
}
