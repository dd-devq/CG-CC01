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

void Renderer::Clear() const {
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

void Renderer::Init() {
}

void Renderer::Update(const Camera& camera) {

}

void Renderer::Shutdown() const {

}

void Renderer::UpdateView(const Camera& camera) {

}

void Renderer::Render(const Camera& camera, Renderable& renderable , Shader& renderableShader) {
    renderableShader.UseShader();
    renderable.Render();
}