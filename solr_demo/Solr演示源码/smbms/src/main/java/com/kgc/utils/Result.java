package com.kgc.utils;

import java.io.Serializable;

/**
 * 数据接口返回对象
 */
public class Result {
    private Object data;//响应数据
    private String message;//响应提示信息

    /**
     * 响应编码
     * 100-请求成功
     * 101-请求异常
     * 103-未登录
     * 104-请求失败
     */
    private int code;

    public Result(){}

    public Result(Object data, String message, int code) {
        this.data = data;
        this.message = message;
        this.code = code;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }
}
