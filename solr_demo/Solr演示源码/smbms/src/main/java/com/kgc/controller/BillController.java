package com.kgc.controller;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.kgc.pojo.Bill;
import com.kgc.pojo.BillEx;
import com.kgc.service.BillService;
import com.kgc.utils.Result;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@RestController
public class BillController extends BaseController{

    @Resource
    private BillService billService;

    /**
     * 根据ID获取订单详情
     * 含供应商名称
     * @return
     */
    @GetMapping("view/getBillDetailById")
    public Result getBillDetailById(@RequestParam Long id){
        BillEx bill = billService.getBillDetailById(id);

        return new Result(bill, "获取订单详情成功",100);
    }

    /**
     * 添加或修改订单，含上传文件
     * 有ID-修改订单
     * 无ID-添加订单
     * @param bill
     * @param multipartFile
     * @return
     * @throws IOException
     */
    @PostMapping("view/addOrUpdBill")
    public Result addOrUpdBill(Bill bill, @RequestParam(value = "productPic", required = false) MultipartFile multipartFile) throws IOException {
        if(multipartFile != null && !multipartFile.isEmpty()){
            //上传文件
            String fileName = uploadFile(multipartFile);

            //添加上传的文件名，存储到数据库
            bill.setProductpic(fileName);
        }

        if(bill.getId() != null) {//修改
            bill.setModifydate(new Date());
            int count = billService.updBill(bill);

            if (count > 0) {
                return new Result(null, "修改订单成功", 100);
            }
            return new Result(null, "修改订单失败，请重试", 104);
        }else{//添加
            bill.setCreationdate(new Date());
            int count = billService.addBill(bill);

            if(count > 0){
                return new Result(null, "添加订单成功",100);
            }
            return new Result(null, "添加订单失败，请重试",104);
        }
    }

    /**
     * 根据ID获取订单详情
     * @param id
     * @return
     */
    @GetMapping("view/getBillById")
    public Result getBillById(@RequestParam Long id){
        Bill bill = billService.getBillById(id);

        return new Result(bill, "获取订单成功",100);
    }

    /**
     * 根据ID删除订单
     * @param id
     * @return
     */
    @GetMapping("view/delBillById")
    public Result delBillById(@RequestParam Long id){
        int count = billService.delBillById(id);
        if(count > 0){
            return new Result(null, "删除订单成功",100);
        }
        return new Result(null, "删除订单失败，订单不存在，请重试",104);
    }

    /**
     * 根据参数获取订单列表
     * @param productName
     * @param providerId
     * @param isPayment
     * @return
     */
    @GetMapping("view/getBillListByParam")
    public Result getBillListByParam(@RequestParam Integer pageNow, @RequestParam Integer pageSize,String productName, Integer providerId, Integer isPayment){
        PageHelper.startPage(pageNow, pageSize);

        List<BillEx> list = billService.getBillListByParam(productName, providerId, isPayment);

        PageInfo<BillEx> pageInfo = new PageInfo<>(list);
        return new Result(pageInfo,"获取订单列表成功",100);
    }
}
