//
//  AStack.h
//  DataStructure_Stack
//
//  Created by 施宇昂 on 2018/10/11.
//  Copyright © 2018 施宇昂. All rights reserved.
//

#ifndef AStack_h
#define AStack_h

// First, get the declaration for the base stack class
#include "Stack.h"
//kakaka
// Array-based stack implementation
template <class Elem> class AStack: public Stack<Elem> {
private:
    int size;                 // Maximum size of stack
    int top;                  // Index for top element
    Elem *listArray;          // Array holding stack elements
public:
    AStack(int sz =20)     // Constructor
    { size = sz;  top = 0; listArray = new Elem[sz]; }
    //~AStack() { delete [] listArray; }  // Destructor
    void clear() { top = 0; }
    bool push(const Elem& item) {
        if (top == size) return false; // Stack is full
        else { listArray[top++] = item;  return true; }
    }
    bool pop(Elem& it) {            // Pop top element
        if (top == 0) return false;
        else { it = listArray[--top];  return true; }
    }
    bool topValue(Elem& it) const { // Return top element
        if (top == 0) return false;
        else { it = listArray[top-1];  return true; }
    }
    int length() const { return top; }
};

#endif /* AStack_h */
