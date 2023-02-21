#include "Camera.h"
#include "Renderer.h"
#include "2DShape.h"
#include "Shader.h"
#include "Texture.h"
#include <iostream>
#include "Cube.h"

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

const char * DEFAULT_VERTEX_SHADER = "../../resources/shader/default.vert";
const char * DEFAULT_FRAGMENT_SHADER = "../../resources/shader/default.frag";



Camera camera(glm::vec3(0.0f, 0.0f, 4.0f));
float lastX = 0.0f;
float lastY = 0.0f;
GLfloat deltaTime = 0.0f;
GLfloat lastFrame = 0.0f;
bool firstMouse = true;
bool cameraMode = false;
bool keys[1024];
GLfloat modelRotationSpeed = 0.0f;
glm::vec3 modelPosition = glm::vec3(0.0f);
glm::vec3 modelRotationAxis = glm::vec3(0.0f, 1.0f, 0.0f);
glm::vec3 modelScale = glm::vec3(0.75f);


class Application {
public:
    Application();
    ~Application() = default;

    void InitGLFWWindow(const char* title);
    void Run();
    void Shutdown() {};
    void CameraMove();

    GLFWwindow* _window {nullptr};
    Renderer _renderer;
};

void KeyboardCallback(GLFWwindow* window, int key, int scancode, int action, int mode)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GL_TRUE);

    if (key >= 0 && key < 1024)
    {
        if (action == GLFW_PRESS)
            keys[key] = true;
        else if (action == GLFW_RELEASE)
            keys[key] = false;
    }
}


void MousePositionCallback(GLFWwindow *window, double xPos, double yPos)
{
    if (!window) {
        return;
    }

    if (firstMouse) {
        lastX = xPos;
        lastY = yPos;
        firstMouse = false;
    }

    GLfloat xOffset = xPos - lastX;
    GLfloat yOffset = lastY - yPos;
    lastX = xPos;
    lastY = yPos;

    if (cameraMode) {
        camera.MouseCall(xOffset, yOffset);
    }
}


void MouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
    if (!window) {
        return;
    }

    if (button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS) {
        cameraMode = true;
    }
    else {
        cameraMode = false;
    }
}


void ScrollCallback(GLFWwindow* window, double xOffset, double yOffset)
{
    if (!window) {
        return;
    }

    std::cout << "OFFSET: (" << xOffset << ", " << yOffset << ")";

    if (cameraMode) {
        camera.ScrollCall(yOffset);
    }
}


Application::Application() {
    InitGLFWWindow("Sandbox");
}

void Application::InitGLFWWindow(const char* title) {

    if(!glfwInit()) {
        return;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);
    glfwWindowHint(GLFW_DOUBLEBUFFER, GL_TRUE);
    glfwWindowHint(GLFW_SAMPLES, 16);

    GLFWmonitor* glfwMonitor = glfwGetPrimaryMonitor();
    const GLFWvidmode* glfwMode = glfwGetVideoMode(glfwMonitor);

    glfwWindowHint(GLFW_RED_BITS, glfwMode->redBits);
    glfwWindowHint(GLFW_GREEN_BITS, glfwMode->greenBits);
    glfwWindowHint(GLFW_BLUE_BITS, glfwMode->blueBits);
    glfwWindowHint(GLFW_REFRESH_RATE, glfwMode->refreshRate);

    int WIDTH = glfwMode->width;
    int HEIGHT = glfwMode->height;
    lastX = WIDTH / 2;
    lastY = HEIGHT / 2;

    _window = glfwCreateWindow(WIDTH, HEIGHT, title, nullptr, nullptr);

    if(!_window)
    {
        glfwTerminate();
        std::cerr << "ERROR::GLFW::Could not initialise GLFW Window" << '\n';
        return;
    }

    glfwMakeContextCurrent(_window);
    glfwSetInputMode(_window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cerr << "Failed to initialize GLAD" << std::endl;
        return;
    }

    std::cout << "OpenGL version: " << glGetString(GL_VERSION) << std::endl;
    std::cout << "GLSL version: " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;
    std::cout << "Vendor: " << glGetString(GL_VENDOR) << std::endl;
    std::cout << "Renderer: " << glGetString(GL_RENDERER) << std::endl;
    
    glViewport(0, 0, WIDTH, HEIGHT);
    glEnable(GL_BLEND);
    glEnable(GL_MULTISAMPLE);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glfwSetKeyCallback(_window, KeyboardCallback);
    glfwSetMouseButtonCallback(_window, MouseButtonCallback);
    glfwSetCursorPosCallback(_window, MousePositionCallback);
    glfwSetScrollCallback(_window, ScrollCallback);
}

void Application::CameraMove() {
    if (keys[GLFW_KEY_W])
        camera.KeyboardCall(FORWARD, deltaTime);
    if (keys[GLFW_KEY_S])
        camera.KeyboardCall(BACKWARD, deltaTime);
    if (keys[GLFW_KEY_A])
        camera.KeyboardCall(LEFT, deltaTime);
    if (keys[GLFW_KEY_D])
        camera.KeyboardCall(RIGHT, deltaTime);
}

void Application::Run() {
    Cube cube;
    Shader rectangleShader;
    Texture rectangleTexture;
    rectangleShader.SetShader(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER);
    rectangleTexture.SetTexture("../../resources/texture/Lion.jpg", "Wood", true);
    rectangleTexture.UseTexture();
    rectangleShader.SetUniform1i("u_Texture", 0);


    while(!glfwWindowShouldClose(_window)) {

        GLfloat currentFrame = glfwGetTime();
        deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;

        glfwPollEvents();

        CameraMove();

        _renderer.Clear();

        rectangleShader.UseShader();

        glm::mat4 projection = glm::perspective(glm::radians(camera.FOV), (float)1280 / (float)720, 0.1f, 100.0f);
        glm::mat4 view = camera.GetViewMatrix();

        GLfloat rotationAngle = glfwGetTime() / 5.0f * modelRotationSpeed;
        glm::mat4 model(1.0f);
        model = glm::translate(model, modelPosition);
        model = glm::rotate(model, rotationAngle, modelRotationAxis);
        model = glm::scale(model, modelScale);

        glm::mat4 u_mvp = projection * view * model;

        rectangleShader.SetUniformMat4f("u_mvp", u_mvp);

        _renderer.Render(camera, cube, rectangleShader);


        glfwSwapBuffers(_window);
    }
}

int main() {
    auto app = new Application();
    app->Run();
    return 0;
}