cmake_minimum_required(VERSION 3.10)
project(vexplus CXX)

#----------------------------------------------------------------------------
# Configuration variables
#----------------------------------------------------------------------------
# Define an INSTALLDIR variable (by default, use CMAKE_INSTALL_PREFIX)
if(NOT DEFINED INSTALLDIR)
  set(INSTALLDIR ${CMAKE_INSTALL_PREFIX} CACHE PATH "Installation directory")
endif()


#----------------------------------------------------------------------------
# Include directories
#----------------------------------------------------------------------------
# These mimic the Makefile’s -I options.
# Adjust the paths as needed.
include_directories(
  ../vex2005
)

#----------------------------------------------------------------------------
# Source and header files
#----------------------------------------------------------------------------
set(SRCS
  vexplus.cxx
)

set(HEADERS
  vexplus.h
)

#----------------------------------------------------------------------------
# Library Targets
#----------------------------------------------------------------------------
# Create a shared library target that will produce libvexplus.so with versioning.
add_library(vexplus SHARED ${SRCS})
set_target_properties(vexplus PROPERTIES
  OUTPUT_NAME "vexplus"
  VERSION "${VER_MAJOR}.${VER_MINOR}.${VER_SUBSUB}"
  SOVERSION "${VER_MAJOR}"
)
set_target_properties(vexplus PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH TRUE
)

target_link_libraries(vexplus PRIVATE vex)
#----------------------------------------------------------------------------
# Installation rules
#----------------------------------------------------------------------------
# Install the shared library and header file(s) to the specified directories.
install(TARGETS vexplus LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/albusionosphere
)


