import com.alibaba.fastjson.JSONObject;
import com.kgc.document.Product;
import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.beans.DocumentObjectBinder;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.List;

/**
 * SolrJ-查询
 */
public class Test2 {
    //连接Solr
    private HttpSolrClient solrClient = new HttpSolrClient.Builder("http://127.0.0.1:8983/solr").build();

    /**
     * 根据ID查询文档
     */
    @Test
    public void test1() throws IOException, SolrServerException {
        SolrDocument solrDocument = solrClient.getById("product", "21");

        //文档解析器
        DocumentObjectBinder binder = solrClient.getBinder();
        //将SolrDocument转为自定义对象Product
        Product product = binder.getBean(Product.class, solrDocument);

        String jsonString = JSONObject.toJSONString(product);
        System.out.println(jsonString);
    }

    /**
     * 其它条件查询
     */
    @Test
    public void test2() throws IOException, SolrServerException {
        //查询条件
        SolrQuery solrQuery = new SolrQuery();

        /*solrQuery.set("q","name:衬衫");
        solrQuery.set("fq","price: [50 TO 100]");
        solrQuery.set("sort","price asc");
        solrQuery.set("start","0");
        solrQuery.set("rows","3");*/

        solrQuery.setQuery("name:衬衫");
        solrQuery.setFilterQueries("price: [50 TO 100]");
        solrQuery.setSort("price", SolrQuery.ORDER.asc);
        solrQuery.setStart(0);
        solrQuery.setRows(3);

        QueryResponse queryResponse = solrClient.query("product", solrQuery);

        //获取结果行数
        long numFound = queryResponse.getResults().getNumFound();
        System.out.println("结果行数："+numFound);

        //转为集合List
        List<Product> productList = queryResponse.getBeans(Product.class);
        for (Product product :productList) {
            String jsonString = JSONObject.toJSONString(product);
            System.out.println(jsonString);
        }
    }
}
