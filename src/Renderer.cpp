#include "Renderer.h"

#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "glad/glad.h"
#include <GLFW/glfw3.h>
#include <iostream>

Renderer::Renderer() {
    Init();
}

Renderer::~Renderer() {
    Shutdown();
}

void Renderer::Init() {
    std::cout << "Init" <<std::endl;
}

void Renderer::Update(const Camera& camera) {

}

void Renderer::Shutdown() const {

}

void Renderer::UpdateView(const Camera& camera) {

}

void Renderer::Render(const Camera& camera, Renderable& renderable , Shader& renderableShader) {
    renderableShader.UseShader();
    glDrawElements(GL_TRIANGLE_STRIP, renderable.GetIndicesCount(), GL_UNSIGNED_INT, nullptr);
}