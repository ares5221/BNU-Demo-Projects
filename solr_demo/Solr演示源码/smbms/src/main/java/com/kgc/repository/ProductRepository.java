package com.kgc.repository;

import com.kgc.document.Product;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.solr.core.query.result.HighlightPage;
import org.springframework.data.solr.repository.Highlight;
import org.springframework.data.solr.repository.SolrCrudRepository;

public interface ProductRepository extends SolrCrudRepository<Product,String> {

    void deleteByName(String name);

    long countByName(String name);

    @Highlight(prefix = "<font color='red'>", postfix = "</font>")
    HighlightPage<Product> findByName(String name, PageRequest pageRequest);
}
