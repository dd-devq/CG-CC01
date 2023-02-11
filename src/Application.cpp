#include "Camera.h"
#include "Renderer.h"
#include "2DShape.h"
#include "Shader.h"
#include <iostream>

const char * DEFAULT_VERTEX_SHADER = "../../resources/shader/default.vert";
const char * DEFAULT_FRAGMENT_SHADER = "../../resources/shader/default.frag";



Camera camera(glm::vec3(0.0f, 0.0f, 4.0f));
float lastX = 0.0f;
float lastY = 0.0f;
bool firstMouse = true;
bool cameraMode = false;
bool keys[1024];

class Application {
public:
    Application();
    ~Application() = default;

    void InitGLFWWindow(const char* title);
    void Run();
    void Shutdown() {};

    GLFWwindow* _window {nullptr};
    Renderer _renderer;
private:
    friend void KeyboardCallback(GLFWwindow *window, int key, int scancode, int action, int mods);
    friend void MouseButtonCallback(GLFWwindow *window, int button, int action, int mods);
    friend void MousePositionCallback(GLFWwindow *window, double xPos, double yPos);
    friend void ScrollCallback(GLFWwindow* window, double xOffset, double yOffset);
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
    if (firstMouse)
    {
        lastX = xPos;
        lastY = yPos;
        firstMouse = false;
    }

    GLfloat xOffset = xPos - lastX;
    GLfloat yOffset = lastY - yPos;
    lastX = xPos;
    lastY = yPos;

    if (cameraMode)
        camera.MouseCall(xOffset, yOffset);
}


void MouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
    if (button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS)
        cameraMode = true;
    else
        cameraMode = false;
}


void ScrollCallback(GLFWwindow* window, double xOffset, double yOffset)
{
    if (cameraMode)
        camera.ScrollCall(yOffset);
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



void Application::Run() {
    Rectangle rectangle;
    Shader rectangleShader;
    rectangleShader.SetShader(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER);
    
    while(!glfwWindowShouldClose(_window)) {
        glfwPollEvents();
        glfwSwapBuffers(_window);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        _renderer.Render(camera, rectangle, rectangleShader);
    }
}

int main() {
    auto app = new Application();
    app->Run();
    return 0;
}