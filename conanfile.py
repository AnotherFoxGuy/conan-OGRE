from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OGREConan(ConanFile):
    name = "OGRE"
    version = "1.11.5"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"
    requires = ("GC/3.1@AnotherFoxGuy/stable",
                "freetype/2.9.0@bincrafters/stable",
                "FreeImage/3.18.0@AnotherFoxGuy/stable",
                "sdl2/2.0.9@bincrafters/stable",
                "zlib/1.2.11@conan/stable",
                "libZZIP/0.13.63@AnotherFoxGuy/stable")

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("xorg-dev")
                installer.install("libfreeimage-dev")
                installer.install("libgl1-mesa-dev")
                installer.install("libglu1-mesa-dev")
                installer.install("nvidia-cg-toolkit")
                installer.install("libopenal-dev")
                installer.install("libx11-dev")
                installer.install("libxt-dev")
                installer.install("libxaw7-dev")

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/OGRECave/ogre.git", "v1.11.5")
        tools.replace_in_file("CMakeLists.txt", "# OGRE BUILD SYSTEM","include(${CMAKE_BINARY_DIR}/conan_paths.cmake)")
        tools.replace_in_file("CMake/Packages/FindFreeImage.cmake",
            "set(FreeImage_LIBRARY_NAMES freeimage freeimageLib FreeImage FreeImageLib)",
            "set(FreeImage_LIBRARY_NAMES freeimage freeimageLib FreeImage FreeImageLib libFreeImage)")
        tools.replace_in_file("CMake/Packages/FindZZip.cmake",
            "set(ZZip_LIBRARY_NAMES zziplib zzip zzip-0)",
            "set(ZZip_LIBRARY_NAMES zziplib zzip zzip-0 libzziplib)")
        tools.replace_in_file("CMake/Dependencies.cmake",
            '''set(OGRE_DEPENDENCIES_DIR "" CACHE PATH "Path to prebuilt OGRE dependencies")''',
            '''set(OGRE_DEPENDENCIES_DIR ${CMAKE_PREFIX_PATH})''')
        tools.replace_in_file("CMake/Utils/FindPkgMacros.cmake",
            'set(${PREFIX} optimized ${${PREFIX}_REL} debug ${${PREFIX}_DBG})',
            'set(${PREFIX} ${${PREFIX}_REL} ${${PREFIX}_DBG})')


    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGRE_BUILD_DEPENDENCIES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_PLUGIN_STBI'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_PYTHON'] = 'OFF'
        cmake.definitions['OGRE_BUILD_SAMPLES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D9'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D11'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL3PLUS'] = 'ON'
        cmake.definitions['OGRE_RESOURCEMANAGER_STRICT'] = 0
        cmake.definitions['OGRE_INSTALL_SAMPLES'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include',
                                     'include/OGRE',
                                     'include/OGRE/Bites',
                                     'include/OGRE/HLMS',
                                     'include/OGRE/MeshLodGenerator',
                                     'include/OGRE/Overlay',
                                     'include/OGRE/Paging',
                                     'include/OGRE/Plugins',
                                     'include/OGRE/Property',
                                     'include/OGRE/RenderSystems',
                                     'include/OGRE/RTShaderSystem',
                                     'include/OGRE/Terrain',
                                     'include/OGRE/Threading',
                                     'include/OGRE/Volume'
        ]
        self.cpp_info.libs = tools.collect_libs(self)
