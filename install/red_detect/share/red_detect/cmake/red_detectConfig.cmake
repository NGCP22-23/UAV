# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_red_detect_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED red_detect_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(red_detect_FOUND FALSE)
  elseif(NOT red_detect_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(red_detect_FOUND FALSE)
  endif()
  return()
endif()
set(_red_detect_CONFIG_INCLUDED TRUE)

# output package information
if(NOT red_detect_FIND_QUIETLY)
  message(STATUS "Found red_detect: 0.0.0 (${red_detect_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'red_detect' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  message(WARNING "${_msg}")
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(red_detect_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${red_detect_DIR}/${_extra}")
endforeach()
