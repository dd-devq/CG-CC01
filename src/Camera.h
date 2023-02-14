#pragma once

#include <GLFW/glfw3.h>
#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <string>
#include <vector>

const GLfloat defaultCameraYaw = -90.0f;
const GLfloat defaultCameraPitch = 0.0f;
const GLfloat defaultCameraSpeed = 2.0f;
const GLfloat defaultCameraSensitivity = 0.10f;
const GLfloat defaultCameraFOV = 45.0f;

enum CameraMovement
{
    FORWARD,
    BACKWARD,
    LEFT,
    RIGHT
};

class Camera
{
public:
    glm::vec3 Position;
    glm::vec3 Front;
    glm::vec3 Up;
    glm::vec3 Right;
    glm::vec3 WorldUp;
    GLfloat Yaw;
    GLfloat Pitch;
    GLfloat Speed;
    GLfloat Sensitivity;
    GLfloat FOV;

    Camera(glm::vec3 position = glm::vec3(0.0f, 0.0f, 0.0f), glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f), GLfloat yaw = defaultCameraYaw, GLfloat pitch = defaultCameraPitch);
    ~Camera() = default;
    glm::mat4 GetViewMatrix();
    void KeyboardCall(CameraMovement direction, GLfloat deltaTime);
    void MouseCall(GLfloat xOffset, GLfloat yOffset, GLboolean constrainPitch = true);
    void ScrollCall(GLfloat yOffset);

private:
    void UpdateCameraVectors();
};

