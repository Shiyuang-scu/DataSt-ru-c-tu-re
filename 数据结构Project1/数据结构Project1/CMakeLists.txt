cmake_minimum_required(VERSION 3.12)
project(Project1)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(Project1
        AQueue.h
        AStack.h
        main.cpp
        Queue.h
        Stack.h
        test.cpp)
