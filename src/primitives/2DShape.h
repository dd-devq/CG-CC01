#pragma once

#include "Renderable.h"


namespace RectangleData {

	static constexpr GLuint stride = 5;

	static constexpr std::array<GLfloat, 20> vertices = {
		0.5f,  0.5f, 0.0f, 1.0f, 1.0f,   // Top right
		0.5f, -0.5f, 0.0f, 1.0f, 0.0f,   // Bottom right
		-0.5f, -0.5f, 0.0f, 0.0f, 0.0f,  // Bottom left
		-0.5f,  0.5f, 0.0f, 0.0f, 1.0f   // Top left	
	};

	static constexpr std::array<GLuint, 4> indices = {
		0, 1, 3, 2
	};
};

class Rectangle: public Renderable {
public:
    Rectangle();

    ~Rectangle();

	void Render() const;

private:
    void Init();

    void Destroy();

};

Rectangle::Rectangle() {
	Init();
}

Rectangle::~Rectangle() {
	Destroy();
}

void Rectangle::Render() const {
    glBindVertexArray(_vao);
	glDrawElements(STRIP, RectangleData::indices.size(), GL_UNSIGNED_INT, nullptr);
}

void Rectangle::Init() {

	glGenVertexArrays(1, &_vao);
    glBindVertexArray(_vao);

    glGenBuffers(1, &_vbo);
    glBindBuffer(ARRAY, _vbo);
    glBufferData(ARRAY, sizeof(GLfloat) * RectangleData::vertices.size(), RectangleData::vertices.data(), STATIC);

    glGenBuffers(1, &_ebo);
    glBindBuffer(ELEMENT, _ebo);
    glBufferData(ELEMENT, sizeof(GLfloat) * RectangleData::indices.size(), RectangleData::indices.data(), STATIC);

	const GLuint position = 0;
	const GLuint texture = 1;
	const GLuint stride = RectangleData::stride * sizeof(GLfloat);

	glEnableVertexAttribArray(position);
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, stride, (void*)0);

	glEnableVertexAttribArray(texture);
	glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, stride, (void*)(3 * sizeof(GLfloat)));

}

void Rectangle::Destroy() {
	glDeleteVertexArrays(1, &_vao);
	glDeleteBuffers(1, &_vbo);
	glDeleteBuffers(1, &_ebo);
}