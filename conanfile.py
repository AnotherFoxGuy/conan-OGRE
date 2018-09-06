from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OGREConan(ConanFile):
    name = "OGRE"
    version = "1.9.1"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("xorg-dev")
                installer.install("libfreetype6-dev")
                installer.install("libfreeimage-dev")
                installer.install("libzzip-dev")
                installer.install("libois-dev")
                installer.install("libgl1-mesa-dev")
                installer.install("libglu1-mesa-dev")
                installer.install("nvidia-cg-toolkit")
                installer.install("libopenal-dev")
                installer.install("libx11-dev")
                installer.install("libxt-dev")
                installer.install("libxaw7-dev")


    def requirements(self):
        if os_info.is_windows:
            self.requires.add('OGREdeps/2018-07@anotherfoxguy/stable')

    def source(self):
        self.run("git clone --branch v1.9.1 --depth 1 https://github.com/OGRECave/ogre.git . ")
        tools.replace_in_file("CMakeLists.txt", "# OGRE BUILD SYSTEM","include(${CMAKE_BINARY_DIR}/conan_paths.cmake)")
        tools.download("https://raw.githubusercontent.com/RigsOfRods/ror-dependencies/master/patches/OgreTerrain.cpp", "Components/Terrain/src/OgreTerrain.cpp", overwrite=True)
        tools.download("https://raw.githubusercontent.com/RigsOfRods/ror-dependencies/master/patches/OgreD3D9Prerequisites.h", "RenderSystems/Direct3D9/include/OgreD3D9Prerequisites.h", overwrite=True)
		
    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGREDEPS_BUILD_AMD_QBS'] = 'OFF'
        cmake.definitions['OGRE_BUILD_SAMPLES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_VOLUME'] = 'OFF'
        cmake.definitions['OGRE_BUILD_PLUGIN_BSP'] = 'OFF'
        cmake.definitions['OGRE_BUILD_PLUGIN_PCZ'] = 'OFF'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D9'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D11'] = 'OFF'  # TODO
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL3PLUS'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["OGRE"]
