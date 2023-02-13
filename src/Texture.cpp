#include "Texture.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"


Texture::~Texture() {
    glDeleteTextures(1, &_id);
}

void Texture::SetTexture(const char* path, std::string name, bool flip) {
    _type = GL_TEXTURE_2D;
    std::string tempPath = std::string(path);

    if(flip) {
        stbi_set_flip_vertically_on_load(true);
    }
    else {
        stbi_set_flip_vertically_on_load(false);
    }

    glGenTextures(1, &_id);
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(_type, _id);

    int width, height, components;
    unsigned char* data = stbi_load(tempPath.c_str(), &width, &height, &components, 0);


    _width = width;
    _height = height;
    _components = components;
    _name = name;

    if (data) {   
        switch (components) {
        case 1:
            _format = GL_RED;
            break;        
        case 3:
            _format = GL_RGB;
            break;
        case 4:
            _format = GL_RGBA;
            break;
        default:
            break;
        }
        _internalFormat = _format;

        glTexImage2D(GL_TEXTURE_2D, 0, _internalFormat, _width, _height, 0, _format, GL_UNSIGNED_BYTE,  data);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);     // Need AF to get rid of the blur on textures
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glGenerateMipmap(GL_TEXTURE_2D);
    }
    else {
        std::cerr << "TEXTURE FAILED - LOADING : " << path << std::endl;
    }

    stbi_image_free(data);

   glBindTexture(_type, 0);
}

void Texture::UseTexture() const {
    glBindTexture(_type, _id);
}