cmake_minimum_required(VERSION 3.22.1)

project(edgegenai)

add_library(
        edgegenai
        SHARED
        native-lib.cpp
)

find_library(
        log-lib
        log
)

target_link_libraries(
        edgegenai
        ${log-lib}
)