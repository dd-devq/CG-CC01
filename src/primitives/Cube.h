#pragma once

#include "Renderable.h"

namespace CubeData {
	static constexpr GLuint stride = 5;

	static constexpr std::array<GLfloat, 40> vertices = {
        -1.0, -1.0,  1.0, 0.0, 0.0,
         1.0, -1.0,  1.0, 1.0, 0.0,
         1.0,  1.0,  1.0, 1.0, 1.0,
        -1.0,  1.0,  1.0, 0.0, 1.0,
        -1.0, -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, -1.0, 1.0, 1.0,
        -1.0,  1.0, -1.0, 0.0, 1.0
	};

	static constexpr std::array<GLuint, 18> indices = {
        0, 1, 2, 3, 6, 7, 4, 5, 0, 1,  // Front face
        1, 5, 3, 7, 6, 2, 4, 0   
	};

}

class Cube : public Renderable
{
public:
    Cube();
    ~Cube();
    void Render() const;
private:
    void Init();
    void Destroy();
};


Cube::Cube() {
	Init();
}

Cube::~Cube() {
	Destroy();
}

void Cube::Render() const {
    glBindVertexArray(_vao);
	glDrawElements(STRIP, CubeData::vertices.size(), GL_UNSIGNED_INT, nullptr);
}

void Cube::Init() {

	glGenVertexArrays(1, &_vao);
    glBindVertexArray(_vao);

    glGenBuffers(1, &_vbo);
    glBindBuffer(ARRAY, _vbo);
    glBufferData(ARRAY, sizeof(GLfloat) * CubeData::vertices.size(), CubeData::vertices.data(), STATIC);

    glGenBuffers(1, &_ebo);
    glBindBuffer(ELEMENT, _ebo);
    glBufferData(ELEMENT, sizeof(GLfloat) * CubeData::indices.size(), CubeData::indices.data(), STATIC);

	const GLuint position = 0;
	const GLuint texture = 1;
	const GLuint stride = CubeData::stride * sizeof(GLfloat);

	glEnableVertexAttribArray(position);
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, stride, (void*)0);

	glEnableVertexAttribArray(texture);
	glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, stride, (void*)(3 * sizeof(GLfloat)));

}

void Cube::Destroy() {
	glDeleteVertexArrays(1, &_vao);
	glDeleteBuffers(1, &_vbo);
	glDeleteBuffers(1, &_ebo);
}
