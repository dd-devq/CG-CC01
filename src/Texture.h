#pragma once

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include "glad/glad.h"


class Texture {
public:
    Texture() = default;
    ~Texture();
    void SetTexture(const char* path, std::string name, bool flip);
    void UseTexture() const;

    inline GLuint GetWidth() const { return _width; }
    inline GLuint GetHeight() const { return _height; }
    inline std::string GetName() const { return _name; }

private:
    GLuint _id, _width, _height, _components;
    std::string _name;
    GLenum _type, _internalFormat, _format;
};