from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OGREConan(ConanFile):
    name = "OGRE"
    version = "1.11.6"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "win32-directx/*"
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
        self.requires.add('OGREdeps/2018-07@anotherfoxguy/stable')

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/OGRECave/ogre.git", "v1.11.6")
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
        tools.patch(patch_string='''
--- OgreMain/src/OgreScriptLexer.cpp
+++ OgreMain/src/OgreScriptLexer.cpp
@@ -82 +82 @@
- return tokens;
+ braceLayer = 1;
             ''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGRE_BUILD_DEPENDENCIES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_CSHARP'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_JAVA'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_PYTHON'] = 'OFF'
        cmake.definitions['OGRE_BUILD_PLUGIN_STBI'] = 'OFF'
        cmake.definitions['OGRE_BUILD_COMPONENT_PYTHON'] = 'OFF'
        cmake.definitions['OGRE_BUILD_SAMPLES'] = 'OFF'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D9'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D11'] = 'ON'
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL3PLUS'] = 'OFF'
        cmake.definitions['OGRE_RESOURCEMANAGER_STRICT'] = 0
        cmake.definitions['OGRE_INSTALL_SAMPLES'] = 'OFF'
        if os_info.is_windows:
            cmake.definitions['CMAKE_CXX_FLAGS'] = '-D_OGRE_FILESYSTEM_ARCHIVE_UNICODE'
            cmake.definitions['DirectX9_D3DX9_LIBRARY'] = 'win32-directx/lib/x86/d3dx9.lib'
            cmake.definitions['DirectX9_DXERR_LIBRARY'] = 'win32-directx/lib/x86/DxErr.lib'
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
