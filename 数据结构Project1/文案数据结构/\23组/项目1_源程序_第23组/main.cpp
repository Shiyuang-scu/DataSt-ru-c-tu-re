
//
//  main.cpp
//  数据结构Project1
//
//  Created by 施宇昂 on 2018/10/30.
//  Copyright © 2018 施宇昂. All rights reserved.
//
#include "AStack.h"
#include "AQueue.h"
#include <iostream>
#include <cmath>
#include <stdlib.h>
#define MAX_SIZE 100
using namespace std;
bool isdigit(char ch);
bool IsOperator(char ch);
int isp(char ch);
int osp(char ch);
bool cal(char op, double x, double y, double& r);
bool Get2Operands(AStack<double> & opnd,  double &x, double &y);
void IntegrateCal(AStack<double> & , AStack<char> & );
void MainInterface();
bool option();

int main(int argc, const char * argv[]) {
    // insert code here...
    AStack<double> OPND;
    AStack<char> OPTR;
    
    while(1)
    {
        system("clear");      //清屏在mac上无效
        MainInterface();
        IntegrateCal(OPND, OPTR);
        printf("是否继续？<y/n>\n");
        getchar();
        if(option())
        {
            continue;
        }
        else
        {
            break;
        }
    }
    system("clear");      //清屏在mac上无效
    printf("Have a good day!\nSee you!\n");

    return 0;
}


void MainInterface(){
    printf("*****************欢迎使用Advanced栈式计算器*****************\n");
    printf("使用说明：\n");
    printf("表达数可包括：\n");
    printf("1. 加（+）、减（-）、乘（*）、除（/）、求模（％）、开方（&）和乘方（^）运算符\n");
    printf("2. 括号\n");
    printf("\n输入表达式<以“=”结束>\n");
}
bool option(){
    while(1)
    {
        char flag = getchar();
        if(flag=='n')
        {
            return false;
        }
        else if(flag=='y')
        {
            return true;
        }
        else
        {
            system("clear");      //清屏在mac上无效
            getchar();
            printf("非法字符！请重新输入……\n");
            printf("是否继续？<y/n>\n");
            continue;
        }
    }
}

int isp(char ch){
    if(ch == '+')
        return 3;
    else if(ch == '=')
        return 0;
    else if(ch == '-')
        return 3;
    else if(ch == '*')
        return 5;
    else if(ch == '%')
        return 5;
    else if(ch == '/')
        return 5;
    else if(ch == '(')
        return 1;
    else if(ch == ')')
        return 8;
    else if(ch == '^')
        return 7;
    else if(ch == '&')
        return 7;
    else
        return -1;
}   //获取并返回操作符 ch 的栈内优先级

int osp(char ch){
    if (ch == '=') {
        return 0;
    }
    else if(ch == '('){
        return 8;
    }
    else if(ch == ')'){
        return 1;
    }
    else{
        return (isp(ch) - 1);}

}   // 获取并返回操作符 ch 的栈外优先级

bool  cal(char op, double x, double y, double & r){
    if(op == '+')
    {
        r = x+y;
    }
    else if(op == '-')
    {
       r = x - y;

    }
    else if(op == '*')
    {
        r = x * y;

    }
    else if(op == '%')
    {
        r = fmod(x, y);

    }
    else if(op == '/')
    {
        r = x / y;

    }
    else if(op == '^')
    {
        r = pow(x,y);

    }
    else if(op == '&')
    {
        r = pow(x, 1.0/y);

    }
    else{
        return false;
    }

    return true;
}   // 计算r = x op y， 计算成功，返回true.

bool isdigit(char ch){
    if (ch >= 0 && ch <= 9){
        return true;
    }
    else{
        return false;
    }
}     // 判断ch是否为数字0-9

bool IsOperator(char ch){
    char ptr[10] = {'+', '-', '*', '/', '(', ')', '=', '&', '%', '^'};
    int i;
    for(i=0; i<10; i++) {
            if(ch==ptr[i])
                return true;
             }
    return false;
}     //判断ch是否为操作符

bool Get2Operands(AStack<double> & opnd,  double &x, double &y){
    if(opnd.pop(y)&&opnd.pop(x)){
        return true;
    }
    else{
        return false;
    }

}   //从操作数栈中取2个操作数

void IntegrateCal(AStack<double> & OPND, AStack<char> & OPTR){
    char OPTR_top, OPTR_temp;
    double OPND_temp1, OPND_temp2, OPND_result;
    char* temp;
    char dest[MAX_SIZE];
    char *str = (char *) malloc (sizeof(char) * 100);
    bool flag;
    
    scanf("%s",str);
    OPTR.push('=');
    OPND.push(0);
    while(*str != '\0')
    {
        temp = dest;
        while((*str >= '0' && *str <= '9') || *str == '.')           /*判断是否是数据*/
        {
            *temp = *str;
            str ++;
            temp ++;
        }                               /*遇到符号退出*/
        
        if(*str != '(' && *(temp - 1) != '\0')      /*判断符号是否为'('*/
        {
            *temp = '\0';
            OPND.push(atof(dest));      /*将字符串转为数字,将数据压入数据栈*/
        }
        
        /*
         1.若栈内优先级低于栈外优先级,则将当前字符push入运算符栈(optr), 继续处理下一个字符
         */
        /*
         2.若栈内优先级高于栈外优先级, 从操作数栈(opnd)中pop出2个操作数,
         从运算符栈(optr)中pop出最顶端运算符进行计算,并将计算结果push进操作数栈(opnd) ,继续处理当前字符
         */
        /*
         3.若栈内优先级等于栈外优先级, 从运算符栈(optr)中pop出最顶端运算符, 继续处理下一个字符.
         */
        while(!((*str >= '0' && *str <= '9') || *str == '.'))
        {
            if(!IsOperator(*str)){
                //system("clear");      清屏在mac上无效
                printf("非法输入，请重试……\n");
                return;
            }
            
            OPTR.topValue(OPTR_top);
            flag = (isp(OPTR_top) < osp(*str));      /*判断操作符优先级*/
            if(flag)
            {
                OPTR.push(*str);   /*压入操作符*/
                break;
            }
            else if(isp(OPTR_top) == osp(*str))                         /*判断括号内的表达式是否结束*/
            {
                OPTR.pop(OPTR_temp);
                break;
            }
            else if(!flag)                        /*进行数据处理*/
            {
                Get2Operands(OPND, OPND_temp1, OPND_temp2);     /*取两个数据*/
                OPTR.pop(OPTR_temp);    /*弹出一个操作符*/
                cal(OPTR_temp, OPND_temp1, OPND_temp2, OPND_result);   /*计算*/
                OPND.push(OPND_result);
                continue;
                //OPTR.push(*str);    /*将当前操作符压入栈内*/
            }
            if(OPTR_top == '=')
            {
                break;
            }
        }
        str ++;                 /*指向表达式下一个字符*/
    }
    OPND.pop(OPND_result);
    printf("num: %f\n", OPND_result);
}
