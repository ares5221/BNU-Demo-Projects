package com.kgc.controller;

import com.kgc.utils.Result;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * 异常通知类
 */
@ControllerAdvice //当Controller抛出异常时，调用
public class ExceptionAdvice {

    @ResponseBody //将返回值直接响应到客户端
    @ExceptionHandler(value = ArithmeticException.class) //捕获算术异常
    public Object handelException(ArithmeticException e){
        e.printStackTrace();

        return new Result(null,"请求异常:"+e.getMessage(),101);
    }

    @ResponseBody
    @ExceptionHandler(value = NullPointerException.class)
    public Object handelException(NullPointerException e){
        e.printStackTrace();

        return new Result(null,"请求异常:"+e.getMessage(),101);
    }

    @ResponseBody
    @ExceptionHandler(value = Exception.class)
    public Object handelException(Exception e){
        e.printStackTrace();

        return new Result(null,"请求异常:"+e.getMessage(),101);
    }
}
