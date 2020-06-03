package com.kgc.controller;

import com.kgc.document.Product;
import com.kgc.service.ProductService;
import com.kgc.utils.Result;
import org.apache.solr.client.solrj.SolrServerException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.io.IOException;
import java.util.Map;

@RestController
public class ProductController {

    @Resource
    private ProductService productService;

    /**
     * 根据ID删除商品
     * @return
     */
    @GetMapping("delProduct")
    public Result delProduct(Integer id) throws IOException, SolrServerException {
        int status = productService.delProduct(id);

        return new Result(status,"删除商品成功", 100);
    }

    /**
     * 根据name删除商品
     * @return
     */
    @GetMapping("delProductByName")
    public Result delProductByName(String name) throws IOException, SolrServerException {
        int status = productService.delProductByName(name);

        return new Result(status,"删除商品成功", 100);
    }

    /**
     * 根据ID增加/修改商品
     * 增加-ID在Solr中不存在
     * 修改-ID在Solr中已存在
     * @return
     */
    @PostMapping("addOrUpdProduct")
    public Result addOrUpdProduct(Product product) throws IOException, SolrServerException {
        int status = productService.addOrUpdProduct(product);

        return new Result(status,"增加/修改商品成功", 100);
    }

    /**
     * 获取商品列表-分页
     * @param name 商品名
     * @param pageNow 页码
     * @param pageSize 每页显示行数
     * @return
     */
    @GetMapping("getProductListByName")
    public Result getProductListByName(String name, Integer pageNow, Integer pageSize) throws IOException, SolrServerException {
        Map<String, Object> map = productService.getProductListByName(name,pageNow,pageSize);

        return new Result(map,"获取商品列表成功", 100);
    }
}
