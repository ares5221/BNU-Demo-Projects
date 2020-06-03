package com.kgc.service.impl;

import com.kgc.dao.UserMapper;
import com.kgc.pojo.User;
import com.kgc.pojo.UserCriteria;
import com.kgc.service.UserService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class UserServiceImpl implements UserService {

    @Resource
    private UserMapper userMapper;

    @Override
    public List<User> getUserList() {
        return userMapper.selectByExample(null);
    }

    @Override
    public User getUserByLogin(String userName, String password) {
        UserCriteria userCriteria = new UserCriteria();
        userCriteria.createCriteria()
                .andUsernameEqualTo(userName)
                .andUserpasswordEqualTo(password);

        List<User> userList = userMapper.selectByExample(userCriteria);
        if(userList != null && userList.size() >0){
            return userList.get(0);
        }

        return null;
    }
}
