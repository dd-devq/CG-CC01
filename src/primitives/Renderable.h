#pragma once

#include "VertexArray.h"

class Renderable {
public:
    Renderable() = default;
    virtual ~Renderable() = default;
    virtual unsigned int GetIndicesCount() const = 0;
protected:
    VertexArray _vao;
};