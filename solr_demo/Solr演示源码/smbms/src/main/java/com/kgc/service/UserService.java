package com.kgc.service;

import com.kgc.pojo.User;

import java.util.List;

public interface UserService {
    List<User> getUserList();

    User getUserByLogin(String userName, String password);
}
