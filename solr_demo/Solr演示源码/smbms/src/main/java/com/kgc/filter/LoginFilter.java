package com.kgc.filter;

import com.alibaba.druid.util.StringUtils;
import com.alibaba.fastjson.JSONObject;
import com.kgc.utils.Result;
import org.springframework.data.redis.core.RedisTemplate;

import javax.annotation.Resource;
import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.concurrent.TimeUnit;

/**
 * 登录过滤器
 */
@WebFilter(urlPatterns = {"/view/*"})
public class LoginFilter implements Filter {
    @Resource
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        //校验用户登录状态
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;

        //Filter过滤器跨域处理
        String origin = request.getHeader("Origin");
        response.setHeader("Access-Control-Allow-Origin", origin);
        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,token");
        response.setHeader("Access-Control-Allow-Credentials", "true");

        //获取Headers中的参数
        String token = request.getHeader("token");
        token = token == null ? "" : token;

        //查询token在Redis中的剩余时间
        Long expire = redisTemplate.getExpire(token);
        if(expire > 0){ //是登录状态
            //重置token的时间
            redisTemplate.expire(token,30L, TimeUnit.MINUTES);

            //放行
            filterChain.doFilter(servletRequest,servletResponse);
        }else{
            //未登录，响应数据
            String string = JSONObject.toJSONString(new Result(null, "未登录", 103));

            response.setContentType("json/text;charset=utf-8");
            PrintWriter out = response.getWriter();

            out.write(string);
        }
    }

    @Override
    public void destroy() {

    }
}
