from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OGREConan(ConanFile):
    name = "OGRE"
    version = "1.11.3"
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
                installer.install("libfreeimage-dev")
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
        git = tools.Git()
        git.clone("https://github.com/OGRECave/ogre.git", "v1.11.3")
        tools.replace_in_file("CMakeLists.txt", "# OGRE BUILD SYSTEM","include(${CMAKE_BINARY_DIR}/conan_paths.cmake)")
        tools.replace_in_file("Components/Overlay/CMakeLists.txt",
        '''target_link_libraries(OgreOverlay PUBLIC OgreMain PRIVATE "${FREETYPE_LIBRARIES}" ZLIB::ZLIB)''',
        '''target_link_libraries(OgreOverlay PUBLIC OgreMain PRIVATE Freetype::Freetype ZLIB::ZLIB)''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGRE_BUILD_COMPONENT_PYTHON'] = 'OFF'
        cmake.definitions['OGRE_BUILD_SAMPLES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D9'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D11'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL3PLUS'] = 'OFF'
        cmake.definitions['OGRE_RESOURCEMANAGER_STRICT'] = 0
        cmake.definitions['OGRE_INSTALL_SAMPLES'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="Dependencies/include")
        self.copy("*.lib", dst="lib", src="Dependencies", keep_path=False)
        self.copy("*.dll", dst="bin", src="Dependencies", keep_path=False)
        self.copy("*.so*", dst="lib", src="Dependencies", keep_path=False)
        self.copy("*.a*", dst="lib", src="Dependencies", keep_path=False)
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
