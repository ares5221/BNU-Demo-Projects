package com.kgc.dao;

import com.kgc.pojo.Bill;
import com.kgc.pojo.BillCriteria;
import java.util.List;
import org.apache.ibatis.annotations.Param;

public interface BillMapper {
    int countByExample(BillCriteria example);

    int deleteByExample(BillCriteria example);

    int deleteByPrimaryKey(Long id);

    int insert(Bill record);

    int insertSelective(Bill record);

    List<Bill> selectByExample(BillCriteria example);

    Bill selectByPrimaryKey(Long id);

    int updateByExampleSelective(@Param("record") Bill record, @Param("example") BillCriteria example);

    int updateByExample(@Param("record") Bill record, @Param("example") BillCriteria example);

    int updateByPrimaryKeySelective(Bill record);

    int updateByPrimaryKey(Bill record);
}