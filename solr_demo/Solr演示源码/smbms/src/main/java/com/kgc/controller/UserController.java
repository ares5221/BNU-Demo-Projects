package com.kgc.controller;

import com.alibaba.druid.util.StringUtils;
import com.kgc.pojo.User;
import com.kgc.service.UserService;
import com.kgc.utils.FtpUtil;
import com.kgc.utils.Result;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.UUID;

@RestController
public class UserController {

    @Resource
    private UserService userService;

    /**
     * 添加用户，含文件上传
     * @param user
     * @param file
     * @return
     * @throws IOException
     */
    @PostMapping("addUser")
    public Object addUser(User user, @RequestParam("headPic") MultipartFile file) throws IOException {
        //调用自定义的FTP工具类上传文件
        String fileName = FtpUtil.uploadFile(file);

        if(!StringUtils.isEmpty(fileName)){
            //设置对象中的图片名
            //user.setPicPath(fileName);

            //添加用户到数据库
            //userService.addUser(user);
        }

        return new Result(fileName,"添加用户成功",100);
    }

    @RequestMapping("getUserList")
    public Object getUserList(){
        List<User> userList = userService.getUserList();

        return new Result(userList,"获取用户列表成功",100);
    }
}