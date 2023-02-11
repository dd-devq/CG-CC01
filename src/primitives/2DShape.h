#pragma once

#include "VertexArray.h"
#include "Renderable.h"

float positions[] = {
    0.5f, 0.5f,
    0.5f, -0.5f,
    -0.5f, 0.5f,
    -0.5f, -0.5f
};

unsigned int indices[] = {
    3, 2, 1, 0
};

class Rectangle: public Renderable {
public:
    Rectangle() {
        _vao.AddBuffer(ARRAY,  2 * 4 * sizeof(float), STATIC, positions);
        _vao.AddBuffer(ELEMENT, 4 * sizeof(unsigned int), STATIC, indices);
        _vao.EnableAttribute(0, 2, 2 * sizeof(float), (void*)0);
        // _vao.EnableAttribute(1, 2, 4 * sizeof(float), (void*)(2 * sizeof(float)));
        _vao.Bind();
    }

    ~Rectangle() {
        _vao.Unbind();
    }

    inline unsigned int GetIndicesCount() const { return 4; }
};