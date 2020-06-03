package com.kgc.controller;

import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class BaseController {
    public String uploadFile(MultipartFile multipartFile) throws IOException {
        //文件路径
        String path = "C:\\Users\\程龙\\Desktop\\D\\SMBMS-WEB\\upload";
        File dir = new File(path);
        if(!dir.exists()){//文件夹不存在则创建
            dir.mkdir();
        }

        //文件原名
        String filename = multipartFile.getOriginalFilename();
        //文件后缀 123.jpg
        String suffix = filename.substring(filename.lastIndexOf("."));
        //存储的文件名
        String newName = UUID.randomUUID()+suffix;

        File file = new File(path+"/"+newName);

        //存储文件
        multipartFile.transferTo(file);
        return newName;
    }
}
