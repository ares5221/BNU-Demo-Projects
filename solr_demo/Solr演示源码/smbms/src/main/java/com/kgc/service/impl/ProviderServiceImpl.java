package com.kgc.service.impl;

import com.alibaba.druid.util.StringUtils;
import com.kgc.dao.ProviderMapper;
import com.kgc.pojo.Provider;
import com.kgc.pojo.ProviderCriteria;
import com.kgc.service.ProviderService;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class ProviderServiceImpl implements ProviderService {

    @Resource
    private ProviderMapper providerMapper;

    @Cacheable(value = "provider", key = "'getProviderList'")
    @Override
    public List<Provider> getProviderList() {
        System.out.println("getProviderList方法被调用。。。。");
        return providerMapper.selectByExample(null);
    }

    @CacheEvict(value = "provider", allEntries = true)
    @Override
    public int delProviderById(Long id) {
        return providerMapper.deleteByPrimaryKey(id);
    }

    @Cacheable(value="provider1", key = "'getProviderById'+#id")
    @Override
    public Provider getProviderById(Long id) {
        return providerMapper.selectByPrimaryKey(id);
    }

    @Cacheable(value="provider2", key = "'getProviderByNameOrPhone'+#name+','+#phone")
    @Override
    public List<Provider> getProviderByNameOrPhone(String name, String phone) {
        ProviderCriteria providerCriteria = new ProviderCriteria();
        ProviderCriteria.Criteria criteria = providerCriteria.createCriteria();
        if(!StringUtils.isEmpty(name)){
            criteria.andPronameLike("%"+name+"%");
        }
        if(!StringUtils.isEmpty(phone)){
            criteria.andProphoneLike("%"+phone+"%");
        }
        return providerMapper.selectByExample(providerCriteria);
    }
}
