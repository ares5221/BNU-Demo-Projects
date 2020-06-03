package com.kgc.service;

import com.kgc.document.Product;
import org.apache.solr.client.solrj.SolrServerException;

import java.io.IOException;
import java.util.Map;

public interface ProductService {
    int delProduct(Integer id) throws IOException, SolrServerException;

    int delProductByName(String name) throws IOException, SolrServerException;

    int addOrUpdProduct(Product product) throws IOException, SolrServerException;

    Map<String, Object> getProductListByName(String name, Integer pageNow, Integer pageSize) throws IOException, SolrServerException;
}
