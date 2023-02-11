#pragma once

#include <unordered_map>
#include <vector>
#include "primitives/Renderable.h"
#include "Camera.h"
#include "Shader.h"



class Renderer {
	std::vector<Renderable> _renderList;
public:
	Renderer();
	~Renderer();
    void Init();
    void Update(const Camera& camera);
    void Shutdown() const;
    void UpdateView(const Camera& camera);
    void Render(const Camera& camera, Renderable& renderable, Shader& renderableShader);
};