package com.kgc.dao;

import com.kgc.pojo.Provider;
import com.kgc.pojo.ProviderCriteria;
import java.util.List;
import org.apache.ibatis.annotations.Param;

public interface ProviderMapper {
    int countByExample(ProviderCriteria example);

    int deleteByExample(ProviderCriteria example);

    int deleteByPrimaryKey(Long id);

    int insert(Provider record);

    int insertSelective(Provider record);

    List<Provider> selectByExample(ProviderCriteria example);

    Provider selectByPrimaryKey(Long id);

    int updateByExampleSelective(@Param("record") Provider record, @Param("example") ProviderCriteria example);

    int updateByExample(@Param("record") Provider record, @Param("example") ProviderCriteria example);

    int updateByPrimaryKeySelective(Provider record);

    int updateByPrimaryKey(Provider record);
}