#pragma once

#include "Renderable.h"


/*

        #       F ----- G
        #   E ----- H   |
        #   |   |   |   |
        #   |   B --|-- C
        #   A ----- D


*/

namespace CubeData {
	static constexpr GLuint stride = 8;

	static constexpr std::array<GLfloat, 64> vertices = {
        -1.0, -1.0,  1.0, 0.0, 0.0, 1.0, 0.0, 0.0, // A
         1.0, -1.0,  1.0, 0.0, 0.0, 0.0, 1.0, 0.0, // D
         1.0,  1.0,  1.0, 1.0, 0.0, 0.0, 1.0, 1.0, // H
        -1.0,  1.0,  1.0, 0.0, 1.0, 1.0, 0.0, 1.0, // E
        -1.0, -1.0, -1.0, 0.0, 1.0, 0.0, 1.0, 0.0, // B
         1.0, -1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 0.0, // C
         1.0,  1.0, -1.0, 1.0, 1.0, 1.0, 0.0, 1.0, // G
        -1.0,  1.0, -1.0, 1.0, 0.0, 1.0, 1.0, 1.0  // F
	};

	static constexpr std::array<GLuint, 14> indices = {
        7, 6, 4, 5, 1, 6, 2, 7, 3, 4, 0, 1, 3, 2
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
	glDrawElements(STRIP, CubeData::indices.size(), GL_UNSIGNED_INT, nullptr);
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
	const GLuint color = 1;
	const GLuint texture = 2;
	const GLuint stride = CubeData::stride * sizeof(GLfloat);

	glEnableVertexAttribArray(position);
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, stride, (void*)0);

	glEnableVertexAttribArray(color);
	glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, stride, (void*)(3 * sizeof(GLfloat)));


	glEnableVertexAttribArray(texture);
	glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, stride, (void*)(6 * sizeof(GLfloat)));

}

void Cube::Destroy() {
	glDeleteVertexArrays(1, &_vao);
	glDeleteBuffers(1, &_vbo);
	glDeleteBuffers(1, &_ebo);
}
