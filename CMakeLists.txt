cmake_minimum_required(VERSION 3.10)
project(AlbusIonosphere LANGUAGES CXX)

# 1. Get environment variables or fallback to defaults
set(ALBUS_PATH $ENV{ALBUS_PATH} CACHE PATH "Path to ALBUS install")
set(INSTALLDIR $ENV{ALBUS_PATH} CACHE PATH "Path to ALBUS install")
set(MAJOR_VERSION $ENV{MAJOR_VERSION} CACHE STRING "Major version")
set(MINOR_VERSION $ENV{MINOR_VERSION} CACHE STRING "Minor version")

# 2. Find Python and NumPy (REQUIRED for pybind11 / NumPy C API)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)

# 3. Include directories for headers
include_directories(
    ${Python3_INCLUDE_DIRS}
    ${Python3_NumPy_INCLUDE_DIRS}
   
    
    ${CMAKE_CURRENT_SOURCE_DIR}/source_dir/vex_to_sky2
    ${CMAKE_CURRENT_SOURCE_DIR}/source_dir/C++/mim/test/PIMrunner
    ${CMAKE_CURRENT_SOURCE_DIR}/source_dir/FORTRAN/SOFA/sofa
    ${CMAKE_CURRENT_SOURCE_DIR}/source_dir/FORTRAN/IRI
    ${CMAKE_CURRENT_SOURCE_DIR}/source_dir/FORTRAN/PIM/PIM_1.7/pim/source/vlb4

   
)

# 4. Link directories for .so or .a libraries
link_directories(${ALBUS_PATH}/lib)

# 5. Define preprocessor macros for version info
add_definitions(-DMAJOR_VERSION=${MAJOR_VERSION} -DMINOR_VERSION=${MINOR_VERSION})

# 6. Add source_dir if it has sources or more targets
add_subdirectory(source_dir)

# 7. Create the shared library module
add_library(AlbusIonosphere MODULE AlbusIonosphere.cxx)
set_target_properties(AlbusIonosphere PROPERTIES
    PREFIX ""
    SUFFIX ".cpython-310-x86_64-linux-gnu.so" # This gives .cpython-310-x86_64-linux-gnu.so
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH TRUE
)


# 8. Link the required external libraries
target_link_libraries(AlbusIonosphere
    PRIVATE
    mim
    jmavex
    iri
    pim
    sofa
    vexplus
    vex
    fl
    gfortran
    m
    ${Python3_LIBRARIES}
)

install(TARGETS AlbusIonosphere
        LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/albusionosphere) 

install(CODE "execute_process(COMMAND touch ${CMAKE_SOURCE_DIR}/albusionosphere/__init__.py)")
