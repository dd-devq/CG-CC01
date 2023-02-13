#pragma once

#include <unordered_map>
#include <vector>
#include "primitives/Renderable.h"
#include "Camera.h"
#include "Shader.h"



class Renderer {
public:
	Renderer();
	~Renderer();
    void Init();
    void Clear() const;
    void Update(const Camera& camera);
    void Shutdown() const;
    void UpdateView(const Camera& camera);
    void Render(const Camera& camera, Renderable& renderable, Shader& renderableShader);
};