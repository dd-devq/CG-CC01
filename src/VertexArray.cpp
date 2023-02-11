#include "VertexArray.h"


VertexArray::VertexArray()
{
    glGenVertexArrays(1, &_vao);
    glBindVertexArray(_vao);
}

VertexArray::~VertexArray()
{
    glDeleteVertexArrays(1, &_vao);
    for (auto& vbo : _vbo) {
        glDeleteBuffers(1, &vbo);
    }
    _vbo.clear();
}

void VertexArray::AddBuffer(const BufferType type, const size_t size, const DrawMode mode, const void *data)
{
    GLuint vbo{0};
    glGenBuffers(1, &vbo);
    glBindBuffer(type, vbo);
    glBufferData(type, size, data, mode);
    _vbo.push_back(vbo);
}

void VertexArray::EnableAttribute(const GLuint index, const int size, const GLuint stride, const void *offset) 
{
    glEnableVertexAttribArray(index);
    glVertexAttribPointer(index, size, GL_FLOAT, GL_FALSE, stride, offset);
}

void VertexArray::Bind() const
{
    glBindVertexArray(_vao);
}

void VertexArray::Unbind() const
{
    glBindVertexArray(0);
}
