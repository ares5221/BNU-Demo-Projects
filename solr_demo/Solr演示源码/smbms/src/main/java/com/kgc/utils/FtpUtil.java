package com.kgc.utils;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.util.UUID;

public class FtpUtil {

    //ftp服务器ip地址
    private static final String FTP_ADDRESS = "192.168.0.106";
    //端口号
    private static final int FTP_PORT = 21;
    //用户名
    private static final String FTP_USERNAME = "user-file";
    //密码
    private static final String FTP_PASSWORD = "123";
    //附件路径
    private static final String FTP_BASEPATH = "/home/user-file/files";

    public static String uploadFile(MultipartFile file) throws IOException {
        //获取上传的文件流
        InputStream inputStream = file.getInputStream();

        //获取上传的文件名
        String filename = file.getOriginalFilename();
        //截取后缀
        String suffix = filename.substring(filename.lastIndexOf("."));
        //使用UUID拼接后缀，定义一个不重复的文件名
        String finalName = UUID.randomUUID()+suffix;

        FTPClient ftp = new FTPClient();
        try {
            int reply;
            ftp.connect(FTP_ADDRESS, FTP_PORT);// 连接FTP服务器
            ftp.login(FTP_USERNAME, FTP_PASSWORD);// 登录
            reply = ftp.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                ftp.disconnect();
                return null;
            }
            ftp.setFileType(FTPClient.BINARY_FILE_TYPE);
            ftp.makeDirectory(FTP_BASEPATH);
            ftp.changeWorkingDirectory(FTP_BASEPATH );
            ftp.enterLocalPassiveMode();
            ftp.storeFile(finalName,inputStream);
            inputStream.close();
            ftp.logout();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            if (ftp.isConnected()) {
                try {
                    ftp.disconnect();
                } catch (IOException ioe) {
                    ioe.printStackTrace();
                }
            }
        }
        return finalName;
    }
}
