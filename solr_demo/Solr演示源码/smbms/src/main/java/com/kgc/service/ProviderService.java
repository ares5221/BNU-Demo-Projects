package com.kgc.service;

import com.kgc.pojo.Provider;

import java.util.List;

public interface ProviderService {
    List<Provider> getProviderList();

    int delProviderById(Long id);

    Provider getProviderById(Long id);

    List<Provider> getProviderByNameOrPhone(String name, String phone);
}
