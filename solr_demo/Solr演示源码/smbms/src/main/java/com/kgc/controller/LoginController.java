package com.kgc.controller;

import com.kgc.pojo.User;
import com.kgc.service.UserService;
import com.kgc.utils.Result;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.time.Duration;
import java.util.UUID;

/**
 * 登录控制器
 * 登录，注册
 */
@RestController
public class LoginController {

    @Resource
    private UserService userService;

    @Resource
    private RedisTemplate<String, Object> redisTemplate;

    /**
     * 注销
     * @return
     */
    @GetMapping("view/logout")
    public Result logout(HttpServletRequest request){
        String token = request.getHeader("token");
        //删除Redis中的token
        Boolean delete = redisTemplate.delete(token);

        return new Result(delete,"注销成功",100);
    }

    /**
     * 从Redis中获取登录用户信息
     * @param request
     * @return
     * @throws UnsupportedEncodingException
     */
    @GetMapping("view/getUserOfLogin")
    public Result getUserOfLogin(HttpServletRequest request) throws UnsupportedEncodingException {
        //获取Headers中的参数
        String token = request.getHeader("token");

        Object user = redisTemplate.opsForValue().get(token);
        if(user != null){
            return new Result(user, "获取登录用户成功", 100);
        }
        return new Result(null, "获取登录用户失败", 104);
    }

    /**
     * 登录
     * @param userName
     * @param password
     * @param response
     * @return
     * @throws UnsupportedEncodingException
     */
    @PostMapping("login")
    public Result login(@RequestParam String userName,@RequestParam String password, HttpServletResponse response) throws UnsupportedEncodingException {
        User user = userService.getUserByLogin(userName,password);
        if(user != null){//登录成功
            //生成Token令牌
            String token = UUID.randomUUID()+"";
            //存到Redis数据库
            redisTemplate.opsForValue().set(token,user, Duration.ofMinutes(30L));

            return new Result(token,"登录成功",100);
        }

        return new Result(null,"登录失败",104);
    }
}
