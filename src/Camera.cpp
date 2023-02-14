#include <GLFW/glfw3.h>
#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <string>
#include <vector>

#include "Camera.h"

Camera::Camera(glm::vec3 position, glm::vec3 up, GLfloat yaw, GLfloat pitch) : Front(glm::vec3(0.0f, 0.0f, -1.0f)),
                                                                               Speed(defaultCameraSpeed),
                                                                               Sensitivity(defaultCameraSensitivity),
                                                                               FOV(defaultCameraFOV)
{
    Position = position;
    WorldUp = up;
    Yaw = yaw;
    Pitch = pitch;
    UpdateCameraVectors();
}

glm::mat4 Camera::GetViewMatrix()
{
    return glm::lookAt(Position, Position + Front, Up);
}

void Camera::KeyboardCall(CameraMovement direction, GLfloat deltaTime)
{
    GLfloat Velocity = Speed * deltaTime;

    if (direction == FORWARD)
        Position += Front * Velocity;
    if (direction == BACKWARD)
        Position -= Front * Velocity;
    if (direction == LEFT)
        Position -= Right * Velocity;
    if (direction == RIGHT)
        Position += Right * Velocity;
}

void Camera::MouseCall(GLfloat xOffset, GLfloat yOffset, GLboolean constrainPitch)
{
    xOffset *= Sensitivity;
    yOffset *= Sensitivity;
    Yaw += xOffset;
    Pitch += yOffset;

    if (constrainPitch)
    {
        if (Pitch > 89.0f)
            Pitch = 89.0f;
        if (Pitch < -89.0f)
            Pitch = -89.0f;
    }

    UpdateCameraVectors();
}

void Camera::ScrollCall(GLfloat yOffset)
{
    if (FOV >= 1.0f && FOV <= 45.0f) {
        FOV -= yOffset;
    }
    else if (FOV <= 1.0f) {
        FOV = 1.0f;
    }
    else if (FOV >= 45.0f) {
        FOV = 45.0f;
    }
}

void Camera::UpdateCameraVectors()
{
    glm::vec3 front;
    front.x = cos(glm::radians(Yaw)) * cos(glm::radians(Pitch));
    front.y = sin(glm::radians(Pitch));
    front.z = sin(glm::radians(Yaw)) * cos(glm::radians(Pitch));

    Front = glm::normalize(front);
    Right = glm::normalize(glm::cross(Front, WorldUp));
    Up = glm::normalize(glm::cross(Right, Front));
}
