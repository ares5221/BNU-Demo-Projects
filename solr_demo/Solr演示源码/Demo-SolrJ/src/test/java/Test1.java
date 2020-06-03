import com.kgc.document.Product;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.UpdateResponse;
import org.junit.jupiter.api.Test;

import java.io.IOException;

/**
 * SolrJ
 * 增删改
 */
public class Test1 {
    //连接Solr
    private HttpSolrClient solrClient = new HttpSolrClient.Builder("http://127.0.0.1:8983/solr").build();

    /**
     * 增加 - id不存在时
     * 修改 - id存在时
     */
    @Test
    public void test3() throws IOException, SolrServerException {
        Product product = new Product();
        product.setId("100");
        product.setName("春夏秋冬");
        product.setPrice(666.89);
        product.setMerchant("雅戈尔旗舰店");
        product.setProvince("浙江");
        product.setCity("宁波");

        UpdateResponse updateResponse = solrClient.addBean("product", product);
        //提交
        solrClient.commit("product");

        int status = updateResponse.getStatus(); //响应状态 0-成功
        System.out.println("响应状态："+status);
    }

    /**
     * 删除
     * 根据ID删除文档
     */
    @Test
    public void test1() throws IOException, SolrServerException {
        //根据ID删除文档
        UpdateResponse updateResponse = solrClient.deleteById("product", "24");
        //提交
        solrClient.commit("product");

        int status = updateResponse.getStatus(); //响应状态 0-成功
        System.out.println("响应状态："+status);
    }

    /**
     * 删除
     * 根据其它条件删除文档
     */
    @Test
    public void test2() throws IOException, SolrServerException {
        String query = "name:爽肤水";
        UpdateResponse updateResponse = solrClient.deleteByQuery("product",query);
        //提交
        solrClient.commit("product");

        int status = updateResponse.getStatus(); //响应状态 0-成功
        System.out.println("响应状态："+status);
    }

}
