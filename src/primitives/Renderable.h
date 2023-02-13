#pragma once

#include <vector>
#include <array>

#include "glad/glad.h"

enum BufferType
{
    ARRAY = GL_ARRAY_BUFFER,
    ELEMENT = GL_ELEMENT_ARRAY_BUFFER
};

enum DrawMode
{
    STATIC = GL_STATIC_DRAW,
    DYNAMIC = GL_DYNAMIC_DRAW,
    STREAM = GL_STREAM_DRAW
};

enum RenderPrimitive {
    TRIANGLE = GL_TRIANGLES,
    STRIP = GL_TRIANGLE_STRIP,
    FAN = GL_TRIANGLE_FAN
};

class Renderable {
public:
    Renderable() {};
    virtual ~Renderable() {};
    virtual void Render() const = 0;
protected:
    virtual void Init() = 0;
    virtual void Destroy() = 0;
    GLuint _vao, _vbo, _ebo;
};