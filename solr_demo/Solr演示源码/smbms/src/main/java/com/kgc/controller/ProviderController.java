package com.kgc.controller;

import com.kgc.pojo.Provider;
import com.kgc.service.ProviderService;
import com.kgc.utils.Result;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.time.Duration;
import java.util.List;

@RestController
public class ProviderController {

    @Resource
    private ProviderService providerService;

    @Resource
    private RedisTemplate<String, Object> redisTemplate;

    @GetMapping("view/getOrderTime")
    public Result getOrderTime(String orderNo){
        //或者指定Key的剩余时间
        Long expire = redisTemplate.getExpire(orderNo);

        return new Result(expire,"获取订单剩余时间成功",100);
    }

    @GetMapping("view/addOrder")
    public Result addOrder(){
        //创建订单。。。数据库操作

        //订单ID存到Redis,存30分钟
        redisTemplate.opsForValue().set("orderid1234","添加的订单",
                Duration.ofMinutes(30L));

        return new Result(null,"创建订单成功",100);
    }

    /**
     *
     * 根据条件获取供应商
     * 供应商名称
     * 手机号
     * @return
     */
    @GetMapping("view/getProviderByNameOrPhone")
    public Result getProviderByNameOrPhone(String name, String phone){
        List<Provider> list = providerService.getProviderByNameOrPhone(name, phone);

        return new Result(list,"获取供应商成功",100);
    }

    /**
     *
     * 根据ID获取供应商
     * @return
     */
    @GetMapping("view/getProviderById")
    public Result getProviderById(Long id){
        Provider provider = providerService.getProviderById(id);

        return new Result(provider,"获取供应商成功",100);
    }

    /**
     * 获取供应商列表
     * @return
     */
    @GetMapping("view/getProviderList")
    public Result getProviderList(){
        List<Provider> list = providerService.getProviderList();

        return new Result(list,"获取供应商列表成功",100);
    }

    /**
     * 根据ID删除供应商
     * @return
     */
    @GetMapping("view/delProviderById")
    public Result delProviderById(Long id){
        int count = providerService.delProviderById(id);

        return new Result(count,"删除供应商列表成功",100);
    }
}
