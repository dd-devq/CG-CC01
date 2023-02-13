#pragma once

#include "glad/glad.h"
#include <vector>

#include "glm/vec2.hpp"
#include "glm/vec3.hpp"

struct Vertex {
	using vec2 = glm::vec2;
	using vec3 = glm::vec3;

	Vertex() = default;

	Vertex(const vec3& position, const vec2& texcoords) : Position(position),
	                                                      TexCoords(texcoords) {
	}

	Vertex(const vec3& position, const vec2& texcoords, const vec3& normal) : Position(position),
	                                                                                   TexCoords(texcoords),
	                                                                                   Normal(normal) {
	}

	Vertex(const vec3& position, const vec2& texcoords, const vec3& normal, const vec3& tangent) : Position(position),
	                                                                                               TexCoords(texcoords),
	                                                                                               Normal(normal),
	                                                                                               Tangent(tangent) {
	}

	vec3 Position;
	vec2 TexCoords;
	vec3 Normal;
	vec3 Tangent;
};


// enum BufferType
// {
//     ARRAY = GL_ARRAY_BUFFER,
//     ELEMENT = GL_ELEMENT_ARRAY_BUFFER
// };

// enum DrawMode
// {
//     STATIC = GL_STATIC_DRAW,
//     DYNAMIC = GL_DYNAMIC_DRAW,
//     STREAM = GL_STREAM_DRAW
// };

// class VertexArray
// {
// private:
//     unsigned int _vao{0};
//     std::vector<unsigned int> _vbo;
// public:
//     VertexArray();
//     ~VertexArray();

//     void AddBuffer(const BufferType type, const size_t size, const DrawMode mode, const void *data);
//     void EnableAttribute(const GLuint index, const int size, const GLuint offset, const void *data);

//     void Bind() const;
//     void Unbind() const;
// };
