cmake_minimum_required(VERSION 3.10)
project(jmavex_project LANGUAGES CXX Fortran)

#----------------------------------------------------------------------------
# Configuration Variables
#----------------------------------------------------------------------------
# Set installation directory (adjust as needed) – note that CMAKE_INSTALL_PREFIX
# is typically used for installation, but we mimic the Makefile variable here.
set(INSTALLDIR "/path/to/install" CACHE PATH "Installation directory")

# For linking with Fortran libraries (e.g. gfortran runtime); adjust if needed.
set(F77_COMPILER_LIB "gfortran" CACHE STRING "Fortran compiler library name")

#----------------------------------------------------------------------------
# Include Directories & Link Directories
#----------------------------------------------------------------------------
# These mimic the -I options from the Makefile.
include_directories(
  vex2005
  vexplus
  ../mim/test/PIMrunner
  ${INSTALLDIR}/include
)

# If the external libraries are not in standard locations, add their directories.
link_directories(${INSTALLDIR}/lib ../mim/test/PIMrunner)

#----------------------------------------------------------------------------
# Define Sources and Headers
#----------------------------------------------------------------------------
set(HEADERS
  ellipsoidal_coord.h
  ut1_interp.h
  vex_source.h
  vex_time.h
  vex_ut1_interp.h
)

set(SRCS
  ellipsoidal_coord.cxx
  ut1_interp.f
  vex_iono_processor.cxx
  vex_time.cxx
  vex_ut1_interp.cxx
)

#----------------------------------------------------------------------------
# Add Subdirectories
#----------------------------------------------------------------------------
# These subdirectories should contain their own CMakeLists.txt.
add_subdirectory(vex2005)
add_subdirectory(vexplus)

#----------------------------------------------------------------------------
# Create Library Targets Using an Object Library
#----------------------------------------------------------------------------
# Create an OBJECT library from the common sources so that both a shared and
# static library can be built without compiling the sources twice.
add_library(jmavex_obj OBJECT ${SRCS})

# Build shared library (libjmavex.so)
add_library(jmavex_shared SHARED $<TARGET_OBJECTS:jmavex_obj>)
set_target_properties(jmavex_shared PROPERTIES
  OUTPUT_NAME "jmavex"
  VERSION "1.0.0"
  SOVERSION "1"
)

# Build static library (libjmavex.a)
add_library(jmavex_static STATIC $<TARGET_OBJECTS:jmavex_obj>)
set_target_properties(jmavex_static PROPERTIES
  OUTPUT_NAME "jmavex"
)

# Link the external libraries to the shared library target.
# This mirrors the Makefile’s EXTERN_LIBS:
#   -lvexplus -lvex -lfl -lsofa -l$(F77_COMPILER_LIB)
target_link_libraries(jmavex_shared PRIVATE
  vexplus
  vex
  fl
  sofa
  ${F77_COMPILER_LIB}
)

#----------------------------------------------------------------------------
# Define Executable Targets
#----------------------------------------------------------------------------
# The Makefile builds two programs:
#
# 1. "ell_coord_converter" – originally built from ellipsoidal_coord.o and
#    ell_coord_converter.o. Here we assume a source file "ell_coord_converter.cxx"
#    exists. We include "ellipsoidal_coord.cxx" so that this executable is built
#    only from the two files as in the original.
#
# 2. "test" – built from test.o plus all the common object files.
#
# You may need to adjust the source file names as appropriate.

# ell_coord_converter executable
add_executable(ell_coord_converter ell_coord_converter.cxx ellipsoidal_coord.cxx)
# Link the math library (for -lm) if required.
target_link_libraries(ell_coord_converter PRIVATE m)

# test executable (assumes a source file "test.cxx" exists)
add_executable(test test.cxx)
target_link_libraries(test PRIVATE
  jmavex_shared
  vexplus
  vex
  fl
  sofa
  ${F77_COMPILER_LIB}
  m
)

#----------------------------------------------------------------------------
# Installation Rules
#----------------------------------------------------------------------------
# Install the shared (and optionally static) library, headers, and executables.
install(TARGETS jmavex_shared
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)

install(TARGETS jmavex_static
  ARCHIVE DESTINATION lib
)

install(FILES ${HEADERS} DESTINATION include)

install(TARGETS ell_coord_converter test
  RUNTIME DESTINATION bin
)

#----------------------------------------------------------------------------
# (Optional) Additional Custom Targets
#----------------------------------------------------------------------------
# The original Makefile provided "clean", "distclean", and "depend" rules.
# CMake-generated build systems (e.g. Makefiles or Ninja) already include a "clean" target.

