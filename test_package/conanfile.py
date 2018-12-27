from conans.model.conan_file import ConanFile
from conans import CMake, tools
import os


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "openssl/1.1.1@conanos/stable"

    def _build_cmake(self, use_find_package):
        cmake = CMake(self)

        if self.settings.os == "Android":
            cmake.definitions["CONAN_LIBCXX"] = ""
        cmake.definitions["USE_FIND_PACKAGE"] = use_find_package
        cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info["openssl"].rootpath
        cmake.definitions["OPENSSL_USE_STATIC_LIBS"] = not self.options["openssl"].shared
        if self.settings.compiler == 'Visual Studio':
            cmake.definitions["OPENSSL_MSVC_STATIC_RT"] = 'MT' in str(self.settings.compiler.runtime)

        cmake.configure()
        cmake.build()

    def build(self):
        self._build_cmake(use_find_package=True)
        self._build_cmake(use_find_package=False)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin", root_package="openssl")
        self.copy(pattern="*.dylib", dst="bin", src="lib", root_package="openssl")

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("cd bin && .%sdigest" % os.sep)
        assert os.path.exists(os.path.join(self.deps_cpp_info["openssl"].rootpath, "LICENSE"))
