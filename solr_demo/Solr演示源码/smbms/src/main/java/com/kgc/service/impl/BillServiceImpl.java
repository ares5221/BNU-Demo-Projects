package com.kgc.service.impl;

import com.kgc.dao.BillMapper;
import com.kgc.dao.BillMapperEx;
import com.kgc.pojo.Bill;
import com.kgc.pojo.BillEx;
import com.kgc.service.BillService;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class BillServiceImpl implements BillService {

    @Resource
    private BillMapperEx billMapperEx;
    @Resource
    private BillMapper billMapper;

    @Override
    public List<BillEx> getBillListByParam(String productName, Integer providerId, Integer isPayment) {
        return billMapperEx.getBillListByParam(productName, providerId, isPayment);
    }

    @Override
    public int delBillById(Long id) {
        return billMapper.deleteByPrimaryKey(id);
    }

    @Override
    public int addBill(Bill bill) {
        return billMapper.insertSelective(bill);
    }

    @Override
    public Bill getBillById(Long id) {
        return billMapper.selectByPrimaryKey(id);
    }

    @Override
    public int updBill(Bill bill) {
        return billMapper.updateByPrimaryKeySelective(bill);
    }

    @Override
    public BillEx getBillDetailById(Long id) {
        return billMapperEx.getBillDetailById(id);
    }
}
