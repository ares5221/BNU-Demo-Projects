package com.kgc.service.impl;

import com.kgc.document.Product;
import com.kgc.repository.ProductRepository;
import com.kgc.service.ProductService;
import org.apache.solr.client.solrj.SolrServerException;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.solr.core.query.result.HighlightEntry;
import org.springframework.data.solr.core.query.result.HighlightPage;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ProductServiceImpl implements ProductService {

    @Resource
    private ProductRepository productRepository;

    @Override
    public int delProduct(Integer id) throws IOException, SolrServerException {
        //删除MySQL数据库中的商品....

        //删除Solr中对应的商品
        productRepository.deleteById(id.toString());
        return 0;
    }

    @Override
    public int delProductByName(String name) throws IOException, SolrServerException {
        //删除MySQL数据库中的商品....

        //删除Solr中对应的商品
        productRepository.deleteByName(name);
        return 0;
    }

    @Override
    public int addOrUpdProduct(Product product) throws IOException, SolrServerException {
        //增加或修改MySQL数据库中的商品....

        //增加或修改Solr中对应的商品
        productRepository.save(product);
        return 0;
    }

    @Override
    public Map<String, Object> getProductListByName(String name, Integer pageNow, Integer pageSize) throws IOException, SolrServerException {
        //获取数据总行数
        long count = productRepository.countByName(name);

        //分页参数 page-页码,0表示第一页  size-每页显示行数
        PageRequest pageRequest = PageRequest.of(pageNow-1, 3);
        //获取高亮结果
        HighlightPage<Product> highlightPage = productRepository.findByName(name,pageRequest);

        //获取含高亮字段的所有结果
        List<HighlightEntry<Product>> highlighted = highlightPage.getHighlighted();

        //修改普通字段的值为高亮值
        for (HighlightEntry<Product> highlightEntry:highlighted) {
            Product product = highlightEntry.getEntity();//普通结果
            List<HighlightEntry.Highlight> highlights = highlightEntry.getHighlights();//高亮结果集合

            //遍历当前对象所有高亮字段
            for (HighlightEntry.Highlight highlight : highlights) {
                String filedName = highlight.getField().getName();//高亮字段名
                String snipplets = highlight.getSnipplets().get(0);//高亮字段值
                if (filedName.equals("name")) {
                    product.setName(snipplets);//替换为高亮内容
                }
            }
        }

        //获取最终结果
        List<Product> productList = highlightPage.getContent();

        Map<String, Object> map = new HashMap<>();
        map.put("count",count);
        map.put("list",productList);
        return map;
    }
}
