//
//  Queue.h
//  DataStructure_Stack
//
//  Created by 施宇昂 on 2018/10/11.
//  Copyright © 2018 施宇昂. All rights reserved.
//

#ifndef Queue_h
#define Queue_h
// Abstract queue class
template <class Elem> class Queue {
public:
    // Reinitialize the queue.  The user is responsible for
    // reclaiming the storage used by the stack elements.
    virtual void clear() = 0;
    // Place an element at the rear of the queue.  Return
    // true if successful, false if not (if queue is full).
    virtual bool enqueue(const Elem&) = 0;
    // Remove the element at the front of the queue. Return
    // true if succesful, false if queue is empty.
    // The element removed is returned in the first parameter.
    virtual bool dequeue(Elem&) = 0; // Remove Elem from front
    // Return in first parameter a copy of the front element.
    // Return true if succesful, false if queue is empty.
    virtual bool frontValue(Elem&) const = 0;
    // Return the number of elements in the queue.
    virtual int length() const = 0;
};

#endif /* Queue_h */
