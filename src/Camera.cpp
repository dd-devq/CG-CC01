#include <GLFW/glfw3.h>
#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <string>
#include <vector>

#include "Camera.h"

Camera::Camera(glm::vec3 position, glm::vec3 up, GLfloat yaw, GLfloat pitch) : cameraFront(glm::vec3(0.0f, 0.0f, -1.0f)),
                                                                               cameraSpeed(defaultCameraSpeed),
                                                                               cameraSensitivity(defaultCameraSensitivity),
                                                                               cameraFOV(defaultCameraFOV)
{
    cameraPosition = position;
    worldUp = up;
    cameraYaw = yaw;
    cameraPitch = pitch;
    UpdateCameraVectors();
}

glm::mat4 Camera::GetViewMatrix()
{
    return glm::lookAt(cameraPosition, cameraPosition + cameraFront, cameraUp);
}

void Camera::KeyboardCall(Camera_Movement direction, GLfloat deltaTime)
{
    GLfloat cameraVelocity = cameraSpeed * deltaTime;

    if (direction == FORWARD)
        cameraPosition += cameraFront * cameraVelocity;
    if (direction == BACKWARD)
        cameraPosition -= cameraFront * cameraVelocity;
    if (direction == LEFT)
        cameraPosition -= cameraRight * cameraVelocity;
    if (direction == RIGHT)
        cameraPosition += cameraRight * cameraVelocity;
}

void Camera::MouseCall(GLfloat xOffset, GLfloat yOffset, GLboolean constrainPitch)
{
    xOffset *= cameraSensitivity;
    yOffset *= cameraSensitivity;
    cameraYaw += xOffset;
    cameraPitch += yOffset;

    if (constrainPitch)
    {
        if (cameraPitch > 89.0f)
            cameraPitch = 89.0f;
        if (cameraPitch < -89.0f)
            cameraPitch = -89.0f;
    }

    UpdateCameraVectors();
}

void Camera::ScrollCall(GLfloat yOffset)
{
    if (cameraFOV >= glm::radians(1.0f) && cameraFOV <= glm::radians(45.0f))
        cameraFOV -= glm::radians(yOffset);
    if (cameraFOV <= glm::radians(1.0f))
        cameraFOV = glm::radians(1.0f);
    if (cameraFOV >= glm::radians(45.0f))
        cameraFOV = glm::radians(45.0f);
}

void Camera::UpdateCameraVectors()
{
    glm::vec3 front;
    front.x = cos(glm::radians(cameraYaw)) * cos(glm::radians(cameraPitch));
    front.y = sin(glm::radians(cameraPitch));
    front.z = sin(glm::radians(cameraYaw)) * cos(glm::radians(cameraPitch));

    cameraFront = glm::normalize(front);
    cameraRight = glm::normalize(glm::cross(cameraFront, worldUp));
    cameraUp = glm::normalize(glm::cross(cameraRight, cameraFront));
}
