package com.kgc.dao;

import com.kgc.pojo.BillEx;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface BillMapperEx {
    List<BillEx> getBillListByParam(@Param("productName") String productName,
                                    @Param("providerId") Integer providerId,
                                    @Param("isPayment") Integer isPayment);

    BillEx getBillDetailById(Long id);
}
