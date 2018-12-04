//
//  AQueue.h
//  DataStructure_Stack
//
//  Created by 施宇昂 on 2018/10/11.
//  Copyright © 2018 施宇昂. All rights reserved.
//

#ifndef AQueue_h
#define AQueue_h
// This is the file to include in your code if you want access to the
// complete AQueue template class

// First, get the declaration for the base stack class
#include "Queue.h"

// Array-based queue implementation
template <class Elem> class AQueue: public Queue<Elem> {
private:
    int size;                  // Maximum size of queue
    int front;                 // Index of front element
    int rear;                  // Index of rear element
    Elem *listArray;           // Array holding queue elements
public:
    AQueue(int sz =20) { // Constructor
        // Make list array one position larger for empty slot
        size = sz+1;
        rear = 0;  front = 1;
        listArray = new Elem[size];
    }
    //~AQueue() { delete [] listArray; } // Destructor
    void clear() { front = rear; }
    bool enqueue(const Elem& it) {
        if (((rear+2) % size) == front) return false;  // Full
        rear = (rear+1) % size; // Circular increment
        listArray[rear] = it;
        return true;
    }
    bool dequeue(Elem& it) {
        if (length() == 0) return false;  // Empty
        it = listArray[front];
        front = (front+1) % size; // Circular increment
        return true;
    }
    bool frontValue(Elem& it) const {
        if (length() == 0) return false;  // Empty
        it = listArray[front];
        return true;
    }
    virtual int length() const
    { return ((rear+size) - front + 1) % size; }
};


#endif /* AQueue_h */
