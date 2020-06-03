package com.kgc.service;

import com.kgc.pojo.Bill;
import com.kgc.pojo.BillEx;

import java.util.List;

public interface BillService {
    List<BillEx> getBillListByParam(String productName, Integer providerId, Integer isPayment);

    int delBillById(Long id);

    int addBill(Bill bill);

    Bill getBillById(Long id);

    int updBill(Bill bill);

    BillEx getBillDetailById(Long id);
}
