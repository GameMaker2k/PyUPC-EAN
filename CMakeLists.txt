project(PyUPC-EAN NONE)
cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp REQUIRED)

add_custom_target(build ALL
    COMMAND ${PYTHON_EXECUTABLE} setup.py build --build-base ${CMAKE_BINARY_DIR}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )

# DESTDIR may be set at install time (eg: `make DESTDIR=/tmp/package install`)
# so we need to check for it when the install code is run and pass the appropriate
# argument to distutils.
#
# Note that if(\$ENV{DESTDIR}) always fails, regardless of the value of the DESTDIR
# environment variable, hence the STREQUAL test.
# See http://public.kitware.com/Bug/view.php?id=14737
install(CODE
    "set(_root_arg)
     if (NOT \$ENV{DESTDIR} STREQUAL \"\")
         set(_root_arg --root \$ENV{DESTDIR})
     endif()
     execute_process(
        COMMAND ${PYTHON_EXECUTABLE} setup.py install --prefix ${CMAKE_INSTALL_PREFIX} \${_root_arg}
        WORKING_DIRECTORY \"${CMAKE_SOURCE_DIR}\"
        )"
    )
